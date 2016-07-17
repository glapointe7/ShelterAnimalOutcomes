#!/usr/bin/python3

from Model import *


def Main():
    # Load train and test sets.
    train = Dataset()
    train.Load("train.csv")
    test = Dataset()
    test.Load("test.csv")

    # Explore the train set.
    #train.Explore()

    # Transform / create / remove features from train and test sets.
    train.ConvertAgeToInteger()
    train.ConvertNameToBool()
    train.ExtractSterilityAsInteger()
    train.ExtractFeaturesFromDateTime()
    train.ConvertAnimalTypeToBool()
    train.ExtractNumberOfColors()

    test.ConvertAgeToInteger()
    test.ConvertNameToBool()
    test.ExtractSterilityAsInteger()
    test.ExtractFeaturesFromDateTime()
    test.ConvertAnimalTypeToBool()
    test.ExtractNumberOfColors()

    trainModel = Model(train)


if __name__ == "__main__":
    Main()