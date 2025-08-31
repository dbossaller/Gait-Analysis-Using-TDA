from gait_pipeline import make_dataset

def construct_dataset(number_of_datasets, path):
    directory = 'data/'

    for _ in range(number_of_datasets):
        full_dataset = {}

        for sub_num in range(1,19):
            try:
                sub_dataset = make_dataset(f'{sub_num}', directory, leg = 'right', 
                                           location = 'thigh', sample_size = 150)
                full_dataset[sub_num] = sub_dataset
            except(ValueError):
                continue
        