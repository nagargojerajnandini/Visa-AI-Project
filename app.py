import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Visa Processing Dashboard", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4B0082;'>🌍 Visa Processing Time Estimator</h1>", unsafe_allow_html=True)

# ---------------------------
# User Inputs
# ---------------------------
visa_type_input = st.selectbox("Visa Type", ["Student", "Tourist", "Work",])
country_input = st.selectbox("Select Country", ["India", "USA", "UK"])
application_date = st.date_input("Application Date", datetime.today())

country_map = {
    "India": 0,
    "USA": 1,
    "UK": 2,
    
}

visa_type_map = {
    "Student": 0,
    "Tourist": 1,
    "Work": 2,
    
}
visa_type = visa_type_map[visa_type_input]
country = country_map[country_input]
application_date_ordinal = application_date.toordinal()

# ---------------------------
# Prediction Function
# ---------------------------
def predict_processing_time(input_data):
    base_days = [30, 20, 45]  # Student, Tourist, Work
    country_adj = [0, 10, 5]   # India, USA, UK
    date_variation = input_data['application_date'] % 10
    estimated_days = base_days[input_data['visa_type']] + country_adj[input_data['country']] + date_variation
    return max(5, min(estimated_days, 90))

# ---------------------------
# Predict Button
# ---------------------------
if st.button("Predict Processing Time"):
    input_data = {"visa_type": visa_type, "country": country, "application_date": application_date_ordinal}
    result = predict_processing_time(input_data)
    st.success(f"⏳ Estimated Processing Time: {result} days")

# ---------------------------
# Sample dataset for graphs
# ---------------------------
data = {
    "application_date": [
        datetime(2026,3,1), datetime(2026,3,5), datetime(2026,2,20),
        datetime(2026,1,10), datetime(2026,3,2), datetime(2026,2,15),
        datetime(2026,1,25), datetime(2026,3,12), datetime(2026,2,28)
    ],
    "decision_date": [
        datetime(2026,3,15), datetime(2026,3,18), datetime(2026,3,5),
        datetime(2026,1,25), datetime(2026,3,20), datetime(2026,3,1),
        datetime(2026,2,5), datetime(2026,3,20), datetime(2026,3,15)
    ]
}

df = pd.DataFrame(data)
df["processing_days"] = (df["decision_date"] - df["application_date"]).dt.days
df["application_month"] = df["application_date"].dt.month


figsize = (6,4)  # Compact, milestone-friendly

# 1. Histogram
st.write("### 📊 Distribution of Visa Processing Days")
fig1, ax1 = plt.subplots(figsize=figsize)
sns.histplot(df["processing_days"], bins=15, ax=ax1)
ax1.set_xlabel("Processing Days")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# 2. Boxplot
st.write("### 📦 Boxplot of Processing Days")
fig2, ax2 = plt.subplots(figsize=figsize)
sns.boxplot(x=df["processing_days"], ax=ax2)
st.pyplot(fig2)

# 3. Correlation Heatmap
st.write("### 🔥 Correlation Heatmap")
corr_matrix = df[["processing_days", "application_month"]].corr()
fig3, ax3 = plt.subplots(figsize=figsize)
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax3)
st.pyplot(fig3)

# 4. Boxplot Month vs Days
st.write("### 📅 Processing Days vs Application Month")
fig4, ax4 = plt.subplots(figsize=figsize)
sns.boxplot(x="application_month", y="processing_days", data=df, ax=ax4)
st.pyplot(fig4)

# 5. Monthly Trend Line
st.write("### 📈 Monthly Trend of Processing Days")
monthly_avg = df.groupby("application_month")["processing_days"].mean()
fig5, ax5 = plt.subplots(figsize=figsize)
ax5.plot(monthly_avg.index, monthly_avg.values, marker='o')
ax5.set_xlabel("Month")
ax5.set_ylabel("Average Processing Days")
st.pyplot(fig5)

