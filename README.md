# Gait Classifier #
Experiment with using topological data analysis techniques to construct a predictor for walking data.

Used the HuGaDb Dataset from the [HuGaDB repository](https://github.com/romanchereshnev/HuGaDB)

I used the persistence toolkit from the [Giotto-TDA repository](https://github.com/giotto-ai/giotto-tda) and a decision tree classifier to classify subjects based on characteristics in their walk.

Disclaimer: I think that there is a possibility of overfitting the data using the decision tree. I also used the entropy calculations of the persistence diagram as a variable in the classification; I'm not sure how effective this is.
