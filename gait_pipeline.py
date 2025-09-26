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