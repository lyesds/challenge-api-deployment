from sklearn.ensemble import GradientBoostingRegressor
from joblib import dump
import pandas as pd


# Read the preprocessed data (without dummies for subtype)
# built during previous project (see https://github.com/Misterkadrix/challenge-regression)
ds_model = pd.read_csv('data/data_preprocessed.csv')
ds_model = ds_model.select_dtypes(exclude=['object'])

# Define the X feature and y
X = ds_model.drop(['price', 'garden_area', 'terrace_area', 'land_surface', 'facade_count'], axis=1)
y = ds_model['price']

# the model that should has a score of around 0.7
estim = GradientBoostingRegressor(n_estimators=100, max_depth=3, min_samples_split=2, learning_rate=0.1, loss='ls')
estim.fit(X, y)
print(estim.score(X, y))
dump(estim, 'model/model.joblib')

'''
X1 = X.iloc[7429:7430,:]
print(X1.to_markdown())
print(estim.predict(X1))
'''