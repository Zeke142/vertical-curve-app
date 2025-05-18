import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Vertical Curve Calculator", layout="centered")
st.title("Vertical Curve Calculator")
st.caption("Designed for Civil Engineers | “Ten toes down!”")

# -----------------------------
# Email Waitlist Feature
# -----------------------------
def collect_email():
    st.markdown("### Join the Beta List")
    email = st.text_input("Enter your email for updates and Pro access")

    if st.button("Join Waitlist"):
        if "@" in email and "." in email:
            with open("emails.txt", "a") as f:
                f.write(f"{email} - {datetime.now()}\n")
            st.success("You're on the list!")
        else:
            st.error("Please enter a valid email address.")

collect_email()
st.divider()

# -----------------------------
# Curve Input Handling
# -----------------------------
def get_inputs():
    input_mode = st.radio("Select Input Type:", ("Elevation-Based", "Grade-Based"))

    if input_mode == "Elevation-Based":
        st.subheader("Elevation-Based Inputs")
        bvc_station = st.number_input("BVC Station", value=0.0)
        bvc_elevation = st.number_input("BVC Elevation", value=0.0)
        evc_station = st.number_input("EVC Station", value=100.0)
        evc_elevation = st.number_input("EVC Elevation", value=10.0)

        pvi_station = st.number_input("PVI Station", value=(bvc_station + evc_station) / 2)
        pvi_elevation = st.number_input("PVI Elevation", value=(bvc_elevation + evc_elevation) / 2)

        length = evc_station - bvc_station
        g1 = (pvi_elevation - bvc_elevation) / (pvi_station - bvc_station) * 100 if pvi_station != bvc_station else 0.0
        g2 = (evc_elevation - pvi_elevation) / (evc_station - pvi_station) * 100 if evc_station != pvi_station else 0.0

    else:
        st.subheader("Grade-Based Inputs")
        bvc_station = st.number_input("BVC Station", value=0.0)
        evc_station = st.number_input("EVC Station", value=100.0)
        bvc_elevation = st.number_input("BVC Elevation", value=0.0)
        g1 = st.number_input("Grade In (g₁) [%]", value=2.0)
        g2 = st.number_input("Grade Out (g₂) [%]", value=-2.0)
        length = evc_station - bvc_station

    return {
        "mode": input_mode,
        "bvc_station": bvc_station,
        "bvc_elevation": bvc_elevation,
        "evc_station": evc_station,
        "g1": g1,
        "g2": g2,
        "length": length
    }

inputs = get_inputs()

# -----------------------------
# Curve Calculation
# -----------------------------
def compute_profile(inputs):
    a = inputs["g2"] - inputs["g1"]
    g1_dec = inputs["g1"] / 100
    x_vals = np.linspace(0, inputs["length"], 100) if inputs["length"] > 0 else np.array([0])
    y_vals = inputs["bvc_elevation"] + g1_dec * x_vals + (a / 100) * (x_vals ** 2) / (2 * inputs["length"]) if inputs["length"] > 0 else np.array([inputs["bvc_elevation"]])
    return x_vals, y_vals, a

x_vals, y_vals, a = compute_profile(inputs)

# -----------------------------
# Output Display
# -----------------------------
def display_summary(inputs, a):
    st.header("Curve Summary")
    st.markdown(f"**Curve Length (L):** {inputs['length']:.2f} ft")
    st.markdown(f"**Grade In (g₁):** {inputs['g1']:.2f} %")
    st.markdown(f"**Grade Out (g₂):** {inputs['g2']:.2f} %")
    st.markdown(f"**A = g₂ - g₁:** {a:.2f} %")

    k_val = inputs['length'] / abs(a) if a != 0 else None
    st.markdown(f"**K-value:** {k_val:.2f}" if k_val else "**K-value:** Undefined")

    st.markdown("### Elevation Profile")
    df = pd.DataFrame({
        "Distance from BVC (ft)": x_vals,
        "Elevation (ft)": y_vals
    })
    st.line_chart(df.set_index("Distance from BVC (ft)"))

display_summary(inputs, a)

# -----------------------------
# Elevation at Specific Station
# -----------------------------
def evaluate_station(inputs, a):
    st.subheader("Elevation at Any Station")
    station = st.number_input("Enter Station to Evaluate", value=inputs["bvc_station"] + inputs["length"] / 2)

    if inputs["bvc_station"] <= station <= inputs["evc_station"] and inputs["length"] > 0:
        x = station - inputs["bvc_station"]
        g1_dec = inputs["g1"] / 100
        elevation = inputs["bvc_elevation"] + g1_dec * x + (a / 100) * x**2 / (2 * inputs["length"])
        grade = inputs["g1"] + a * x / inputs["length"]

        st.markdown(f"**Elevation at {station:.2f} ft:** {elevation:.4f} ft")
        st.markdown(f"**Grade at {station:.2f} ft:** {grade:.4f} %")
    else:
        st.warning("Station is outside the curve limits or curve length is invalid.")

evaluate_station(inputs, a)

# -----------------------------
# Placeholder for Export
# -----------------------------
st.divider()
st.markdown("#### Export Results (Pro Feature)")
st.button("Export to PDF or CSV (Coming Soon!)")