import pandas as pd
import numpy as np
from datetime import timedelta
from statsmodels.tsa.stattools import acf
from math import floor

"""
Given the data, read in as a dataframe, we'd like to isolate the acceleration columns and
and then rescale the acceleration according to the HuGaDB article.
"""


# Calculation to convert a number (in uint8 format) to m/s^2
def conv_acceleration(num):
    return 2 * num / 32768


# Function to take in a dataframe read from the HuGaDB and pull out the columns with the acceleration,
# and set the index to be time from the beginning of the dataframe
def pull_acceleration(dataframe):
    df_accel = pd.DataFrame(None)

    for column in dataframe.columns:
        if "acc" in column:
            df_accel[column] = dataframe[column].apply(conv_acceleration)

    delta = timedelta(seconds=1 / 56.35)

    df_accel["time"] = (dataframe.index - dataframe.index[0]) * delta

    df_accel.set_index("time", inplace=True)

    return df_accel


def find_period_acf(series, lags):
    autocorr = np.array(acf(series, nlags=lags))
    initial_value = floor(lags * 0.25)
    first_max = np.argmax(autocorr[initial_value:-1])
    return initial_value + first_max
