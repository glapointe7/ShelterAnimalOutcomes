#!/usr/bin/python3

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import log_loss
import xgboost as xgb

from Dataset import *

class Model:
    _dataset = []


    def __init__(self, dataset):
        outcomes = range(0, len(dataset.GetUniqueOutcomeTypes()) - 1)
        dataset.RemoveFeatures(['OutcomeType', 'OutcomeSubtype'])
        self._dataset = dataset.Get()
        self._dataset = xgb.DMatrix(self._dataset, outcomes)


    def CrossValidate(self, numberOfTrees):
        numberOfFolds = 10
        #cvModel = xgb.cv(param = param, data = self._dataset, nfold = numberOfFolds, nrounds = numberOfTrees)