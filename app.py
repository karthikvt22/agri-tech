import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="🍅 Tomato AI Assistant", layout="centered")
st.markdown("<h1 style='text-align: center; color: tomato;'>🍅 Tomato AI Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
mode = st.sidebar.radio("🔘 Choose Mode", ["📈 Price Prediction", "🌿 Crop Health"])

# ------------------ PRICE PREDICTION ------------------ #
if mode == "📈 Price Prediction":
    st.subheader("🔮 Predict Tomato Market Price")
    st.markdown("Use AI to predict the tomato market price based on date and arrival volume.")

    with st.form("price_form"):
        c1, c2 = st.columns([1, 1])
        with c1:
            arrival = st.slider("🚛 Arrival Volume (Tonnes)", 10, 300, 100)
        with c2:
            selected_date = st.date_input("📅 Market Date", date.today())

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔍 Predict Price")

    if submitted:
        with st.spinner("🧠 Crunching data..."):
            day = selected_date.day
            month = selected_date.month
            predicted_price = 5000 - (10 * arrival) + (25 * month) + np.random.randint(-100, 100)
            st.success(f"💰 **Predicted Price**: ₹{int(predicted_price)} per quintal")

            # Graph
            st.markdown("---")
            st.subheader("📊 Impact of Arrival on Price")
            arrivals = np.arange(10, 310, 10)
            prices = 5000 - 10 * arrivals + 25 * month
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(arrivals, prices, marker='o', color='tomato')
            ax.set_xlabel("Arrival Volume (Tonnes)")
            ax.set_ylabel("Price (₹/quintal)")
            ax.set_title("Tomato Price vs Arrival Volume")
            st.pyplot(fig)

# ------------------ CROP HEALTH ------------------ #
else:
    st.subheader("🧪 Tomato Crop Health Checker")
    st.markdown("Check if your crop's nutrient levels match its growth stage requirements.")

    st.markdown("### 🌿 Nutrient Inputs")
    c1, c2, c3, c4 = st.columns(4)
    with c1: N = st.number_input("Nitrogen (N)", 0, 300, 100)
    with c2: P = st.number_input("Phosphorus (P)", 0, 300, 60)
    with c3: K = st.number_input("Potassium (K)", 0, 300, 120)
    with c4: age = st.number_input("Age (Days)", 0, 200, 40)

    if age < 30:
        stage = "🍃 Transplant to Vegetative"
        ideal = {"N": (80, 120), "P": (50, 70), "K": (80, 100)}
    elif age < 60:
        stage = "🌿 Vegetative to Flowering"
        ideal = {"N": (100, 140), "P": (60, 80), "K": (100, 130)}
    elif age < 90:
        stage = "🌸 Flowering to Fruiting"
        ideal = {"N": (80, 120), "P": (60, 80), "K": (130, 160)}
    else:
        stage = "🍅 Maturity & Harvest"
        ideal = {"N": (60, 100), "P": (50, 70), "K": (120, 150)}

    def evaluate(val, low, high):
        if val < low: return "🔻 Low"
        elif val > high: return "🔺 High"
        else: return "✅ Optimal"

    st.markdown("---")
    st.markdown(f"### 🩺 Health Report for Stage: **{stage}**")

    st.markdown(f"- **Nitrogen (N):** {evaluate(N, *ideal['N'])} _(Ideal: {ideal['N'][0]}–{ideal['N'][1]})_")
    st.markdown(f"- **Phosphorus (P):** {evaluate(P, *ideal['P'])} _(Ideal: {ideal['P'][0]}–{ideal['P'][1]})_")
    st.markdown(f"- **Potassium (K):** {evaluate(K, *ideal['K'])} _(Ideal: {ideal['K'][0]}–{ideal['K'][1]})_")

    # Graph
    st.markdown("---")
    st.subheader("📊 Nutrient Analysis Chart")
    df = pd.DataFrame({
        'Nutrient': ['Nitrogen', 'Phosphorus', 'Potassium'],
        'Current': [N, P, K],
        'Ideal Min': [ideal['N'][0], ideal['P'][0], ideal['K'][0]],
        'Ideal Max': [ideal['N'][1], ideal['P'][1], ideal['K'][1]],
    })

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df['Nutrient'], df['Current'], label='Current', color='seagreen')
    ax.plot(df['Nutrient'], df['Ideal Min'], 'r--', label='Ideal Min')
    ax.plot(df['Nutrient'], df['Ideal Max'], 'g--', label='Ideal Max')
    ax.set_ylabel("kg/ha")
    ax.set_title("Current vs Ideal Nutrient Levels")
    ax.legend()
    st.pyplot(fig)
