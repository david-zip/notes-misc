"""Feature engineers the abalone dataset."""
import argparse
import logging
import os
import pathlib
import requests
import tempfile

import boto3
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
#from sklearn.compose import ColumnTransformer
#from sklearn.impute import SimpleImputer
#from sklearn.pipeline import Pipeline
#from sklearn.preprocessing import StandardScaler, OneHotEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    logger.debug("Starting preprocessing.")
    base_dir = "house-price-prediction-p-li0pqhei7lcj/sagemaker-house-price-prediction-p-li0pqhei7lcj-modelbuild/pipelines/abalone"
    
    logger.info("Reading data")
    fn = f"{base_dir}/data/Housing.csv"
    raw_data = pd.read_csv(fn)

    logger.debug("Defining transformers.")
    boolmap = {
        "yes": 1,
        "no": 0
    }

    catemap = {
        "furnished": 2, 
        "semi-furnished": 1, 
        "unfurnished": 0
    }

    processed_data = raw_data.replace({
                                    "mainroad": boolmap,
                                    "guestroom": boolmap,
                                    "basement": boolmap,
                                    "hotwaterheating": boolmap,
                                    "airconditioning": boolmap,
                                    "prefarea": boolmap,
                                    "furnishingstatus": catemap
                      })

    logger.info("Applying transforms.")
    logger.info("Splitting %d rows of data into train, validation, test datasets.", len(processed_data))
    train, test = train_test_split(processed_data, test_size=0.2)

    logger.info("Writing out datasets to %s.", base_dir)
    pd.DataFrame(train).to_csv(f"{base_dir}/data/train.csv", header=False, index=False)
    pd.DataFrame(test).to_csv(f"{base_dir}/data/test.csv", header=False, index=False)
