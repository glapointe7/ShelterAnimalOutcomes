#!/usr/bin/python3

import matplotlib.pyplot as plt


class BarChartPlot:
    _dataset = []

    def __init__(self, dataset):
        plt.style.use('ggplot')
        self._dataset = dataset


    def AgeByOutcomePlot(self):
        age = self._dataset.groupby(['AgeuponOutcome', 'OutcomeType']).size().unstack()
        agePlot = age.plot(kind = 'bar', stacked = True, figsize = (12, 13))
        agePlot.set_title("Number of animals by Age and outcome")
        agePlot.set_xlabel("Age of animals")
        agePlot.set_ylabel("Number of animals")

        fig = agePlot.get_figure()
        fig.savefig("AgeByOutcome.png")

