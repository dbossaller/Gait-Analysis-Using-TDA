from gait_pipeline import make_sub_dataset

def main():
    pass


def construct_dataset(directory = '\data', leg = 'right', location = 'thigh', num_periods = 4, sample_size=50):
    full_dataset = {}

    for sub_num in range(1,19):
        try:
            sub_dataset = make_sub_dataset(f'{sub_num}', directory, leg, location, num_periods=3, sample_size = 150)
            full_dataset[sub_num] = sub_dataset
        except(ValueError):
            continue

    return full_dataset


if __name__ == '__main__':
    main()