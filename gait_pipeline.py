import numpy as np
import pandas as pd
from datetime import datetime

from gtda.diagrams import PersistenceEntropy, Scaler
from gtda.homology import VietorisRipsPersistence
from gtda.pipeline import Pipeline

def topological_transform(signals):
    persistence = VietorisRipsPersistence(homology_dimensions=(0,1,2), n_jobs = -1)

    scaling = Scaler()

    entropy = PersistenceEntropy(normalize = True, nan_fill_value=-10)


    steps = [
        ('persistence', persistence),
        ('scaling', scaling),
        ('entropy', entropy)]

    topological_transformer = Pipeline(steps)

    H0_H1_H2_entropies = topological_transformer.fit_transform(signals)
    
    return H0_H1_H2_entropies

def calculate_entropies(full_dataset):
    entropies = []
    for subject in full_dataset.keys():
        start_time = datetime.now()
        print(f'Calculating entropies for subject {subject}')
        for measurement in full_dataset[subject]:
            measurement = np.array(measurement)[None,:,:]
            H0, H1, H2 = topological_transform(measurement)[0]
            entropies.append([subject, H0, H1, H2])
        print(f'\tCompleted, took {(datetime.now()-start_time).total_seconds():.0f} seconds')
    return entropies

def make_entropy_dataframe(entropies):
    return pd.DataFrame(entropies, columns = ['subject', 'H0 Entropy', 'H1 Entropy', 'H2 Entropy'])

def entropy_dataframe(full_dataset):
    return make_entropy_dataframe(calculate_entropies(full_dataset))