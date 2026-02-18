import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="LV Digital Twin", layout="wide")

st.title("⚡ LV Transformer Digital Twin")

# ===============================
# Input Section
# ===============================

st.sidebar.header("Transformer Parameters")

rated_power_kva = st.sidebar.number_input("Rated Power (kVA)", value=500.0)
rated_voltage = st.sidebar.number_input("Rated Voltage (V)", value=400.0)
power_factor = st.sidebar.number_input("Power Factor", value=0.9)

st.sidebar.header("Feeder Currents (A)")

I1 = st.sidebar.number_input("Feeder 1 Current", value=100.0)
I2 = st.sidebar.number_input("Feeder 2 Current", value=120.0)
I3 = st.sidebar.number_input("Feeder 3 Current", value=90.0)

# ===============================
# Calculation
# ===============================

if st.button("Evaluate"):

    total_current = I1 + I2 + I3
    apparent_power = (rated_voltage * total_current * 1.732) / 1000  # kVA
    loading_percent = (apparent_power / rated_power_kva) * 100

    # Status logic
    if loading_percent < 70:
        status = "🟢 Normal"
        color = "green"
    elif loading_percent < 100:
        status = "🟡 Warning"
        color = "orange"
    else:
        status = "🔴 Overloaded"
        color = "red"

    # ===============================
    # Results Display
    # ===============================

    st.subheader("Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Current (A)", f"{total_current:.2f}")
    col2.metric("Apparent Power (kVA)", f"{apparent_power:.2f}")
    col3.metric("Loading (%)", f"{loading_percent:.2f}%")

    st.markdown(f"### Status: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)

    # ===============================
    # Table
    # ===============================

    df = pd.DataFrame({
        "Feeder": ["Feeder 1", "Feeder 2", "Feeder 3"],
        "Current (A)": [I1, I2, I3]
    })

    st.subheader("Feeder Data")
    st.dataframe(df, use_container_width=True)

    # ===============================
    # Plot
    # ===============================

    st.subheader("Current Distribution")

    fig, ax = plt.subplots()
    ax.bar(df["Feeder"], df["Current (A)"])
    ax.set_ylabel("Current (A)")
    ax.set_title("Feeder Currents")

    st.pyplot(fig)
