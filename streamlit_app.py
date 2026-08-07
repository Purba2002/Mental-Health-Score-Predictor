import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Mental Health Score Predictor", page_icon="🧠")

st.title("🧠 Mental Health Score Predictor")
st.write("Apne details daalke mental health score predict karo")

# Model load
model = joblib.load("Mental_Health_Model.pkl")

# Saare input fields
col1, col2 = st.columns(2)

with col1:
    Age = st.number_input("Age", 10, 100, 20)
    Gender = st.selectbox("Gender", ["Male", "Female"])
    Academic_Level = st.selectbox("Academic Level", ["School", "Undergraduate", "Graduate", "Postgraduate"])
    Sleep_Hours_Per_Night = st.slider("Sleep Hours Per Night", 0.0, 12.0, 7.0)
    Study_Hours = st.slider("Study Hours", 0.0, 12.0, 4.0)
    Physical_Activity_Hours = st.slider("Physical Activity Hours", 0.0, 5.0, 1.0)

with col2:
    Avg_Daily_Usage_Hours = st.slider("Avg Daily Social Media Usage Hours", 0.0, 10.0, 3.0)
    Daily_Unlocks = st.number_input("Daily Phone Unlocks", 0, 500, 50)
    Purpose_Of_Use = st.selectbox("Purpose Of Use", ["Entertainment", "Education", "Social", "Work"])
    Most_Used_Platform = st.selectbox("Most Used Platform", ["Instagram", "YouTube", "WhatsApp", "Facebook", "TikTok"])
    Grouped_country = st.selectbox("Country", ["India", "USA", "UK", "Canada", "Other"])
    Stress_Level = st.selectbox("Stress Level", ["Low", "Medium", "High"])

if st.button("Predict Score"):
    # DataFrame banao model ke hisaab se
    input_data = pd.DataFrame([{
        "Age": Age,
        "Gender": Gender,
        "Academic_Level": Academic_Level,
        "Sleep_Hours_Per_Night": Sleep_Hours_Per_Night,
        "Study_Hours": Study_Hours,
        "Physical_Activity_Hours": Physical_Activity_Hours,
        "Avg_Daily_Usage_Hours": Avg_Daily_Usage_Hours,
        "Daily_Unlocks": Daily_Unlocks,
        "Purpose_Of_Use": Purpose_Of_Use,
        "Most_Used_Platform": Most_Used_Platform,
        "Grouped_country": Grouped_country,
        "Stress_Level": Stress_Level
    }])

    prediction = model.predict(input_data)
    score = prediction[0]

    st.success(f"### Tumhara Predicted Mental Health Score: {score:.2f}")
    if score > 70:
        st.info("Mental Health: Good 👍")
    elif score > 40:
        st.warning("Mental Health: Average 😐")
    else:
        st.error("Mental Health: Needs Attention ⚠️")