import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Vertical Curve Calculator", layout="centered")

st.title("Vertical Curve Calculator")
st.subheader("Designed for Civil Engineers")

# --- Email Capture Form ---
st.markdown("### Join the beta list")
email = st.text_input("Enter your email to get updates and Pro access later", key="email_input")

if st.button("Join Waitlist"):
    if "@" in email and "." in email:
        with open("emails.txt", "a") as f:
            f.write(f"{email} - {datetime.now()}\n")
        st.success("You're on the list!")
    else:
        st.error("Please enter a valid email.")

# --- Vertical Curve Inputs ---
st.markdown("---")
st.markdown("### Curve Inputs")
g1 = st.number_input("Grade 1 (%)", value=-2.0)
g2 = st.number_input("Grade 2 (%)", value=3.0)
L = st.number_input("Curve Length (ft)", value=400.0)
PVI_station = st.number_input("PVI Station (ft)", value=1000.0)
PVI_elevation = st.number_input("PVI Elevation (ft)", value=120.0)

# --- Calculations ---
A = g2 - g1
x_vals = np.linspace(0, L, 100)
y_vals = PVI_elevation + g1 * x_vals + (A * x_vals**2) / (2 * L)

df = pd.DataFrame({"Distance from PVI (ft)": x_vals, "Elevation (ft)": y_vals})
st.line_chart(df.set_index("Distance from PVI (ft)"))

# --- Export Button (Pro Feature Placeholder) ---
st.markdown("#### Export Results (Pro Feature)")
st.button("Export to PDF or CSV (Coming Soon!)")