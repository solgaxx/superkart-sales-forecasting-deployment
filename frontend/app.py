
import streamlit as st
import pandas as pd
import requests

# base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# create the page title
st.title("SuperKart System")
st.write(
    "Enter the product and store details below to predict the total sales."
)

# create input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
Product_Char = st.selectbox("Product ID Character", ["FD", "DR", "NC"])
Store_Age = st.number_input("Store Age (Years)", min_value=0, value=16)
Product_Type_Perishability = st.selectbox("Product Type Category", ["Perishable", "Non-Perishable"])

# create JSON payload
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Char": Product_Char,
    "Store_Age": Store_Age,
    "Product_Type_Perishability": Product_Type_Perishability
}

# Single Prediction
if st.button("Predict", type='primary'):

    response = requests.post(
        f"{BACKEND_URL}/v1/predict",
        json=product_data
    )

    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Predicted_Sales"]
        st.success(f"Predicted Product Store Sales Total: ₹{predicted_sales:.2f}")
    else:
        st.error("Unable to connect to the prediction API.")

# Batch Prediction
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict for Batch", type="primary"):

        response = requests.post(
            f"{BACKEND_URL}/v1/predictbatch",
            files={"file": uploaded_file}
        )

        if response.status_code == 200:
            results = response.json()

            st.success("Predictions completed successfully!")

            # extract prediction records from the API response
            predictions = results["predictions"]

            # convert predictions into a DataFrame
            df = pd.DataFrame(predictions)

            # display results
            st.dataframe(df, use_container_width=True)

        else:
            st.error("Unable to connect to the prediction API.")
