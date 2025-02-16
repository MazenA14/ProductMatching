# predict_matches.py
import pandas as pd
import re  # Import the re module for regular expressions
from rapidfuzz import fuzz  # Faster alternative to fuzzywuzzy
from tqdm import tqdm
import joblib
from joblib import Parallel, delayed  # For parallel processing

# Step 1: Load the trained model
print("Loading the trained model...")
model = joblib.load('product_matching_model.pkl')

# Step 2: Load the seller and master files
print("Loading seller and master files...")
seller_file = pd.read_excel('seller_file.xlsx')
master_file = pd.read_excel('master_file.xlsx')

# Step 3: Preprocess product names
def preprocess_text(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^\w\s]', '', str(text)).lower()
    return text

print("Preprocessing product names...")
seller_file['seller_item_name_clean'] = [preprocess_text(name) for name in tqdm(seller_file['seller_item_name'], desc="Preprocessing seller names")]
master_file['product_name_clean'] = [preprocess_text(name) for name in tqdm(master_file['product_name'], desc="Preprocessing master names")]

# Step 4: Define the extract_features function
def extract_features(seller_name, master_name):
    # Example features: similarity score, length difference, common words
    similarity_score = fuzz.token_set_ratio(seller_name, master_name) / 100  # Using rapidfuzz
    length_diff = abs(len(seller_name) - len(master_name))
    common_words = len(set(seller_name.split()) & set(master_name.split()))
    return [similarity_score, length_diff, common_words]

# Step 5: Function to predict matches
def predict_match(seller_name, master_name):
    features = extract_features(seller_name, master_name)
    match_probability = model.predict_proba([features])[0][1]  # Probability of being a match
    return match_probability

# Step 6: Match products using the ML model (parallelized)
def process_seller_row(row, master_file):
    seller_name_en = row['seller_item_name_clean']
    best_match = None
    best_score = 0
    for _, master_row in master_file.iterrows():
        master_name_en = master_row['product_name_clean']
        match_prob = predict_match(seller_name_en, master_name_en)
        if match_prob > best_score:
            best_score = match_prob
            best_match = master_name_en
    return {
        'seller_item_name': row['seller_item_name'],
        'matched_product_name': best_match,
        'match_probability': best_score
    }

print("Matching products...")
results = Parallel(n_jobs=-1)(delayed(process_seller_row)(row, master_file) for _, row in tqdm(seller_file.iterrows(), total=seller_file.shape[0], desc="Matching products"))

# Step 7: Save results to Excel
results_df = pd.DataFrame(results)
results_df.to_excel('matched_products_ml.xlsx', index=False)
print("Results saved to 'matched_products_ml.xlsx'.")