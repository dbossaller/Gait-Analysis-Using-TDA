# Gait Classifier #
Experiment with using topological data analysis techniques to construct a predictor for walking data.

Used the HuGaDb Dataset from the [HuGaDB repository](https://github.com/romanchereshnev/HuGaDB)

I used the persistence toolkit from the [Giotto-TDA repository](https://github.com/giotto-ai/giotto-tda) and a decision tree classifier to classify subjects based on characteristics in their walk.

### Disclaimer: ### 

I think that there is a possibility that I'm overfitting the data by using a decision tree which is significantly deeper than $\log_2(18) \sim 4.2$. 

I also used the entropy calculations of the persistence diagram as a variable in the classification; I'm not sure how effective this is.
