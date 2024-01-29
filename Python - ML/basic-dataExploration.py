import pandas as pd
from sklearn.tree import DecisionTreeRegressor 
# save filepath to variable for easier access
melbourne_file_path = './melb_data.csv'
# read the data and store data in DataFrame titled melbourne_data
melbourne_data = pd.read_csv(melbourne_file_path) 
# print a summary of the data in Melbourne data
print(melbourne_data.describe())
# print a columns of the data in Melbourne data
print(melbourne_data.columns) 
# store the series of prices separately
y = melbourne_data.Price
# store the features separately
melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']
# store the features in X
X = melbourne_data[melbourne_features]
# print a summary of the data in X
print(X.describe())
# print the top few lines of the data in X
print(X.head())
# Define model. Specify a number for random_state to ensure same results each run
melbourne_model = DecisionTreeRegressor(random_state=1)
# Fit model
melbourne_model.fit(X, y)
print("Making predictions for the following 5 houses:")
print(X.head())
print("The predictions are")
print(melbourne_model.predict(X.head()))
print(melbourne_data.head())