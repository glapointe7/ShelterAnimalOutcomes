#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn


class BarChartPlot:
    _dataset = []

    def __init__(self, dataset):
        plt.style.use('ggplot')
        seaborn.set(style="darkgrid")
        self._dataset = dataset.get()

    # Plot a bar chart stacked of the number of animals by age stacked by outcome.
    def plot_age_by_outcome(self):
        self._dataset['AgeuponOutcome'].replace('1 weeks', '1 week')
        age = self._dataset.groupby(['AgeuponOutcome', 'OutcomeType']).size().unstack(1)

        age_plot = age.plot(kind='bar', stacked=True, figsize=(12, 13))
        age_plot.set_title('Number of animals by Age and outcome')
        age_plot.set_xlabel('Age of animals')
        age_plot.set_ylabel('Number of animals')

        fig = age_plot.get_figure()
        fig.savefig('AgeByOutcome.png')

    # Plot the overall percentage of animals by outcome.
    def plot_outcome_percentages(self):
        outcome = self._dataset.groupby('OutcomeType').size() / len(self._dataset)
        print(outcome * 100)
        outcome_plot = outcome.plot(kind='bar', figsize=(12, 13))
        outcome_plot.set_title('Percentage of animals by outcome')
        outcome_plot.set_xlabel('Outcomes')
        outcome_plot.set_ylabel('Percentage of animals')
        vals = outcome_plot.get_yticks()
        outcome_plot.set_yticklabels(['{:3.0f}%'.format(x * 100) for x in vals])

        fig = outcome_plot.get_figure()
        fig.savefig('OutcomePercentage.png')

    # Plot the percentage and number of animals by outcome.
    def plot_outcome_percentages_per_animal_type(self):
        plt.figure(figsize=(12, 8))
        ax = seaborn.countplot(x='OutcomeType', hue='AnimalType', data=self._dataset)
        plt.title('Percentage of cats and dogs by outcome')
        plt.xlabel('Outcomes')

        # Make twin axis
        ax2 = ax.twinx()

        # Switch so count axis is on right, frequency on left
        ax2.yaxis.tick_left()
        ax2.yaxis.set_label_position('left')
        ax2.set_ylabel('Frequency [%]')
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position('right')
        ax.set_ylabel('Number of Animals')

        ncount = len(self._dataset)
        for p in ax.patches:
            x = p.get_bbox().get_points()[:, 0]
            y = p.get_bbox().get_points()[1, 1]
            ax.annotate('{:2.2f}%'.format(100. * y / ncount),
                        (x.mean(), y),
                        ha='center',
                        va='bottom')
        # Use a LinearLocator to ensure the correct number of ticks
        ax.yaxis.set_major_locator(ticker.LinearLocator(11))

        # Fix the frequency range to 0-100
        ax2.set_ylim(0, 100)
        ax.set_ylim(0, ncount)

        # And use a MultipleLocator to ensure a tick spacing of 10
        ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))
        plt.savefig('OutcomePercentageByAnimalType.png')