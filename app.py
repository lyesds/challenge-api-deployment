import os
from flask import Flask, request, jsonify
from joblib import load
from preprocessing.cleaning_data import preprocess

app = Flask(__name__)

@app.route('/')
def alive():
    return 'alive'

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return """
        <p>Welcome to /predict webpage :)</p>
        <p>This page accepts a POST request allowing you to send some data describing a real estate property
        (location, number of rooms, area, kitchen equipped,...) that will be processed with a machine learning model in order to send you
        back an estimate of its price in euros.</p>
        <p>Please see below for the input data to submit.</p>
        <p>Enjoy!</p>
        
        <code style='color: red;'>Important: data sent to this POST request must be in 
        <a href="https://en.wikipedia.org/wiki/JSON">JSON</a> format with 
        <a href=”https://raw.githubusercontent.com/lyesds/challenge-api-deployment/main/data/input_format.txt”>
        this specific format</a>.
        ALL fields are required, if you don't know the value for a numerical field, please put 0 (zero).</code>
        """
    elif request.method == 'POST':
        inputdict = request.get_json()
        if inputdict:
            estim = load('model/model.joblib')
            ds = preprocess(input_dict=inputdict)
            predicted_price = round(estim.predict(ds)[0] / 1e3, 0) * 1e3  # the price will be a multiple of 1000€
            #print(inputdict)
            return jsonify({
                "prediction": predicted_price,
                "currency": 'euros',
                # Add this option to distinct the POST request
                "METHOD": "POST"
            })

if __name__ == '__main__':
    # You want to put the value of the env variable PORT if it exist (some services only open specifiques ports)
    port = int(os.environ.get('PORT', 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port)
