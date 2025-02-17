import numpy
import os
import pandas
import seaborn

from matplotlib import pyplot
from requests import get
from scipy.io import arff


def main():
    training_file = arff.loadarff("nsl-kdd/full-train.arff")
    data_frame = pandas.DataFrame(training_file[0]).select_dtypes(
        [object]).stack().str.decode('utf-8').unstack()

    print(data_frame.head())


if __name__ == '__main__':
    main()
