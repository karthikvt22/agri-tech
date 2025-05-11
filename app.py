import streamlit as st
import numpy as np
from datetime import date

st.set_page_config(page_title="Tomato AI Platform", layout="centered")

st.title("🍅 Tomato Crop Price & Health Analysis")

# ----- SECTION 1: Price Prediction -----
st.header("📈 Tomato Price Prediction")

arrival = st.slider("Arrivals (Tonnes)", 10, 300, 100)
day = st.slider("Day of Month", 1, 31, date.today().day)
month = st.slider("Month", 1, 12, date.today().month)

# Dummy regression equation: price = 5000 - 10*arrival + 20*month + noise
predicted_price = 5000 - (10 * arrival) + (20 * month) + np.random.randint(-100, 100)
st.success(f"Predicted Tomato Price: ₹{int(predicted_price)} per quintal")

# ----- SECTION 2: Crop Health Assessment -----
st.header("🌱 Crop Health Assessment")

N = st.number_input("🌿 Nitrogen (N)", 0, 300, 100)
P = st.number_input("🌸 Phosphorus (P)", 0, 300, 80)
K = st.number_input("🍂 Potassium (K)", 0, 300, 150)
age = st.number_input("⏳ Crop Age (in days)", 0, 200, 20)

# Determine stage
if age < 30:
    stage = "Seedling"
elif age < 60:
    stage = "Vegetative"
elif age < 90:
    stage = "Flowering"
else:
    stage = "Mature"

def assess(value, low, high):
    if low <= value <= high:
        return "✅ Optimal", f"(Ideal: {low}–{high})"
    elif value < low:
        return "🔻 Low", f"(Ideal: {low}–{high})"
    else:
        return "🔺 High", f"(Ideal: {low}–{high})"

n_status, n_range = assess(N, 50, 100)
p_status, p_range = assess(P, 30, 60)
k_status, k_range = assess(K, 100, 150)

st.subheader("📋 Health Assessment")
st.markdown(f"🌵 **Growth Stage:** {stage}")
st.markdown(f"- **Nitrogen (N):** {n_status} {n_range}")
st.markdown(f"- **Phosphorus (P):** {p_status} {p_range}")
st.markdown(f"- **Potassium (K):** {k_status} {k_range}")
