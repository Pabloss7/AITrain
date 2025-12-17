import pandas as pd

def clean_dataset(rows):
    df = pd.DataFrame([rows])
    df = df.fillna(0)
    
    return df