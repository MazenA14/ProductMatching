import pandas as pd
from tqdm import tqdm  # Import tqdm for the progress bar
from preprocess import preprocess_product_name
from model import match_products

# Step 1: Load the dataset file (seller sheet) with a progress bar
print("Loading seller sheet...")
seller_sheet = pd.read_excel('seller_sheet.xlsx')

# Step 2: Load the master file with a progress bar
print("Loading master file...")
master_file = pd.read_excel('master_file.xlsx')

# Step 3: Preprocess product names with a progress bar
print("Preprocessing product names...")
seller_sheet['processed_name'] = [preprocess_product_name(name) for name in tqdm(seller_sheet['marketplace_product_name_ar'], desc="Preprocessing Seller Sheet")]
master_file['processed_name'] = [preprocess_product_name(name) for name in tqdm(master_file['product_name_ar'], desc="Preprocessing Master File")]

# Step 4: Match products with a progress bar
print("Matching products...")
matched_products = match_products(seller_sheet, master_file)

# Step 5: Save the output to a CSV file
print("Saving results to CSV...")
matched_products.to_csv('matched_products.csv', index=False)

# Display a message indicating where the output is saved
print("Output saved to 'matched_products.csv'")