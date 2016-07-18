#!/usr/bin/python3

from sklearn.metrics import log_loss
from sklearn.grid_search import GridSearchCV
import xgboost as xgb
from xgboost.sklearn import XGBClassifier

from Dataset import *


class Model:
    _train_matrix = []
    _test_matrix = []
    _target = []
    _test_id = []

    def __init__(self, train, test):
        self._train_matrix = train.get()
        train.convertOutcomeToInteger()
        self._target = self._train_matrix['OutcomeType'].values
        self._train_matrix.drop('AnimalID', axis=1, inplace=True)
        self._train_matrix.drop('OutcomeType', axis=1, inplace=True)
        self._train_matrix.drop('OutcomeSubtype', axis=1, inplace=True)

        self._test_matrix = test.get()
        self._test_id = self._test_matrix['ID'].values
        self._test_matrix.drop('ID', axis=1, inplace=True)

    # Find the best parameters to apply to the xgboost algorithm depending on the dataset and the target.
    def findBestParameters(self, number_of_estimators):
        number_of_folds = 10
        classifier_parameters = {'max_depth': 8,
                                 'n_estimators': number_of_estimators,
                                 'objective': 'multi:softprob',
                                 'seed': 1234}
        grid_parameters = {'learning_rate': [0.1, 0.12, 0.15],
                           'subsample': [0.8, 0.75],
                           'colsample_bytree': [0.9, 0.85]}

        xgb_classifier = XGBClassifier(**classifier_parameters)

        grid_cv = GridSearchCV(estimator=xgb_classifier, param_grid=grid_parameters, cv=number_of_folds)
        grid_cv.fit(self._train_matrix, self._target)

        return grid_cv.best_params_

    #
    def crossValidate(self, best_parameters, number_of_estimators):
        number_of_folds = 10
        parameters = {'max_depth': 8,
                      'objective': 'multi:softprob',
                      'eval_metric': 'mlogloss',
                      'eta': best_parameters['learning_rate'],
                      'subsample': best_parameters['subsample'],
                      'colsample_bytree': best_parameters['colsample_bytree'],
                      'num_class': 5,
                      'seed': 1234,
                      'silent': True}

        self._train_matrix = xgb.DMatrix(self._train_matrix, self._target)
        model_cv = xgb.cv(parameters, self._train_matrix, number_of_estimators, number_of_folds)

        return model_cv

    #
    def train(self, best_parameters, number_of_estimators):
        parameters = {'max_depth': 8,
                      'objective': 'multi:softprob',
                      'eval_metric': 'mlogloss',
                      'eta': best_parameters['learning_rate'],
                      'subsample': best_parameters['subsample'],
                      'colsample_bytree': best_parameters['colsample_bytree'],
                      'num_class': 5,
                      'seed': 1234,
                      'silent': 1}

        self._train_matrix = xgb.DMatrix(self._train_matrix, self._target)
        self._test_matrix = xgb.DMatrix(self._test_matrix, self._target)
        model = xgb.train(parameters, self._train_matrix, number_of_estimators)

        predictions = model.predict(self._test_matrix)
        importance = xgb.plot_importance(model)
        fig = importance.get_figure()
        fig.savefig('FeatureImportance.png')

        return pandas.DataFrame(predictions)

    #
    def save(self, predictions):
        submission = pandas.DataFrame()
        submission['id'] = self._test_id
        submission['Adoption'] = predictions[0]
        submission['Died'] = predictions[1]
        submission['Euthanasia'] = predictions[2]
        submission['Return_to_owner'] = predictions[3]
        submission['Transfer'] = predictions[4]

        submission.to_csv('Submission_py.csv', index=False)