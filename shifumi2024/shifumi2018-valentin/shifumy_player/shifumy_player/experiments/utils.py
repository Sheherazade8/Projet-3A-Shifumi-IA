# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import matplotlib.pyplot as plt
import numpy as np


def plot_rps(score, title=None, filename=None):
    x_values = np.arange(1, score.size+1)

    plt.figure()
    plt.subplot(211)
    plt.plot(x_values, np.cumsum(score))
    plt.plot(x_values, x_values, ':k')
    plt.ylabel('Score')
    plt.xlabel('#Round')
    if title is not None:
        plt.title(title)
    plt.grid()

    plt.subplot(212)
    plt.plot(x_values,
             score,
             label='Individual')
    for n in [10, 100]:
        y = np.convolve(np.ones(n)/n, score)
        plt.plot(x_values[n-1:],
                 y[n-1:-n+1],
                 label='Average, last {} rounds'.format(n))
    plt.plot(x_values,
             np.cumsum(score) / x_values,
             label='Overall average score')
    plt.xlabel('#Round')
    plt.legend()
    plt.grid()

    if filename is not None:
        plt.savefig(filename)
