from predict import predict_processing_time

test_cases = [
    {"country": "India", "visa_type": "Student", "application_date": "2024-01-01"},
    {"country": "USA", "visa_type": "Work", "application_date": "2024-03-15"},
    {"country": "UK", "visa_type": "Tourist", "application_date": "2024-06-10"}
]

for i, case in enumerate(test_cases, start=1):
    result = predict_processing_time(case)
    print(f"Test Case {i}: {result} days")