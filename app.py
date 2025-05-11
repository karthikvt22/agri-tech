import streamlit as st
import pandas as pd
import joblib
import datetime

# Load your trained price prediction model
model = joblib.load("tomato_price_model.pkl")

# Page configuration
st.set_page_config(page_title="Tomato Price & Crop Health", layout="centered")
st.title("🍅 Tomato Price Forecast & 🧪 Crop Health Check")

st.markdown("## 📈 Tomato Price Prediction")
st.markdown("Upload CSV with columns: `Arrivals (Tonnes)` and `Date`.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file, parse_dates=["Arrival Date"])
    data["Day"] = data["Arrival Date"].dt.day
    data["Month"] = data["Arrival Date"].dt.month

    if "Arrivals (Tonnes)" in data and "Day" in data and "Month" in data:
        X = data[["Arrivals (Tonnes)", "Day", "Month"]]
        prediction = model.predict(X)
        data["Predicted Modal Price (Rs./Quintal)"] = prediction
        st.write("### 🔍 Prediction Results", data)
    else:
        st.warning("Missing required columns: 'Arrivals (Tonnes)', 'Arrival Date'.")

st.markdown("---")
st.markdown("## 🌱 Crop Health Assessment")

# Inputs
N = st.number_input("🌿 Nitrogen (N)", 0, 500, 100)
P = st.number_input("🌸 Phosphorus (P)", 0, 500, 80)
K = st.number_input("🍂 Potassium (K)", 0, 500, 150)
age = st.number_input("⏳ Crop Age (in days)", 0, 150, 20)

# Determine growth stage
if age < 30:
    stage = "Seedling"
    ideal_N, ideal_P, ideal_K = (50, 100), (30, 60), (100, 150)
elif age < 60:
    stage = "Vegetative"
    ideal_N, ideal_P, ideal_K = (100, 150), (60, 80), (100, 200)
else:
    stage = "Flowering"
    ideal_N, ideal_P, ideal_K = (80, 120), (50, 70), (120, 180)

def assess(value, ideal_range):
    if value < ideal_range[0]:
        return "🔻 Low"
    elif value > ideal_range[1]:
        return "🔺 High"
    return "✅ Optimal"

st.markdown("### 🧾 Health Assessment")
st.markdown(f"**🌱 Growth Stage:** `{stage}`")
st.markdown(f"- **Nitrogen (N):** {assess(N, ideal_N)} (Ideal: {ideal_N[0]}–{ideal_N[1]})")
st.markdown(f"- **Phosphorus (P):** {assess(P, ideal_P)} (Ideal: {ideal_P[0]}–{ideal_P[1]})")
st.markdown(f"- **Potassium (K):** {assess(K, ideal_K)} (Ideal: {ideal_K[0]}–{ideal_K[1]})")
