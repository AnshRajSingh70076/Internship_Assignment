# rag.py

import pandas as pd
import warnings
warnings.filterwarnings("ignore")
def load_data(path="data.csv"):
    df = pd.read_excel(path)

    docs = []
    for _, row in df.iterrows():
        text = f"{row['Customer Complaint / Query']} {row['Agent Action']}"
        docs.append({
            "id": row["Call ID"],
            "text": text,
            "outcome": row["Outcome"]
        })

    return docs