#!/usr/bin/python3

import pandas
import pathlib
from datetime import datetime


class Dataset:
    _dataset = []

    # Return the dataset.
    def get(self):
        return self._dataset

    # Load a dataset from a CSV file and replace the values in STRINGS_AS_NAN by NaN in the entire dataset.
    def load(self, filename):
        if pathlib.Path(filename).is_file():
            self._dataset = pandas.read_csv(filename, na_values='', parse_dates=True, delimiter=',')
        else:
            print('File' + filename + 'not found!')

    # Remove features (columns) specified from the dataset.
    def remove_features(self, features):
        self._dataset = self._dataset.drop(features, axis=1)

    # We transform the feature AgeuponOutcome to integer values. For example, the age should be counted in days.
    # Thus, 2 years is replaced by the value 2 * 365 = 730. For months, the formula is age * 30.
    # For weeks, the formula is age * 7. For years, the formula is age * 365.
    def convert_age_to_integer(self):
        age_list = self._dataset[['AgeuponOutcome']].values.tolist()
        age_list = [age[0] for age in age_list]

        ages = []
        for age in age_list:
            if pandas.isnull(age):
                ages.append(0)
            else:
                age_number, age_type = age.split(' ')
                if 'year' in age_type:
                    ages.append(int(age_number) * 365)
                elif 'month' in age_type:
                    ages.append(int(age_number) * 30)
                elif 'week' in age_type:
                    ages.append(int(age_number) * 7)
                elif 'day' in age_type:
                    ages.append(int(age_number))
                else:
                    ages.append(0)
        self._dataset['AgeInDays'] = ages
        self.remove_features('AgeuponOutcome')

    # The feature Name is transformed to a boolean value where the value is 0 when the animal has no name and 1 otherwise.
    def convert_name_to_bool(self):
        self._dataset['IsNamed'] = pandas.isnull(self._dataset['Name']).astype(int)
        self.remove_features('Name')

    # We replace the possible values of the AnimalType feature by 0 = Dog and 1 = Cat.
    def convert_animal_type_to_bool(self):
        self._dataset['AnimalType'] = (self._dataset['AnimalType'] == 'Cat').astype(int)

    # We replace the feature SexuponOutcome by Sterility where Unknown = 0, Intact = 1 and Sterile = 2.
    def extract_sterility(self):
        sex_upon_outcome = self._dataset['SexuponOutcome'].values.tolist()

        sterilities = []
        for sex in sex_upon_outcome:
            if pandas.isnull(sex):
                sterilities.append(0)
            else:
                sterility = sex.split(' ')
                if 'Unknown' in sterility:
                    sterilities.append(0)
                elif 'Intact' in sterility:
                    sterilities.append(1)
                elif any(sterility_type in sterility for sterility_type in ['Spayed', 'Neutered']):
                    sterilities.append(2)
                else:
                    sterilities.append(0)
        self._dataset['Sterility'] = sterilities
        self.remove_features('SexuponOutcome')

    """
    The features we extract are the following:
        * Day: integer from 1 to 31 depending on the month
        * Month: integer from 1 to 12
        * Year: integer from 2013 to 2016
        * Weekday: integer from 0 to 6 which represent Sunday to Saturday
        * DateInDays: Number of days from the oldest date of the dataset
        * Hour: integer from 0 to 23 where 0 = midnight
        * Time: The time represented by the equation 60h + m where h is the hours and m the minutes.
    """
    def extract_features_from_datetime(self):
        date_time_list = self._dataset['DateTime'].values.tolist()
        date_time_list = [datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S') for dateTime in date_time_list]

        min_date_time = min(date_time_list)
        self._dataset['Year'] = [date_time.year for date_time in date_time_list]
        self._dataset['Month'] = [date_time.month for date_time in date_time_list]
        self._dataset['Day'] = [date_time.day for date_time in date_time_list]
        self._dataset['Weekday'] = [date_time.weekday() for date_time in date_time_list]
        self._dataset['DateInDays'] = [(date_time - min_date_time).days for date_time in date_time_list]

        self._dataset['Hour'] = [dateTime.hour for dateTime in date_time_list]
        self._dataset['Time'] = [dateTime.hour*60 + dateTime.minute for dateTime in date_time_list]

        self.remove_features('DateTime')

    # If we find a slash `/` character which we define as a `separator`, then we have 2 colors.
    # If we find `Tricolor`, then this means that we have 3 colors.
    def extract_number_of_colors(self):
        colors = self._dataset['Color'].values.tolist()
        self._dataset['NumberOfColors'] = [color.count('/') + 1 for color in colors]
        self.remove_features('Color')

    # We extract this information from the `Breed` feature and add a new feature `BreedType`
    # where all purebred animals are identified with the value 0.
    # The mixed breed are identified with the value 2 and crossed breed with value 1.
    def extract_breed_types(self):
        breed_list = self._dataset['Breed'].values.tolist()

        breed_type_list = []
        for breed in breed_list:
            if ' Mix' in breed:
                breed_type_list.append(2)
            elif '/' in breed:
                breed_type_list.append(1)
            else:
                breed_type_list.append(0)
        self._dataset['BreedType'] = breed_type_list
        self.extract_special_breeds()
        self.remove_features('Breed')

    # Special cases with Pit Bull, Shih Tzu and Pug are considered since they are less adopted than the others.
    def extract_special_breeds(self):
        breed_list = self._dataset['Breed'].values.tolist()

        breed_specials = []
        for breed in breed_list:
            if 'Pit Bull' in breed:
                breed_specials.append(1)
            elif 'Shih Tzu' in breed:
                breed_specials.append(2)
            elif 'Pug' in breed:
                breed_specials.append(3)
            else:
                breed_specials.append(0)
        self._dataset['SpecialBreed'] = breed_specials

    # Get the unique outcomes from the OutcomeType feature.
    def get_unique_outcomes(self):
        outcomes = self._dataset['OutcomeType'].values.tolist()

        return sorted(list(set(outcomes)))

    # Convert each outcome to an integer (e.g. Adoption = 0, Transfer = 4).
    def convert_outcomes_to_integers(self):
        outcome_list = self.get_unique_outcomes()
        outcome_types = self._dataset['OutcomeType'].values.tolist()

        for i, outcome in enumerate(outcome_list):
            for j, outcome_type in enumerate(outcome_types):
                if outcome == outcome_type:
                    outcome_types[j] = i
        self._dataset['OutcomeType'] = outcome_types
