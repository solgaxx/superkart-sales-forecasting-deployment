
# import necessary libraries
import numpy as np
import pandas as pd
import joblib  # to load the serialized model
from flask import Flask, request, jsonify  # to create the Flask API

# initialize a Flask instance (API) for the project
superkart_api = Flask("SuperKart")

# load the trained model
model = joblib.load("xgb_tuned.joblib")

# define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart App"

# define an endpoint to predict sales for a single product
@superkart_api.post('/v1/predict')
def predict_sales():
    # get JSON data from the request
    data = request.get_json()

    # extract relevant features from the input data
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Product_Id_char': data['Product_Id_char'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category']
    }

    # convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # return the prediction as a JSON response
    return jsonify({'Predicted_Sales': prediction})

# define an endpoint to predict sales for a batch of products
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    # get the uploaded CSV file from the request
    file = request.files['file']

    # read the file into a DataFrame
    input_data = pd.read_csv(file)

    # make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # create an output mapping row index to predicted sales
    return jsonify({
        "predictions": [
            {"row": i, "predicted_sales": round(pred, 2)}
            for i, pred in enumerate(predictions)
        ]
    })


# run the Flask web server in debug mode
if __name__ == '__main__':
  superkart_api.run(debug=True)
