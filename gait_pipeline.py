import pandas as pd
import numpy as np
import random

from gtda.diagrams import PersistenceEntropy, Scaler
from gtda.homology import WeakAlphaPersistence
from gtda.metaestimators import CollectionTransformer
from gtda.pipeline import Pipeline
from gtda.time_series import TakensEmbedding
from sklearn.decomposition import PCA

from pre_process import conv_acceleration, find_period_acf
from find_walking_frames import find_walking_data

def topological_transform(signals):
    embedding_dimension = 10
    embedding_time_delay = 5
    stride = 1

    embedder = TakensEmbedding(time_delay=embedding_time_delay,
                            dimension = embedding_dimension,
                            stride = stride)

    batch_pca = CollectionTransformer(PCA(n_components = 3), n_jobs = -1)

    persistence = WeakAlphaPersistence(homology_dimensions=[0,1], n_jobs = -1)

    scaling = Scaler()

    entropy = PersistenceEntropy(normalize = True, nan_fill_value=-10)


    steps = [
        ('embedder', embedder),
        ('pca', batch_pca),
        ('persistence', persistence),
        ('scaling', scaling),
        ('entropy', entropy)]

    topological_transformer = Pipeline(steps)

    H0_H1_entropies = topological_transformer.fit_transform(signals)
    
    return H0_H1_entropies

'''
function to construct a dataset of walking examples for the 
given subject that will then be fed into the pipeline function'''

def make_dataset(subject, directory, leg = 'right', location = 'thigh', num_periods = 4, sample_size = 50):
    sub_walks = find_walking_data(subject, directory)
    
    keys = sub_walks.keys()

    sensor_location = {'right': {'foot':'rf', 'shin':'rs', 'thigh':'rt'},
                       'left' : {'foot':'lf', 'shin':'ls', 'thigh':'lt'}}
    
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
        
        df_accel_loc = df_accel[['acc_' + sensor_placed_where + '_x',
                             'acc_' + sensor_placed_where + '_y',
                             'acc_' + sensor_placed_where + '_z']]

        num_rows = df_accel_loc.shape[0]
        
        period = find_period_acf(df_accel_loc, 150)

        num_strides = num_rows//period + 1

        if num_strides > num_periods:
            wind_start = random.randint(0, num_strides - num_periods)
            series = np.asarray(df_accel_loc[wind_start*period: wind_start*period + num_periods*period])
            signals.append(series)
    return signals