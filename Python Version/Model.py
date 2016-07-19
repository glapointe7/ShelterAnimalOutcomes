#!/usr/bin/python3

from sklearn.grid_search import GridSearchCV
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import classification_report
import numpy

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

        grid_cv = GridSearchCV(estimator=xgb_classifier, param_grid=grid_parameters, scoring='log_loss', cv=number_of_folds)
        grid_cv.fit(self._train_matrix, self._target)

        print("Best parameters set found on development set:")
        print()
        print(grid_cv.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        for params, mean_score, scores in grid_cv.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        cv_predictions = grid_cv.predict(self._train_matrix)
        print(classification_report(self._target, cv_predictions))
        print()

        return grid_cv.best_params_

    #
    # def crossValidate(self, best_parameters, number_of_estimators):
    #     number_of_folds = 10
    #     parameters = {'max_depth': 8,
    #                   'objective': 'multi:softprob',
    #                   'eval_metric': 'mlogloss',
    #                   'eta': best_parameters['learning_rate'],
    #                   'subsample': best_parameters['subsample'],
    #                   'colsample_bytree': best_parameters['colsample_bytree'],
    #                   'num_class': 5,
    #                   'seed': 1234,
    #                   'silent': True}
    #
    #     self._train_matrix = xgb.DMatrix(self._train_matrix, self._target)
    #     model_cv = xgb.cv(parameters, self._train_matrix, number_of_estimators, number_of_folds)
    #
    #     return model_cv

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

        predictions_test = model.predict(self._test_matrix)
        predictions_train = model.predict(self._train_matrix)

        print('Train Log-Loss = ' + repr(self.multiClassLogLoss(numpy.array(self._target), numpy.array(predictions_train))))

        importance = xgb.plot_importance(model)
        fig = importance.get_figure()
        fig.savefig('FeatureImportance.png')

        trees = xgb.plot_tree(model, num_trees=1)
        fig = trees.get_figure()
        fig.savefig('Trees.png')

        return pandas.DataFrame(predictions_test)

    """
    Multi class version of Logarithmic Loss metric.
    https://www.kaggle.com/wiki/MultiClassLogLoss

    idea from this post:
    http://www.kaggle.com/c/emc-data-science/forums/t/2149/is-anyone-noticing-difference-betwen-validation-and-leaderboard-error/12209#post12209

    Parameters
    ----------
    y_true : array, shape = [n_samples]
    y_pred : array, shape = [n_samples, n_classes]

    Returns
    -------
    loss : float
    """
    def multiClassLogLoss(self, y_true, y_pred, eps=1e-15):
        predictions = numpy.clip(y_pred, eps, 1 - eps)

        # Normalize row sums to 1.
        predictions /= predictions.sum(axis=1)[:, numpy.newaxis]

        actual = numpy.zeros(y_pred.shape)
        rows = actual.shape[0]
        actual[numpy.arange(rows), y_true.astype(int)] = 1
        vsota = numpy.sum(actual * numpy.log(predictions))

        return -1.0 / rows * vsota

    # Create the final dataframe with the predictions and save it in a CSV file.
    def save(self, predictions):
        submission = pandas.DataFrame()
        submission['id'] = self._test_id
        submission['Adoption'] = predictions[0]
        submission['Died'] = predictions[1]
        submission['Euthanasia'] = predictions[2]
        submission['Return_to_owner'] = predictions[3]
        submission['Transfer'] = predictions[4]

        submission.to_csv('Submission_py.csv', index=False)