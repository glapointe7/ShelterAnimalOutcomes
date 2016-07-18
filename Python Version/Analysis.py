#!/usr/bin/python3

from Model import *


def main():
    # Load train and test sets.
    train = Dataset()
    train.load("train.csv")
    test = Dataset()
    test.load("test.csv")

    # Explore the train set.
    #train.explore()

    # Transform / create / remove features from train and test sets.
    train.convertAgeToInteger()
    train.convertNameToBool()
    train.extractSterilityAsInteger()
    train.extractFeaturesFromDateTime()
    train.convertAnimalTypeToBool()
    train.extractNumberOfColors()

    test.convertAgeToInteger()
    test.convertNameToBool()
    test.extractSterilityAsInteger()
    test.extractFeaturesFromDateTime()
    test.convertAnimalTypeToBool()
    test.extractNumberOfColors()

    train_model = Model(train, test)
    #best_parameters = train_model.findBestParameters(number_of_estimators=100)
    predictions = train_model.train({'learning_rate': 0.12, 'subsample': 0.8, 'colsample_bytree': 0.9}, 200)
    train_model.save(predictions)


if __name__ == "__main__":
    main()