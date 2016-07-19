#!/usr/bin/python3

from Model import *


def main():
    # Load train and test sets.
    train = Dataset()
    train.load("../train.csv")
    test = Dataset()
    test.load("../test.csv")

    # Explore the train set.
    #train.explore()

    # Transform / create / remove features from train and test sets.
    train.convert_age_to_integer()
    train.convert_name_to_bool()
    train.extract_sterility()
    train.extract_features_from_datetime()
    train.convert_animal_type_to_bool()
    train.extract_number_of_colors()
    train.extract_breed_types()
    train.extract_special_breeds()

    test.convert_age_to_integer()
    test.convert_name_to_bool()
    test.extract_sterility()
    test.extract_features_from_datetime()
    test.convert_animal_type_to_bool()
    test.extract_number_of_colors()
    test.extract_breed_types()
    test.extract_special_breeds()

    train_model = Model(train, test)
    best_parameters = train_model.find_best_parameters(number_of_estimators=100)
    #best_parameters = {'subsample': 0.8, 'colsample_bytree': 0.9, 'learning_rate': 0.12}
    predictions = train_model.train(best_parameters, number_of_estimators=100)
    train_model.save(predictions)


if __name__ == "__main__":
    main()