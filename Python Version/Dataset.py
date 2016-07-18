#!/usr/bin/python3

import pandas
import pathlib
from datetime import datetime
from BarChartPlot import *


class Dataset:
    _dataset = []

    def get(self):
        return self._dataset

    # Load a dataset from a CSV file and replace the values in STRINGS_AS_NAN by NaN in the entire dataset.
    def load(self, filename):
        if pathlib.Path(filename).is_file():
            self._dataset = pandas.read_csv(filename, na_values='', parse_dates=True, delimiter=',')
        else:
            print('File' + filename + 'not found!')

    # Replace all NaN values by 0.
    #def ReplaceNaNByZeros(self):
    #    self._dataset['AgeuponOutcome'].replace("1 Weeks", "1 Week")

    # Remove features (columns) specified from the dataset.
    def removeFeatures(self, features):
        self._dataset = self._dataset.drop(features, axis=1)

    # Plot all needed Bar charts.
    def explore(self):
        barChart = BarChartPlot(self._dataset)
        barChart.ageByOutcomePlot()

    # We transform the feature AgeuponOutcome to integer values. For example, the age should be counted in days.
    # Thus, 2 years is replaced by the value 2 * 365 = 730. For months, the formula is age * 30.
    # For weeks, the formula is age * 7. For years, the formula is age * 365.
    def convertAgeToInteger(self):
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
        self.removeFeatures('AgeuponOutcome')

    # The feature Name is transformed to a boolean value where the value is 0 when the animal has no name and 1 otherwise.
    def convertNameToBool(self):
        self._dataset['IsNamed'] = pandas.isnull(self._dataset['Name']).astype(int)
        self.removeFeatures('Name')

    # We replace the possible values of the AnimalType feature by 0 = Dog and 1 = Cat.
    def convertAnimalTypeToBool(self):
        self._dataset['AnimalType'] = (self._dataset['AnimalType'] == 'Cat').astype(int)

    # We replace the feature SexuponOutcome by Sterility where Unknown = 0, Intact = 1 and Sterile = 2.
    def extractSterilityAsInteger(self):
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
        self.removeFeatures('SexuponOutcome')

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
    def extractFeaturesFromDateTime(self):
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

        self.removeFeatures('DateTime')

    # TODO
    def extractNumberOfColors(self):
        self.removeFeatures('Color')
        self.removeFeatures('Breed')

    # Get the unique outcomes from the OutcomeType feature.
    def getUniqueOutcomeTypes(self):
        outcomes = self._dataset['OutcomeType'].values.tolist()

        return sorted(list(set(outcomes)))

    #
    def convertOutcomeToInteger(self):
        outcome_list = self.getUniqueOutcomeTypes()
        outcome_types = self._dataset['OutcomeType'].values.tolist()

        for i, outcome in enumerate(outcome_list):
            for j, outcome_type in enumerate(outcome_types):
                if outcome == outcome_type:
                    outcome_types[j] = i
        self._dataset['OutcomeType'] = outcome_types
