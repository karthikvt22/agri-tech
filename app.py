import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt

# --- Function 1: Tomato Price Predictor ---

def tomato\_price\_predictor():
st.header("🍅 Tomato Price Predictor")
st.write("Select a future date to predict the expected tomato price.")

```
# User-selected date
user_date = st.date_input("Pick a future date", pd.to_datetime("2024-12-01"))

# Simulated historical data
dates = pd.date_range(start="2019-01-01", end="2024-12-31", freq="M")
prices = np.random.normal(loc=2500, scale=300, size=len(dates))  # INR per quintal
df = pd.DataFrame({"ds": dates, "y": prices})

# Train Prophet model
model = Prophet()
model.fit(df)

# Predict future
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Find prediction for user date
selected = forecast[forecast['ds'] == pd.to_datetime(user_date)]
if not selected.empty:
    predicted_price = selected['yhat'].values[0]
    st.success(f"📈 Predicted Tomato Price on {user_date}: ₹{predicted_price:.2f} per quintal")
else:
    st.warning("⚠️ Please select a date within one year from today.")

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
```

# --- Function 2: Crop Health Assessor ---

def crop\_health\_assessor():
st.header("🌿 Crop Health & Growth Stage Assessor")
st.write("Enter NPK values and crop age to assess current health status.")

```
# Inputs
n = st.number_input("Nitrogen (N)", 0, 300, 150)
p = st.number_input("Phosphorus (P)", 0, 300, 100)
k = st.number_input("Potassium (K)", 0, 300, 200)
crop_age = st.number_input("Crop Age (in days)", 1, 200, 50)

# Growth stage
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

ideal = norms[stage]
def assess(value, ideal_range):
    if ideal_range[0] <= value <= ideal_range[1]:
        return "✅ Optimal"
    elif value < ideal_range[0]:
        return "🔻 Low"
    else:
        return "🔺 High"

# Output
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
```

# --- Main App Layout ---

def main():
st.title("🌾 Smart Agriculture Assistant")
st.sidebar.title("🔍 Choose Feature")
app\_mode = st.sidebar.radio("Select Option", \["Tomato Price Predictor", "Crop Health Assessor"])

```
if app_mode == "Tomato Price Predictor":
    tomato_price_predictor()
elif app_mode == "Crop Health Assessor":
    crop_health_assessor()
```

if **name** == "**main**":
main()
