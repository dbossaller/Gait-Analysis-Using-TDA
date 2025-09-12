import random
import pandas as pd
import numpy as np

from pre_process import conv_acceleration
from pre_process import find_period_acf
from find_walking_frames import find_walking_data


def main():
    pass

'''
function to construct a dataset of walking examples for the 
given subject that will then be fed into the pipeline function'''

def make_sub_dataset(subject, directory, leg = 'right', location = 'thigh', num_periods = 4, sample_size = 50):
    sub_walks = find_walking_data(subject, directory)
    
    keys = sub_walks.keys()

    sensor_location = {'right': {'foot':'rf', 'shin':'rs', 'thigh':'rt'},
                       'left' : {'foot':'lf', 'shin':'ls', 'thigh':'lt'}}
    
    period = None

    signals = []
    while len(signals) < sample_size:
        sub_choice = random.choice(list(keys))
        
        length = len(sub_walks[sub_choice])
        
        df = sub_walks[sub_choice][random.randint(0, length-1)]

        df_accel = pd.DataFrame(None)

        for column in df.columns:
            if 'acc' in column:
                df_accel[column] = df[column].apply(conv_acceleration)
        
        sensor_placed_where = sensor_location[leg][location]
        
        df_accel_loc = df_accel[['acc_' + sensor_placed_where + '_x','acc_' + sensor_placed_where + '_y','acc_' + sensor_placed_where + '_z']]
        _ = df_accel_loc['acc_' + sensor_placed_where + '_z']
        num_rows = _.shape[0]

        period = find_period_acf(_, 150)

        num_strides = num_rows//period + 1

        if num_strides > num_periods:
            wind_start = random.randint(0, num_strides - num_periods)
            series = np.asarray(df_accel_loc[wind_start*period: wind_start*period + num_periods*period])
            signals.append(series)
    return signals


def construct_dataset(directory = 'data/', leg = 'right', location = 'thigh', num_periods = 4, sample_size=50):
    full_dataset = {}
    
    for sub_num in range(1,19):
        try:
            sub_dataset = make_sub_dataset(f'{sub_num}', directory, leg, location, num_periods, sample_size)
            full_dataset[sub_num] = sub_dataset
        except(ValueError):
            continue

    return full_dataset


if __name__ == '__main__':
    main() 