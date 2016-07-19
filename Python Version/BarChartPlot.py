#!/usr/bin/python3

import matplotlib.pyplot as plt
from Dataset import Dataset


class BarChartPlot:
    _dataset = []

    def __init__(self, dataset):
        plt.style.use('ggplot')
        self._dataset = dataset.get()

    # Plot a bar chart stacked of the number of animals by age stacked by outcome.
    def plot_age_by_outcome(self):
        age = self._dataset.groupby(['AgeuponOutcome', 'OutcomeType']).size().unstack()
        age_plot = age.plot(kind='bar', stacked=True, figsize=(12, 13))
        age_plot.set_title('Number of animals by Age and outcome')
        age_plot.set_xlabel('Age of animals')
        age_plot.set_ylabel('Number of animals')

        fig = age_plot.get_figure()
        fig.savefig('AgeByOutcome.png')

