import pandas as pd
import re

def validate_csv_and_extract_data(df):
    required_columns = ["name", "age", "email"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df = df[required_columns]
    df = df.dropna()

    df = df[df["age"].apply(lambda x: str(x).isdigit())]
    df["age"] = df["age"].astype(int)
    df = df[df["age"].between(0, 120)]

    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    df = df[df["email"].apply(lambda x: bool(email_regex.match(str(x))))]

    data = df.to_dict(orient="records")
    return data
