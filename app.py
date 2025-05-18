import streamlit as st
import numpy as np 
import pandas as pd
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Vertical Curve Calculator", layout="centered")
st.title("Vertical Curve Calculator")
st.caption("Designed for Civil Engineers | “Ten toes down!”")

# --- Email Capture ---
st.markdown("### Join the Beta List")
email = st.text_input("Enter your email to get updates and Pro access later", key="email_input")

if st.button("Join Waitlist"):
    if "@" in email and "." in email:
        with open("emails.txt", "a") as f:
            f.write(f"{email} - {datetime.now()}\n")
        st.success("You're on the list!")
    else:
        st.error("Please enter a valid email address.")

st.divider()

# --- Input Mode Selection ---
st.markdown("### Choose Input Method")
input_mode = st.radio("Select Input Type:", ("Elevation-Based", "Grade-Based"))

# --- Input Variables ---
bvc_station = bvc_elevation = evc_station = evc_elevation = 0.0
pvi_station = pvi_elevation = g1 = g2 = curve_length = 0.0

# --- Elevation-Based Input ---
if input_mode == "Elevation-Based":
    st.subheader("Elevation-Based Inputs")

    bvc_station = st.number_input("BVC Station", value=0.0, step=1.0, format="%.2f")
    bvc_elevation = st.number_input("BVC Elevation", value=0.0, step=0.01)

    evc_station = st.number_input("EVC Station", value=100.0, step=1.0, format="%.2f")
    evc_elevation = st.number_input("EVC Elevation", value=10.0, step=0.01)

    # Safe default to avoid division by zero or blank screen
    if bvc_station < evc_station:
        default_pvi = (bvc_station + evc_station) / 2
    else:
        default_pvi = bvc_station + 50.0

    pvi_station = st.number_input("PVI Station", value=default_pvi, step=1.0, format="%.2f")
    pvi_elevation = st.number_input("PVI Elevation", value=(bvc_elevation + evc_elevation) / 2, step=0.01)

    curve_length = evc_station - bvc_station
    g1 = ((pvi_elevation - bvc_elevation) / (pvi_station - bvc_station) * 100) if pvi_station != bvc_station else 0.0
    g2 = ((evc_elevation - pvi_elevation) / (evc_station - pvi_station) * 100) if evc_station != pvi_station else 0.0

# --- Grade-Based Input ---
else:
    st.subheader("Grade-Based Inputs")

    bvc_station = st.number_input("BVC Station", value=0.0, step=1.0, format="%.2f")
    evc_station = st.number_input("EVC Station", value=100.0, step=1.0, format="%.2f")
    bvc_elevation = st.number_input("BVC Elevation", value=0.0, step=0.01)
    g1 = st.number_input("Grade In (g₁) [%]", value=2.0, step=0.01, format="%.2f")
    g2 = st.number_input("Grade Out (g₂) [%]", value=-2.0, step=0.01, format="%.2f")

    curve_length = evc_station - bvc_station

# --- Computation ---
a_value = g2 - g1
g1_decimal = g1 / 100
g2_decimal = g2 / 100

if curve_length > 0:
    x_vals = np.linspace(0, curve_length, 100)
    y_vals = bvc_elevation + g1_decimal * x_vals + (a_value / 100) * x_vals**2 / (2 * curve_length)
else:
    x_vals = np.array([0])
    y_vals = np.array([bvc_elevation])

# --- Results Display ---
st.header("Curve Summary")
st.markdown(f"**Curve Length (L):** {curve_length:.2f} ft")
st.markdown(f"**Grade In (g₁):** {g1:.2f} %")
st.markdown(f"**Grade Out (g₂):** {g2:.2f} %")
st.markdown(f"**A = g₂ - g₁:** {a_value:.2f} %")

k_val = curve_length / abs(a_value) if a_value != 0 else None
st.markdown(f"**K-value:** {k_val:.2f}" if k_val else "**K-value:** Undefined")

# --- Plot Output ---
st.markdown("### Elevation Profile")
df = pd.DataFrame({"Distance from BVC (ft)": x_vals, "Elevation (ft)": y_vals})
st.line_chart(df.set_index("Distance from BVC (ft)"))

# --- Point Elevation Lookup ---
st.subheader("Elevation at Any Station")
station_input = st.number_input("Enter Station to Evaluate", value=bvc_station + curve_length / 2, step=1.0, format="%.2f")

if bvc_station <= station_input <= evc_station and curve_length > 0:
    x = station_input - bvc_station
    elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
    grade_at_x = g1 + (a_value * x / curve_length)

    st.markdown(f"**Elevation at {station_input:.2f} ft:** {elevation:.4f} ft")
    st.markdown(f"**Grade at {station_input:.2f} ft:** {grade_at_x:.4f} %")
else:
    st.warning("Station is outside curve limits or curve length is invalid.")

# --- Export Placeholder ---
st.divider()
st.markdown("#### Export Results (Pro Feature)")
st.button("Export to PDF or CSV (Coming Soon!)")