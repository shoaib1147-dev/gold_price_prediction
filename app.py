import streamlit as st
import pandas as pd
import numpy as np
import joblib 

# Load your trained Linear Regression model
model = joblib.load('Linear_model_of_goldprice.pkl')
volume_scaler=joblib.load('volume_scaler.pkl')

st.set_page_config(page_title="Gold Price Predictor", layout="centered")
st.title("Gold Price Prediction(BTC) App")
st.markdown("Enter the required details below. Some fields accept gold price in USD, and will be converted to BTC for prediction.")

# --- BTC to USD conversion rate (this should be updated regularly or via API in real app)
st.subheader("BTC to USD Rate")
btc_usd_rate = st.number_input("Current BTC to USD rate:", value=65000.0)

st.subheader("Enter Gold Prices (in USD or BTC)")

# --- User inputs
priceOpen_usd = st.number_input("Gold Current Open Price (USD):", value=3300)
priceOpen_btc = priceOpen_usd / btc_usd_rate

priceHigh_usd = st.number_input("Gold Current High Price (USD):", value=3300)
priceHigh_btc = priceHigh_usd / btc_usd_rate

priceLow_usd = st.number_input("Gold Current Low  Price (USD):", value=3300)
priceLow_btc = priceLow_usd / btc_usd_rate

volume = st.number_input("Trading Volume:", format="%.2f")

st.subheader("Date & Time Details")
year = st.selectbox("Year", [2023, 2024, 2025])
month = st.slider("Month", 1, 12)
timeopnen_day = st.slider("Open Day", 1, 31)
timeopen_hour = st.slider("Open Hour", 0, 23)
timeHigh_day = st.slider("High Day", 1, 31)
timeHigh_hour = st.slider("High Hour", 0, 23)
timeClose_day = st.slider("Close Day", 1, 31)
timeClose_hour = st.slider("Close Hour", 0, 23)
timeLow_day = st.slider("Low Day", 1, 31)
timeLow_hour = st.slider("Low Hour", 0, 23)

# --- Predict button
if st.button("Predict Gold Price"):
    try:
        volume_scaled=volume_scaler.transform([[volume]])[0][0]
        input_data = pd.DataFrame({
        'priceOpen': [priceOpen_btc],
        'priceHigh': [priceHigh_btc],
        'priceLow': [priceLow_btc],
        'volume': [volume],
        'volume_scaled':[volume_scaled],
        # Skip volume_scaled, assuming model was trained with original volume and not scaled one
        'year': [year],
        'month': [month],
        'timeopnen_day': [timeopnen_day],
        'timeopen_hour': [timeopen_hour],
     
        'timeHigh_day': [timeHigh_day],
        'timeHigh_hour': [timeHigh_hour],

        'timeClose_day': [timeClose_day],
        'timeClose_hour': [timeClose_hour],

        'timeLow_day': [timeLow_day],
        'timeLow_hour': [timeLow_hour],
        })

    # Predict
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted Target Value: {prediction:.8f} BTC")
    except Exception as e:
        st.error(f"Error making prediction :{e}")