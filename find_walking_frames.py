import os
import re

import pandas as pd

'''
Script to extract the walking frames from each subject. The full dataset contains accelerometer data for various activities. 
'''
def main():
    directory = 'data/'
    test_subject_num = '2'
    print(find_walking_data(test_subject_num, directory))

def find_walking_data(test_subject_num, directory):
    test_subject_num = str(test_subject_num)
    walking_dict = {}
    test_subject_num = test_subject_num.zfill(2)
    for filename in os.listdir(directory):
        pattern = rf'_various_{test_subject_num}_.+txt$'
        if re.search(pattern, filename):
            if walking_dataframes(directory,filename):
                walking_dict[filename[-9:-4]] = walking_dataframes(directory, filename)
            else:
                continue
        else:
            continue
    return walking_dict

        
def walking_dataframes(directory, filename):
    df = pd.read_csv(directory+filename, sep = '\t', header = 3)
    with open(directory+filename, 'r') as file:
        firstline = file.readlines()[0]
        
    line1 = firstline.lstrip('#Activity\t').rstrip(' \n').split(' ')
    line1 = line1[0:-2]
    if 'walking' not in line1:
        return False
    else:
        walking_idx = df.loc[df['act'] == 1].index

        walking_idx_starts = [walking_idx[0]]
        walking_idx_ends = []
        for i in range(1, len(walking_idx)):
            if walking_idx[i] != walking_idx[i-1] + 1:
                walking_idx_starts.append(walking_idx[i])
                walking_idx_ends.append(walking_idx[i-1])
        walking_intervals = [(s,e) for (s,e) in zip(walking_idx_starts, walking_idx_ends)]
        walk_dfs = []
        for int in walking_intervals:
            walk_dfs.append(df.iloc[int[0]:int[1]])

    return walk_dfs
if __name__ == '__main__':
    main()