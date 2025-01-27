#pip install numpy
#pip install pandas
#pip install xlrd
#pip install sklearn


import pandas as pd
import os

from sklearn.metrics import mean_squared_error
from flask import Flask, render_template, url_for, redirect, request
from pandas.io.json import json_normalize
import pickle as pikl

global bike_model

app = Flask(__name__)

# Run or refresh model
def model():
    print('Model called')
    # if x == 1:
    #     OSdata = OSpd.read_excel(
    #         'basket_ball.xlsx')
    # else:
    #     OSdata = OSpd.read_excel(
    #         'basket_ball2.xlsx')

    # OSdataX = OSdata[['height_ft', 'weight_pd', 'successfieldgoals%', 'successfreethrows%']]
    # OSdataY = OSdata['avg_points']

    # Load pickle file and predict

    # global OSLM

    #OSLM = OSlm.LinearRegression()
    # global bbmodel
    bike_model = pikl.load(open(r'C:\Users\Noomit yagna\Desktop\N1\GSS_ML\ML28_Internship\BikeShare\model\bike_share_rf_model.P', 'rb'))
    #result = load_model.predict(x)
    # print(result)

    # OSLM.fit(OSdataX, OSdataY)
    # bbpred = OSLM.predict(OSdataX)
    # rmse = mean_squared_error(OSdataY, bbpred)
    # return OSLM, rmse
    return bike_model

# Predict from the model build
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    print('Some one called me')
    if request.method == 'POST':
        print('From if')
        input_values = request.form

    inputX = pd.DataFrame(json_normalize(input_values))
    print('Values from user are as below')
    print(inputX)
    input = inputX[['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'qtrs','windspeed']]
    # predval = OSLM.predict(input)
    bike_model = model()
    predval = bike_model.predict(input)

    input['predval'] = predval
    # input.columns = ['Height (feet)', 'Weight (pounds)', 'Field Success (%)', 'Free Success (%)', 'Predicted Avg Score']
    input.columns = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'qtrs', 'windspeed', 'Predcited Result']
    return render_template('predict.html', tables=[input.to_html()], titles=input.columns.values)


# Home page that renders for every web call
@app.route("/")
def home():
    print('Starting from here')
    return render_template("home.html")


if __name__ == "__main__":
    print('From main')
    port = int(os.environ.get('PORT', 9000))
    #global OSLM, Error
    global bike_model
    # OSLM, Error = model(1)
    app.run(host='localhost', port=port, debug=True)
    # app.run(debug=True)