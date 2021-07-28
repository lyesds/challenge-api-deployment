# import
import tabulate
from joblib import load
from preprocessing.cleaning_data import preprocess


def predict():
    estim = load('model/model.joblib')
    ds = preprocess('input')
    predicted_price = round(estim.predict(ds)[0] / 1e3, 0) * 1e3  # the price will be a multiple of 1000€

    return predicted_price


print(predict())