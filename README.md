# Gait Classifier #
Experiment with using topological data analysis techniques to construct a classifier for walking data taken from an accelerometer strapped to the thigh of a subject. The goal is to explore features of the data which can be used to determine if a device has been stolen and is being carried in the pocket of another person. See [Identifying People from Gait Pattern with Accelerometers](/References/VTT%20Identifying%20People%20by%20Gait.pdf) for more information about this specifice use case.

Used the HuGaDb Dataset from the [HuGaDB repository](https://github.com/romanchereshnev/HuGaDB)

I used the persistence toolkit from the [Giotto-TDA repository](https://github.com/giotto-ai/giotto-tda) and a decision tree classifier to determine if the persistence entropy is sufficient for classifying whether an individual has someone else's phone in their pocket.

A decision tree classifier implemented in [HGDB_classifcation.ipynb](/HGDB_classification.ipynb) was ~95% accurate in determining if an individual's signal did not match Subject 1's.

## To do: ##
- Currently I am only using the z-accelration sensor from the dataset (measuring the ''back and forth'' acceleration of the leg). In order to make this more robust to phones stored in other orientations (such as upside-down in the pocket), we need to implement some kind of PCA to use the x, y, and z accelerations and extract the principal components. This will then be more robust.




