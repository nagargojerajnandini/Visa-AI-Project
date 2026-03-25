import pickle
import pandas as pd

# Load your trained model once
model = pickle.load(open("model.pkl", "rb"))

# Maps for string to numeric
visa_type_map = {"Student": 0, "Tourist": 1, "Work": 2}
country_map = {"India": 0, "USA": 1, "UK": 2}

def predict_processing_time(input_data):
    """
    input_data = {
        "country": "India",
        "visa_type": "Student",
        "application_date": "2024-01-01"
    }
    """
    # Convert strings to numbers
    visa_type_num = visa_type_map.get(input_data["visa_type"], 0)
    country_num = country_map.get(input_data["country"], 0)
    
    # Convert date to numeric ordinal
    application_date_num = pd.to_datetime(input_data["application_date"]).toordinal()
    
    # Prepare DataFrame for model
    X = pd.DataFrame([{
        "visa_type": visa_type_num,
        "country": country_num,
        "application_date": application_date_num
    }])
    
    # Predict
    predicted_days = model.predict(X)[0]
    
    # Optional: clamp for realistic range
    predicted_days = int(round(predicted_days))
    predicted_days = max(5, min(predicted_days, 90))
    
    return predicted_days