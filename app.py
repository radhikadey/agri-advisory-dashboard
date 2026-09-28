import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
model = joblib.load('model.pkl')
le_district = joblib.load('le_district.pkl')
le_crop = joblib.load('le_crop.pkl')

st.set_page_config(page_title="Agri-Data Advisory System", layout="centered")

st.title("🌾 Agri-Data Driven Yield & Profitability Advisory System")
st.write("Get ROI predictions for your crop based on district, crop type, and land area.")

# ---------------- SECTION 1: ROI PREDICTOR ----------------
st.sidebar.header("ROI Predictor")
district = st.sidebar.selectbox("Select District", sorted(le_district.classes_))
crop = st.sidebar.selectbox("Select Crop", sorted(le_crop.classes_))
area = st.sidebar.number_input("Land Area (Acres)", min_value=0.1, value=1.0, step=0.1)

if st.sidebar.button("Predict ROI"):
    district_encoded = le_district.transform([district])[0]
    crop_encoded = le_crop.transform([crop])[0]

    input_data = pd.DataFrame([[district_encoded, crop_encoded, area]],
                               columns=['District_encoded', 'Crop_encoded', 'Area (Acres)'])

    predicted_roi = model.predict(input_data)[0]

    st.subheader("📊 ROI Prediction Result")
    col1, col2 = st.columns(2)
    col1.metric("District", district)
    col2.metric("Crop", crop)

    st.metric("Predicted ROI (%)", f"{predicted_roi:.2f}%")

    if predicted_roi > 50:
        st.success("✅ This crop looks profitable in this district!")
    elif predicted_roi > 0:
        st.warning("⚠️ Moderate profitability — consider carefully.")
    else:
        st.error("❌ This crop may not be profitable in this district.")

st.markdown("---")

# ---------------- SECTION 2: PRICE VOLATILITY (Onion demo) ----------------
st.header("📉 Price Volatility by Month — Onion (Demonstration)")
st.write(
    "This section shows how much Onion prices swing month to month, based on "
    "2022-2024 market data. It illustrates the kind of price risk that motivated "
    "this project, using Onion because it is the only crop with usable data in "
    "both the production dataset and the market price dataset."
)

month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

volatility_data = pd.DataFrame({
    'Month': month_order,
    'Avg_Price': [5743.10, 6633.33, 5131.58, 3900.00, 5422.22, 5967.65,
                  7762.50, 8514.29, 6845.83, 8544.12, 9527.08, 8656.25],
    'Price_Volatility': [1858.83, 3526.66, 1940.52, 1096.26, 1432.83, 2224.36,
                         2704.72, 2653.64, 2474.98, 2720.36, 3286.82, 2387.34]
})

st.dataframe(volatility_data.set_index('Month'), use_container_width=True)

riskiest_month = volatility_data.loc[volatility_data['Price_Volatility'].idxmax(), 'Month']
safest_month = volatility_data.loc[volatility_data['Price_Volatility'].idxmin(), 'Month']

col1, col2 = st.columns(2)
col1.metric("Riskiest Month to Sell", riskiest_month)
col2.metric("Most Stable Month to Sell", safest_month)

st.markdown("---")
st.caption(
    "Built using public BBS, weather, and market price datasets. "
    "Prices/costs in the ROI predictor are estimated for demonstration purposes. "
    "Price volatility data covers 2022-2024 only."
)
