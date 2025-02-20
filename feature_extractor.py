import re
from tqdm import tqdm

def extract_features(text):
    dosage = re.findall(r'\d+\s*mg|\d+\s*ml', text)
    concentration = re.findall(r'\d+', text)
    return dosage, concentration

def add_features(df, column_name):
    print("Extracting features...")
    df['features'] = df[column_name].apply(extract_features)
    return df