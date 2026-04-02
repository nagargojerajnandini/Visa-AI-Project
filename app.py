import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="AI Visa Estimator", layout="centered")

# ---------------------------
# Sidebar (ONLY INFO)
# ---------------------------
st.sidebar.title("🌍 AI Visa System")
st.sidebar.write("Smart visa processing estimator")
st.sidebar.write("📊 AI-based prediction")
st.sidebar.write("⚡ Real-time insights")
st.sidebar.write("🎯 Decision support system")

# ---------------------------
# Main Title
# ---------------------------
st.title("🌍 AI Visa Processing Time Estimator")
st.caption("🔍 Powered by AI-based estimation model")

# ---------------------------
# Inputs
# ---------------------------
st.subheader("📝 Enter Visa Details")

col1, col2, col3 = st.columns(3)

with col1:
    visa_type_input = st.selectbox("Visa Type", ["Student", "Tourist", "Work"])

with col2:
    country_input = st.selectbox("Country", ["India", "USA", "UK"])

with col3:
    application_date = st.date_input("Application Date", datetime.today())

# Mapping
country_map = {"India": 0, "USA": 1, "UK": 2}
visa_type_map = {"Student": 0, "Tourist": 1, "Work": 2}

visa_type = visa_type_map[visa_type_input]
country = country_map[country_input]
application_date_ordinal = application_date.toordinal()

# ---------------------------
# Prediction Function
# ---------------------------
def predict_processing_time(input_data):
    base_days = [30, 20, 45]
    country_adj = [0, 10, 5]
    date_variation = input_data['application_date'] % 10
    estimated_days = base_days[input_data['visa_type']] + country_adj[input_data['country']] + date_variation
    return max(5, min(estimated_days, 90))

# ---------------------------
# Predict Button
# ---------------------------
if st.button("🚀 Predict Processing Time"):

    # Progress bar
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    input_data = {
        "visa_type": visa_type,
        "country": country,
        "application_date": application_date_ordinal
    }

    result = predict_processing_time(input_data)

    # Status
    if result < 20:
        status = "Fast 🟢"
    elif result < 40:
        status = "Normal 🟡"
    else:
        status = "Delayed 🔴"

    # Decision Date
    decision_date = application_date + timedelta(days=result)

    # ---------------------------
    # RESULT
    # ---------------------------
    st.success("✅ Prediction Ready!")

    st.subheader("📊 Result")

    c1, c2, c3 = st.columns(3)
    c1.metric("⏳ Days", result)
    c2.metric("📌 Status", status)
    c3.metric("📅 Decision Date", str(decision_date))

    # ---------------------------
    # Generate Dynamic Data
    # ---------------------------
    months = list(range(1, 13))

    processing_days = [
        max(5, result + random.randint(-10, 10)) for _ in months
    ]

    df_dynamic = pd.DataFrame({
        "Month": months,
        "Processing Days": processing_days
    })

    # ---------------------------
    # Charts
    # ---------------------------
    st.subheader("📈 Monthly Processing Trend")
    fig1 = px.line(df_dynamic, x="Month", y="Processing Days", markers=True)
    st.plotly_chart(fig1)

    st.subheader("📊 Processing Days by Month")
    fig2 = px.bar(df_dynamic, x="Month", y="Processing Days")
    st.plotly_chart(fig2)

    st.subheader("📦 Processing Distribution")
    fig3 = px.histogram(df_dynamic, x="Processing Days", nbins=10)
    st.plotly_chart(fig3)

    # Pie Chart
    st.subheader("🥧 Processing Category Distribution")

    categories = []
    for d in processing_days:
        if d < 20:
            categories.append("Fast")
        elif d < 40:
            categories.append("Normal")
        else:
            categories.append("Delayed")

    df_pie = pd.DataFrame({"Category": categories})
    pie_data = df_pie["Category"].value_counts().reset_index()
    pie_data.columns = ["Category", "Count"]

    fig4 = px.pie(pie_data, names="Category", values="Count")
    st.plotly_chart(fig4)

    # Area Chart
    st.subheader("🌊 Processing Area Trend")
    fig5 = px.area(df_dynamic, x="Month", y="Processing Days")
    st.plotly_chart(fig5)

    # ---------------------------
    # AI Insight
    # ---------------------------
    st.subheader("🤖 AI Insight")

    st.info(f"""
    The estimated processing time is **{result} days** for a **{visa_type_input} visa in {country_input}**.

    This is influenced by:
    - Visa category workload  
    - Country processing speed  
    - Application timing trends  
    """)

    # Celebration
    st.balloons()