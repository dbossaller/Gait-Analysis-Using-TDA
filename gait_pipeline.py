from gtda.diagrams import PersistenceEntropy, Scaler
from gtda.homology import WeakAlphaPersistence
from gtda.metaestimators import CollectionTransformer
from gtda.pipeline import Pipeline
from gtda.time_series import TakensEmbedding
from sklearn.decomposition import PCA

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

    features = topological_transformer.fit_transform(signals)
    
    return features
