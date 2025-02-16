import pandas as pd
from fuzzywuzzy import fuzz
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Step 1: Load labeled data
print("Loading labeled data...")
labeled_data = pd.read_excel('labeled_data.xlsx')  # Ensure this file exists and is correctly formatted

# Step 2: Feature engineering
def extract_features(seller_name, master_name):
    # Example features: similarity score, length difference, common words
    similarity_score = fuzz.token_set_ratio(seller_name, master_name) / 100
    length_diff = abs(len(seller_name) - len(master_name))
    common_words = len(set(seller_name.split()) & set(master_name.split()))
    return [similarity_score, length_diff, common_words]

# Step 3: Extract features and labels
print("Extracting features...")
X = [extract_features(row['seller_name'], row['master_name']) for _, row in tqdm(labeled_data.iterrows(), total=len(labeled_data))]
y = labeled_data['match']

# Step 4: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train a Random Forest model
print("Training the model...")
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 6: Evaluate the model
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred)}")

# Step 7: Save the model to disk
joblib.dump(model, 'product_matching_model.pkl')
print("Model trained and saved to 'product_matching_model.pkl'.")