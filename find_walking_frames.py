import os
import re

import pandas as pd
import numpy as np
def main():
    directory = 'data/'
    test_subject_num = '10'
    files_with_walk(test_subject_num, directory)

def files_with_walk(test_subject_num, directory):
    test_subject_num = test_subject_num.zfill(2)
    for filename in os.listdir(directory):
        pattern = f'{test_subject_num}_.+txt$'
        if re.search(pattern, filename):
            with open(directory+filename) as f:
                    # This won't return all filenames, only the first.
                    return walking_data_frames(directory,filename)           
        else:
            continue

        
def walking_data_frames(directory, filename):
    pass

if __name__ == '__main__':
    main()