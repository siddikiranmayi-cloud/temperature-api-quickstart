import streamlit as st

st.set_page_config(
    page_title="HeatShield AI",
    page_icon="",
    layout="wide"
)

def calculate_risk(temperature,
humidity):
    score = 0

    if temperature >= 40:
        score += 60
    elif temperature >= 35:
        score += 45
    elif temperature >= 30:
        score += 25
    else:
        score += 10
    if humidity >= 70:
        score += 30
    elif humidity >= 50:
        score += 20
    elif humidity >= 30:
        score += 10
    if score >= 75:
        level = "Extreme"
    elif score >= 55:
        level = "High"
    elif score >= 35:
        level = "Moderate"
    else:
        level = "Low"
    return score, level

st.title(" HeatShield AI")
st.subheader("AI-powered urban heat risk analysis")

st.write(
        "Analyze temperature and environmental conditions "
            "to understand local heat risk."
            
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=60.0, 
        value=35.0, 
        step=0.1
    )

with col2:
    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=1.0
    )

if st.button(" Analyze Heat Risk", use_container_width=True):
    score, level = calculate_risk(temperature, humidity)
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Heat Risk Score",f"{score}/100")
    with col2:
        st.metric("Risk Level", level)
    if level == "Extreme":
        st.error(" Extreme heat risk. Immediate precautions are recommended.")
    elif level == "High":
        st.warning("A High heat risk. Reduce prolonged outdoor exposure.")
    elif level == "Moderate":
        st.info(" Moderate heat risk. Stay hydrated and take breaks.")
    else:
        st.success(" Low heat risk. continue normal precautions.")
    st.subheader(" Recommendations")
    if temperature >= 35: 
        st.write(". Stay hydrated.") 
        st.write(". Avoid prolonged outdoor activity during peak heat.")
        st.write(". Use shaded or cool areas when possible.")
    if humidity >= 60:
        st.write(". High humidity may reduce the body's ability to cool itself.")
    st.write(" Check local heat conditions regularly.")