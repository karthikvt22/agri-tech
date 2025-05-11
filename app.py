import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="🍅 Tomato AI Assistant", layout="centered")
st.title("🌾 Tomato AI-Powered Dashboard")

# -------- Mode Selector --------
mode = st.sidebar.radio("Choose Mode", ["📈 Tomato Price Prediction", "🌿 Crop Health Assessment"])

# -------- Price Prediction --------
if mode == "📈 Tomato Price Prediction":
    st.header("📈 Tomato Price Prediction Tool")

    arrival = st.slider("Tomato Arrivals (Tonnes)", 10, 300, 100)
    day = st.slider("Day of Month", 1, 31, date.today().day)
    month = st.slider("Month", 1, 12, date.today().month)

    # Dummy model
    predicted_price = 5000 - (10 * arrival) + (20 * month) + np.random.randint(-100, 100)
    st.success(f"Predicted Price: ₹{int(predicted_price)} per quintal")

    # Graph: Price vs Arrival
    st.subheader("📊 Price vs Arrival Trend (Simulated)")
    arrivals = np.arange(10, 310, 10)
    prices = 5000 - 10 * arrivals + 20 * month
    plt.figure(figsize=(8, 4))
    plt.plot(arrivals, prices, marker='o', color='tomato')
    plt.xlabel("Arrivals (Tonnes)")
    plt.ylabel("Price (₹/quintal)")
    plt.title("Impact of Arrivals on Tomato Price")
    st.pyplot(plt)

# -------- Crop Health --------
else:
    st.header("🌿 Crop Health Assessment Tool")

    N = st.number_input("🌿 Nitrogen (N)", 0, 300, 100)
    P = st.number_input("🌸 Phosphorus (P)", 0, 300, 80)
    K = st.number_input("🍂 Potassium (K)", 0, 300, 150)
    age = st.number_input("⏳ Crop Age (in days)", 0, 200, 20)

    # Determine growth stage
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

    # Health Report
    st.subheader("📋 Health Assessment")
    st.markdown(f"🌵 **Growth Stage:** {stage}")
    st.markdown(f"- **Nitrogen (N):** {n_status} {n_range}")
    st.markdown(f"- **Phosphorus (P):** {p_status} {p_range}")
    st.markdown(f"- **Potassium (K):** {k_status} {k_range}")

    # NPK Bar Chart
    st.subheader("📊 NPK Level Visualization")
    nutrients = ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']
    values = [N, P, K]
    ideal_min = [50, 30, 100]
    ideal_max = [100, 60, 150]

    df = pd.DataFrame({
        'Nutrient': nutrients,
        'Current Value': values,
        'Ideal Min': ideal_min,
        'Ideal Max': ideal_max
    })

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df['Nutrient'], df['Current Value'], label='Current', color='mediumseagreen')
    ax.plot(df['Nutrient'], df['Ideal Min'], 'r--', label='Ideal Min')
    ax.plot(df['Nutrient'], df['Ideal Max'], 'g--', label='Ideal Max')
    ax.set_ylabel("Value")
    ax.set_title("NPK Nutrient Comparison")
    ax.legend()
    st.pyplot(fig)
