import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load your dataset
df = pd.read_csv("visa_dataset.csv", dayfirst=True)

# Map strings to numbers
country_map = {"India":0,"USA":1,"UK":2,"Australia":3,"Germany":4}
visa_type_map = {"Student":0,"Tourist":1,"Work":2,"Business":3,"Dependent":4}

df["country_num"] = df["country"].map(country_map)
df["visa_type_num"] = df["visa_type"].map(visa_type_map)
df["application_date_num"] = pd.to_datetime(df["application_date"], dayfirst=True).apply(lambda x: x.toordinal())
df["processing_days"] = (pd.to_datetime(df["decision_date"], dayfirst=True) - pd.to_datetime(df["application_date"], dayfirst=True)).dt.days

X = df[["visa_type_num","country_num","application_date_num"]]
y = df["processing_days"]

model = LinearRegression()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained on real dataset!")