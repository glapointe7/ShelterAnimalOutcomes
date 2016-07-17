#!/usr/bin/python3

import pandas
import pathlib
from BarChartPlot import *
from datetime import datetime


class Dataset:
    _dataset = []


    def Get(self):
        return self._dataset

    # Load a dataset from a CSV file and replace the values in STRINGS_AS_NAN by NaN in the entire dataset.
    def Load(self, filename):
        if(pathlib.Path(filename).is_file()):
            self._dataset = pandas.read_csv(filename, index_col = 0, na_values = "", parse_dates = True)
        else:
            print("File" + filename + "not found!")


    # Replace all NaN values by 0.
    #def ReplaceNaNByZeros(self):
    #    self._dataset[pandas.isnull(self._dataset)] = 0
    #    self._dataset['AgeuponOutcome'].replace("1 Weeks", "1 Week")

    # Get the number of rows of the dataset.
    def Size(self):
        return(len(self._dataset))

    # Remove features (columns) specified from the dataset.
    def RemoveFeatures(self, features):
        self._dataset = self._dataset.drop(features, axis = 1)

    # Plot all needed Bar charts.
    def Explore(self):
        barChart = BarChartPlot(self._dataset)
        barChart.AgeByOutcomePlot()

    # We transform the feature AgeuponOutcome to integer values. For example, the age should be counted in days.
    # Thus, 2 years is replaced by the value 2 * 365 = 730. For months, the formula is age * 30.
    # For weeks, the formula is age * 7. For years, the formula is age * 365.
    def ConvertAgeToInteger(self):
        ageList = self._dataset[['AgeuponOutcome']].values.tolist()
        ageList = [age[0] for age in ageList]

        ages = []
        for age in ageList:
            if pandas.isnull(age):
                ages.append(0)
            else:
                (ageInt, ageType) = age.split(' ')
                if 'year' in ageType:
                    ages.append(int(ageInt) * 365)
                if 'month' in ageType:
                    ages.append(int(ageInt) * 30)
                if 'week' in ageType:
                    ages.append(int(ageInt) * 7)
                if 'day' in ageType:
                    ages.append(int(ageInt))
        self._dataset['AgeInDays'] = ages
        self.RemoveFeatures('AgeuponOutcome')

    # The feature Name is transformed to a boolean value where the value is 0 when the animal has no name and 1 otherwise.
    def ConvertNameToBool(self):
        self._dataset['IsNamed'] = pandas.isnull(self._dataset['Name']).astype(int)
        self.RemoveFeatures('Name')

    # We replace the possible values of the AnimalType feature by 0 = Dog and 1 = Cat.
    def ConvertAnimalTypeToBool(self):
        self._dataset['AnimalType'] = (self._dataset['AnimalType'] == "Cat").astype(int)

        # We replace the feature SexuponOutcome by Sterility where Unknown = 0, Intact = 1 and Sterile = 2.
    def ExtractSterilityAsInteger(self):
        sexuponOutcome = self._dataset['SexuponOutcome'].values.tolist()

        sterilities = []
        for sex in sexuponOutcome:
            if pandas.isnull(sex):
                sterilities.append(0)
            else:
                if 'Unknown' in sex:
                    sterilities.append(0)
                if 'Intact' in sex:
                    sterilities.append(1)
                if any(sterilityType in sex for sterilityType in ['Spayed', 'Neutered']):
                    sterilities.append(2)
        self._dataset['Sterility'] = sterilities
        self.RemoveFeatures('SexuponOutcome')

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
    def ExtractFeaturesFromDateTime(self):
        dateTimeList = self._dataset['DateTime'].values.tolist()
        dateTimeList = [datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S") for dateTime in dateTimeList]

        minDateTime = min(dateTimeList)
        self._dataset['Year'] = [dateTime.year for dateTime in dateTimeList]
        self._dataset['Month'] = [dateTime.month for dateTime in dateTimeList]
        self._dataset['Day'] = [dateTime.day for dateTime in dateTimeList]
        self._dataset['Weekday'] = [dateTime.weekday() for dateTime in dateTimeList]
        self._dataset['DateInDays'] = [(dateTime - minDateTime).days for dateTime in dateTimeList]

        self._dataset['Hour'] = [dateTime.hour for dateTime in dateTimeList]
        self._dataset['Time'] = [dateTime.hour * 60 + dateTime.minute for dateTime in dateTimeList]

        self.RemoveFeatures('DateTime')

    #
    def ExtractNumberOfColors(self):
        self.RemoveFeatures('Color')
        self.RemoveFeatures('Breed')

    # Get the unique outcomes from the OutcomeType feature.
    def GetUniqueOutcomeTypes(self):
        outcomes = self._dataset['OutcomeType'].values.tolist()
        return sorted(list(set(outcomes)))
