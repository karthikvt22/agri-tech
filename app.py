import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt

# --- Function 1: Tomato Price Predictor with Real Data ---
def tomato_price_predictor():
    st.header("🍅 Tomato Price Predictor")
    st.write("Select a future date to predict the expected tomato price.")

    # User-selected date
    user_date = st.date_input("Pick a future date", pd.to_datetime("2024-12-01"))

    # Load your market data (this can be your CSV data)
    data = {
        'Market': ['Arakalgud', 'Bagepalli', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        'Arrival Date': ['03/04/2021', '01/04/2021', '02/04/2021', '04/04/2021', '05/04/2021', '06/04/2021', '07/04/2021', '08/04/2021', '09/04/2021', '10/04/2021', '11/04/2021', '12/04/2021', '13/04/2021', '14/04/2021', '15/04/2021', '16/04/2021', '17/04/2021', '18/04/2021', '19/04/2021', '20/04/2021', '21/04/2021', '22/04/2021', '23/04/2021'],
        'Modal Price(Rs./Quintal)': [2000, 350, 350, 300, 400, 360, 350, 320, 300, 330, 300, 300, 300, 320, 300, 320, 360, 350, 360, 300, 325, 310, 400]
    }
    df = pd.DataFrame(data)
    
    # Preprocess data
    df['Arrival Date'] = pd.to_datetime(df['Arrival Date'], format='%d/%m/%Y')
    df = df[['Arrival Date', 'Modal Price(Rs./Quintal)']]
    df.columns = ['ds', 'y']  # Prophet expects columns to be named 'ds' and 'y'
    
    # Train Prophet model
    model = Prophet()
    model.fit(df)

    # Predict future
    future = model.make_future_dataframe(periods=365)  # Predict for 1 year into the future
    forecast = model.predict(future)

    # Find prediction for user date
    selected = forecast[forecast['ds'] == pd.to_datetime(user_date)]
    if not selected.empty:
        predicted_price = selected['yhat'].values[0]
        st.success(f"📈 Predicted Tomato Price on {user_date}: ₹{predicted_price:.2f} per quintal")
    else:
        st.warning("⚠️ Please select a date within the available range of data.")

    # Plot
    st.subheader("📊 Price Forecast Graph")
    fig = plt.figure(figsize=(10, 6))
    plt.plot(forecast['ds'], forecast['yhat'], label='Predicted Price')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3, label='Confidence Interval')
    plt.xlabel("Date")
    plt.ylabel("Price (INR/quintal)")
    plt.title("Tomato Price Forecast")
    plt.legend()
    st.pyplot(fig)

# --- Function 2: Crop Health Assessor ---
def crop_health_assessor():
    st.header("🌿 Crop Health & Growth Stage Assessor")
    st.write("Enter NPK values and crop age to assess current health status.")

    # Inputs
    n = st.number_input("Nitrogen (N)", 0, 300, 150)
    p = st.number_input("Phosphorus (P)", 0, 300, 100)
    k = st.number_input("Potassium (K)", 0, 300, 200)
    crop_age = st.number_input("Crop Age (in days)", 1, 200, 50)

    # Growth stage determination based on crop age
    if crop_age <= 30:
        stage = "Seedling"
    elif crop_age <= 60:
        stage = "Vegetative"
    elif crop_age <= 90:
        stage = "Flowering"
    elif crop_age <= 120:
        stage = "Fruiting"
    else:
        stage = "Maturity"

    # Recommended NPK by stage
    norms = {
        "Seedling": {"N": (50, 100), "P": (30, 60), "K": (100, 150)},
        "Vegetative": {"N": (100, 150), "P": (50, 90), "K": (150, 200)},
        "Flowering": {"N": (120, 170), "P": (70, 110), "K": (180, 230)},
        "Fruiting": {"N": (130, 180), "P": (80, 120), "K": (200, 250)},
        "Maturity": {"N": (100, 150), "P": (60, 90), "K": (150, 200)}
    }

    # Assess the crop health based on NPK values and growth stage
    ideal = norms[stage]
    def assess(value, ideal_range):
        if ideal_range[0] <= value <= ideal_range[1]:
            return "✅ Optimal"
        elif value < ideal_range[0]:
            return "🔻 Low"
        else:
            return "🔺 High"

    # Output crop health assessment
    st.subheader("📋 Assessment")
    st.write(f"**Growth Stage**: {stage}")
    st.write(f"- Nitrogen: {assess(n, ideal['N'])} (Recommended: {ideal['N'][0]}–{ideal['N'][1]})")
    st.write(f"- Phosphorus: {assess(p, ideal['P'])} (Recommended: {ideal['P'][0]}–{ideal['P'][1]})")
    st.write(f"- Potassium: {assess(k, ideal['K'])} (Recommended: {ideal['K'][0]}–{ideal['K'][1]})")

    # Final verdict
    if all(assess(val, ideal[ele]) == "✅ Optimal" for val, ele in zip([n, p, k], ['N', 'P', 'K'])):
        st.success("✅ Your crop is in good health! Keep it up!")
    else:
        st.warning("⚠️ Your crop needs nutrient adjustment.")

# --- Main App Layout ---
def main():
    st.title("🌾 Smart Agriculture Assistant")
    st.sidebar.title("🔍 Choose Feature")
    app_mode = st.sidebar.radio("Select Option", ["Tomato Price Predictor", "Crop Health Assessor"])

    if app_mode == "Tomato Price Predictor":
        tomato_price_predictor()
    elif app_mode == "Crop Health Assessor":
        crop_health_assessor()

if __name__ == "__main__":
    main()
