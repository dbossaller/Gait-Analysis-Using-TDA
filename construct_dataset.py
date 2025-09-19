import random
import pandas as pd
import json

from pre_process import conv_acceleration
from pre_process import find_period_acf
from find_walking_frames import find_walking_data


def main():
    make_n_json_datasets(5, leg = 'right', location = 'thigh', sample_size = 150)
    make_n_json_datasets(5, leg = 'left', location = 'thigh', sample_size = 150)

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
            series = df_accel_loc[wind_start*period: wind_start*period + num_periods*period]
            signals.append(series)
    return signals

'''
Constructs a dataset (if possible) for all subjects. This outputs a dictionary whose indices correspond to the subject number, and whose values are a list of pandas dataframes.

'''
def construct_dataset(directory = 'data/', leg = 'right', location = 'thigh', num_periods = 4, sample_size=50):
    full_dataset = {}
    
    for sub_num in range(1,19):
        try:
            sub_dataset = make_sub_dataset(f'{sub_num}', directory, leg, location, num_periods, sample_size)
            full_dataset[sub_num] = sub_dataset
        except(ValueError):
            continue
    return full_dataset

def dataset_to_json(dataset):
    keys = dataset.keys()
    dict_dataset = {}
    for key in keys:            
        sub_list = []
        for sample in dataset[key]:
            sub_list.append(sample.to_dict())
        dict_dataset[key] = sub_list
    
    return dict_dataset


def write_data_to_json(filename, data):
    json_dataset = dataset_to_json(data)
    with open(filename, 'w+') as fp:
        json.dump(json_dataset, fp, indent=2)

def read_data_json(filename):
    data = None
    with open(filename,'r') as dataset:
        data = json.load(dataset)
    return data

def samples_to_dataframes(dataset):
    keys  = dataset.keys()
    df_dataset = {}
    for key in keys:
        df_dataset[int(key)] = []
        for sample_no in range(len(dataset[key])):
            df_dataset[int(key)].append(pd.DataFrame(dataset[key][sample_no]))
    return df_dataset

def load_data_from_json(filename):
    dataset = read_data_json(filename)
    return samples_to_dataframes(dataset)

def make_n_json_datasets(n, save_folder = '/Datasets', directory = './data/', leg = 'right', location = 'thigh', num_periods = 4, sample_size=50):
    for i in range(n):
        filename = f'.{save_folder}/{leg}_{location}_{i}.json'
        dataset = construct_dataset(directory, leg, location, num_periods, sample_size)
        write_data_to_json(filename, dataset)

if __name__ == '__main__':
    main() 