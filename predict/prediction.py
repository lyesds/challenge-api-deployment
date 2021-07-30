from joblib import load
from preprocessing.cleaning_data import preprocess


inputdict = {
  "0": {
    "location": 1050,
    "type": "APARTMENT",
    "room_number": 1,
    "area": 50,
    "kitchen_equipped": 0,
    "furnished": 0,
    "fireplace": 0,
    "terrace": 0,
    "terrace_area": 0,
    "garden": 0,
    "garden_area": 0,
    "land_surface": 0,
    "facade_count": 2,
    "swimming_pool": 0,
    "building_condition": "GOOD"
  }
}


def predict():
    estim = load('model/model.joblib')
    ds = preprocess(input_dict=inputdict)
    predicted_price = round(estim.predict(ds)[0] / 1e3, 0) * 1e3  # the price will be a multiple of 1000€

    return predicted_price


'''
print(predict())
'''
