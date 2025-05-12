import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="🍅 Tomato AI Assistant", layout="centered")
st.title("🍅 Tomato AI-Powered Dashboard")

# -------- Mode Selector --------
mode = st.sidebar.radio("Choose Mode", ["📈 Tomato Price Prediction", "🌿 Tomato Crop Health"])

# -------- Tomato Price Prediction --------
if mode == "📈 Tomato Price Prediction":
    st.header("📈 Tomato Price Prediction Tool (India-based)")

    with st.form("price_form"):
        arrival = st.slider("Tomato Arrivals (Tonnes)", 10, 300, 100)
        selected_date = st.date_input("📅 Select Date", date.today())
        submit = st.form_submit_button("🔍 Predict Price")

    if submit:
        day = selected_date.day
        month = selected_date.month

        with st.spinner("🧮 Calculating best price..."):
            predicted_price = 5000 - (10 * arrival) + (25 * month) + np.random.randint(-100, 100)
            st.success(f"🧮 Predicted Market Price: ₹{int(predicted_price)} per quintal")

            # Graph: Price vs Arrival
            st.subheader("📊 Simulated Price Trend")
            arrivals = np.arange(10, 310, 10)
            prices = 5000 - 10 * arrivals + 25 * month
            plt.figure(figsize=(8, 4))
            plt.plot(arrivals, prices, marker='o', color='tomato')
            plt.xlabel("Arrivals (Tonnes)")
            plt.ylabel("Price (₹/quintal)")
            plt.title("Effect of Arrival Volume on Tomato Price")
            st.pyplot(plt)

# -------- Tomato Crop Health Assessment --------
else:
    st.header("🌿 Tomato Crop Health Analysis")

    # NPK input ranges specific to tomatoes
    N = st.number_input("🌿 Nitrogen (N) in kg/ha", 0, 300, 100)
    P = st.number_input("🌸 Phosphorus (P) in kg/ha", 0, 300, 60)
    K = st.number_input("🍂 Potassium (K) in kg/ha", 0, 300, 120)
    age = st.number_input("⏳ Tomato Crop Age (days)", 0, 200, 40)

    # Tomato growth stages
    if age < 30:
        stage = "🍃 Transplant to Vegetative"
        ideal_ranges = {"N": (80, 120), "P": (50, 70), "K": (80, 100)}
    elif age < 60:
        stage = "🌿 Vegetative to Flowering"
        ideal_ranges = {"N": (100, 140), "P": (60, 80), "K": (100, 130)}
    elif age < 90:
        stage = "🌸 Flowering to Fruiting"
        ideal_ranges = {"N": (80, 120), "P": (60, 80), "K": (130, 160)}
    else:
        stage = "🍅 Maturity & Harvest"
        ideal_ranges = {"N": (60, 100), "P": (50, 70), "K": (120, 150)}

    def assess(val, min_val, max_val):
        if min_val <= val <= max_val:
            return "✅ Optimal", f"(Ideal: {min_val}–{max_val})"
        elif val < min_val:
            return "🔻 Low", f"(Ideal: {min_val}–{max_val})"
        else:
            return "🔺 High", f"(Ideal: {min_val}–{max_val})"

    n_status, n_range = assess(N, *ideal_ranges["N"])
    p_status, p_range = assess(P, *ideal_ranges["P"])
    k_status, k_range = assess(K, *ideal_ranges["K"])

    # Health Report
    st.subheader("🩺 Tomato Health Assessment")
    st.markdown(f"🕒 **Growth Stage:** {stage}")
    st.markdown(f"- **Nitrogen (N):** {n_status} {n_range}")
    st.markdown(f"- **Phosphorus (P):** {p_status} {p_range}")
    st.markdown(f"- **Potassium (K):** {k_status} {k_range}")

    # Graph - NPK levels
    st.subheader("📊 Nutrient Levels vs Ideal Ranges")
    nutrients = ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']
    values = [N, P, K]
    ideal_min = [ideal_ranges["N"][0], ideal_ranges["P"][0], ideal_ranges["K"][0]]
    ideal_max = [ideal_ranges["N"][1], ideal_ranges["P"][1], ideal_ranges["K"][1]]

    df = pd.DataFrame({
        'Nutrient': nutrients,
        'Current': values,
        'Ideal Min': ideal_min,
        'Ideal Max': ideal_max
    })

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df['Nutrient'], df['Current'], label='Current', color='mediumseagreen')
    ax.plot(df['Nutrient'], df['Ideal Min'], 'r--', label='Ideal Min')
    ax.plot(df['Nutrient'], df['Ideal Max'], 'g--', label='Ideal Max')
    ax.set_ylabel("kg/ha")
    ax.set_title("NPK Analysis for Tomato")
    ax.legend()
    st.pyplot(fig)
