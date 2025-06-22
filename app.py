import streamlit as st
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Exoplanet Habitability Predictor", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

.stApp {
    background-image: url("https://i.gifer.com/origin/d7/d76326011a134837339791474559d745_w200.gif");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

.main > div {
    background-color: rgba(0, 0, 0, 0.7);
    padding: 2rem;
    border-radius: 1rem;
    border: 3px solid;
    border-image-slice: 1;
    border-width: 3px;
    border-image-source: linear-gradient(to right, #00bfff, #ee82ee);
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from {
        box-shadow: 0 0 10px #00bfff, 0 0 20px #00bfff, 0 0 30px #00bfff;
    }
    to {
        box-shadow: 0 0 20px #ee82ee, 0 0 30px #ee82ee, 0 0 40px #ee82ee;
    }
}

h1, .stMarkdown, label {
    font-family: 'Orbitron', sans-serif !important;
}

h1 {
    text-shadow: 0 0 10px #00bfff, 0 0 20px #00bfff;
    color: #00bfff;
    animation: pulse 1.5s infinite alternate;
}

@keyframes pulse {
    from {
        text-shadow: 0 0 10px #00bfff, 0 0 20px #00bfff;
    }
    to {
        text-shadow: 0 0 20px #00bfff, 0 0 35px #00bfff;
    }
}

.stButton > button {
    border: 2px solid #00bfff;
    border-radius: 20px;
    padding: 10px 20px;
    background-color: transparent;
    color: #00bfff;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    transition: .4s;
}

.stButton > button:hover {
    background-color: #00bfff;
    color: black;
    box-shadow: 0 0 20px #00bfff;
}

.stNumberInput input {
    transition: all 0.2s ease-in-out;
    border-color: #00bfff;
    background-color: rgba(0, 0, 0, 0.5) !important;
    color: #00bfff !important;
}

.stNumberInput input:focus {
    border-color: #ee82ee;
    box-shadow: 0 0 10px #ee82ee;
}

[data-testid="stAlert"] {
    border-radius: 10px;
    font-family: 'Orbitron', sans-serif;
}

/* Success Alert */
[data-testid="stAlert"][data-baseweb="notification"][role="alert"] > div:first-of-type {
    background-color: rgba(0, 255, 127, 0.2);
    border: 1px solid springgreen;
}

/* Error Alert */
[data-testid="stAlert"][data-baseweb="notification"][role="alert"] > div:nth-of-type(2) {
    background-color: rgba(255, 69, 0, 0.2);
    border: 1px solid orangered;
}

</style>
""", unsafe_allow_html=True)


model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("🔭 Cosmic Oracle")
st.markdown("Is this world a new Earth? Enter planetary and stellar data to reveal its secrets.")


test_cases = {
    "Custom Input": None,
    "Earth-like Planet": [1.0, 288, 365, 5778, 1.0, 4.44],
    "Hot Jupiter": [11.0, 1200, 3.5, 6100, 1.5, 4.1],
    "Super-Earth": [1.5, 310, 130, 5000, 0.8, 4.5],
    "Cold Gas Giant": [3.5, 151, 493, 4299, 0.7, 2.5],
}

choice = st.selectbox("Select a celestial body profile:", options=list(test_cases.keys()))

if choice != "Custom Input":
    radius, temp, period, teff, st_rad, st_logg = test_cases[choice]
    st.info(f"Populated with data for: {choice}")
   
    st.number_input("Planet Radius (Earth radii)", value=radius, disabled=True)
    st.number_input("Equilibrium Temperature (K)", value=temp, disabled=True)
    st.number_input("Orbital Period (days)", value=period, disabled=True)
    st.number_input("Stellar Effective Temperature (K)", value=teff, disabled=True)
    st.number_input("Stellar Radius (Solar radii)", value=st_rad, disabled=True)
    st.number_input("Stellar Surface Gravity (log g)", value=st_logg, disabled=True)

else:
    radius = st.number_input("Planet Radius (Earth radii)", min_value=0.1, max_value=20.0, value=1.0, step=0.1)
    temp = st.number_input("Equilibrium Temperature (K)", min_value=100, max_value=2000, value=300)
    period = st.number_input("Orbital Period (days)", min_value=0.1, max_value=1000.0, value=365.0, step=0.1)
    teff = st.number_input("Stellar Effective Temperature (K)", min_value=2000, max_value=8000, value=5500)
    st_rad = st.number_input("Stellar Radius (Solar radii)", min_value=0.1, max_value=20.0, value=1.0, step=0.1)
    st_logg = st.number_input("Stellar Surface Gravity (log g)", min_value=0.0, max_value=10.0, value=4.4, step=0.1)

if st.button("Predict Habitability"):
    input_data = np.array([[radius, temp, period, teff, st_rad, st_logg]])
    scaled_input = scaler.transform(input_data)
    prediction = model.predict(scaled_input)[0]
    probability = model.predict_proba(scaled_input)[0][1] * 100

    if prediction == 1:
        st.success(f"Cosmic Scan Complete: This exoplanet shows signs of being habitable! (Confidence: {probability:.2f}%)")
    else:
        st.error(f"Cosmic Scan Complete: This exoplanet is likely hostile to life. (Confidence: {100 - probability:.2f}%)")

st.markdown("---")
st.caption("Model trained on Kepler data and tested on TESS candidates.")
