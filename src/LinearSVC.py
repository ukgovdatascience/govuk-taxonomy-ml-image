# coding: utf-8
"""Automated algorithm selection using TPOT for GOVUK tagging
"""
import pandas as pd
import numpy as np
import os
import logging
import logging.config
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.svm import LinearSVC
from datetime import datetime
# Load env vars

# TPOT vars

TPOT_TESTSIZE = float(os.getenv('TPOT_TESTSIZE'))

# file locations

DOCKERDATADIR = os.getenv('DOCKERDATADIR')
NOW = "{}_pipeline.py".format(datetime.now().strftime('%Y%m%d%H%M%S'))
PIPELINEFILE = os.path.join(DOCKERDATADIR, NOW)

# Setup pipeline logging

LOGGING_CONFIG = os.getenv('LOGGING_CONFIG')
logging.config.fileConfig(LOGGING_CONFIG)
logger = logging.getLogger('pipeline')

TAXONS = os.path.join(DOCKERDATADIR, 'clean_taxons.csv')
CONTENT = os.path.join(DOCKERDATADIR, 'clean_content.csv.gz')

logger.info('Loading taxons')
taxons = pd.read_csv(TAXONS)
logger.info('taxons.shape: %s', taxons.shape)

logger.info('Loading content')
content = pd.read_csv(CONTENT, compression='gzip')
logger.info('content.shape: %s', content.shape)

# ##  ------------- This data prep step should move to clean_content.py -------------
# 
# Remove taxons that are legacy (Imported), World, Corporate information.

taxons = taxons[['base_path','content_id','taxon_name','level1taxon',
                 'level2taxon','level3taxon','level4taxon']]

taxons['level1taxon'] = taxons['level1taxon'].astype('str')

# Drop taxons that start with Imported (i.e. legacy taxons at the top level)

taxons = taxons[~taxons['level1taxon'].str.startswith("Imported")]
taxons = taxons[~taxons['taxon_name'].str.startswith("Imported")]

logger.info("Taxons shape after deleting imported top taxons: %s", taxons.shape)

taxons = taxons[taxons.level1taxon != 'World']
taxons = taxons[taxons.taxon_name != 'World']

logger.info("Taxons shape after deleting 'World' top taxons: %s", taxons.shape)

taxons = taxons[taxons.level1taxon != 'Corporate information']
taxons = taxons[taxons.taxon_name != 'Corporate information']

logger.info("Taxons shape after deleting 'corporate information' top taxons: %s", taxons.shape)

# Convert nans to None

taxons['level1taxon'] = taxons['level1taxon'].where(taxons['level1taxon'] != 'nan', None)
taxons['level2taxon'] = taxons['level2taxon'].where(~taxons['level2taxon'].isnull(), None)

logger.info("Taxons shape after deleting nans to Nones: %s", taxons.shape)

# Combine the taxons with the content 

logger.info("Merging taxons and content")

content_taxons = pd.merge(left=content, right=taxons, left_on='taxon_id', 
                          right_on='content_id', how='outer', indicator=True)

logger.info("Merged taxon and content shape: %s", content_taxons.shape)

# ##  --------------------------------------------------

logger.info("Dropping nas from combined content and taxons")
content_taxons.dropna(subset = ['level2taxon'], inplace=True)
logger.info("This leaves %s pre-classified rows.", content_taxons.shape[0])

# There are likely to be lots of content items that have more than one tag. Check here and remove for now:
# TODO: devise a way to deal with multiple tags applied to each content item.

# Identify where duplicates exist on content_id and count


logger.info("Identifying content items which have >1 tag")

dupes = content_taxons['content_id_x'].value_counts().to_frame('dupes')
dupes = dupes.groupby('dupes').size().to_frame('count')

# Add index as a column

dupes.reset_index(level=0, inplace=True)

logger.info("Duplicates: %s", dupes)


multiple_tags = sum(dupes.loc[dupes['dupes'] > 1, 'count'])
single_tags = sum(dupes.loc[dupes['dupes'] == 1, 'count'])

logger.info("Stripping multiply applied tags to one will leave"
             "a total of %s tagged content items to train on",
             multiple_tags + single_tags)

logger.info("Dropping duplicates")
logger.info("Before deduplication that are %s items.", content_taxons.shape)
      
content_taxons.drop_duplicates(subset = ['content_id_x'], inplace=True)
      
logger.info("After deduplication that are %s items.", content_taxons.shape)

content_taxons['level2taxoncat'] = content_taxons['level2taxon'].astype('category')

# Drop bizarre anomalous row

content_taxons.drop(content_taxons['combined_text'].isnull().index, axis=0, inplace=True)

logger.info('Nan rows: %s', content_taxons['combined_text'].isnull().index)

logger.info("Running transformation pipeline")

nlp_pipeline = Pipeline([
	   ('vect', CountVectorizer()),
	   ('tfidf', TfidfTransformer()),
    ])

X = nlp_pipeline.fit_transform(content_taxons['combined_text'])

logger.info("Output dataset X has shape: %s", content_taxons.shape)
logger.info("Output dataset X has columns: %s", content_taxons.columns)
logger.info("Creating train/test split")

X_train, X_test, y_train, y_test = train_test_split(
    X, content_taxons['level2taxoncat'], test_size=TPOT_TESTSIZE, random_state=1337)

exported_pipeline = make_pipeline(
    SelectPercentile(score_func=f_classif, percentile=2),
    LinearSVC(C=10.0, dual=False, loss="squared_hinge", penalty="l2", tol=0.01)
)

logger.info("Initialising LinearSVC pipelinePOT with parameters: %s", nlp_pipeline)
logger.info("Running pipeline...")

exported_pipeline.fit_transform(X_train, y_train)

logger.info("TPOT score: %s", exported_pipeline.score(X_test, y_test))

# Score on the training set was:0.7925764732068796
