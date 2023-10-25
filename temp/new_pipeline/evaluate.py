import os
import logging
import pickle
import tarfile
import pandas

from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

if __name__=='__main__':
    model_path = "/opt/ml/processing/model/model.tar.gz"
    with tarfile.open(model_path) as tar:
        tar.extractall(path='..')
    
    