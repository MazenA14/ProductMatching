from fuzzywuzzy import fuzz
from tqdm import tqdm  # Import tqdm for the progress bar

def match_products(seller_sheet, master_file):
    matched_products = []

    # Add a progress bar for the matching process
    for _, seller_row in tqdm(seller_sheet.iterrows(), total=len(seller_sheet), desc="Matching Products"):
        best_match = None
        best_score = 0

        for _, master_row in master_file.iterrows():
            # Calculate similarity score between product names
            score = fuzz.ratio(seller_row['processed_name'], master_row['processed_name'])

            if score > best_score:
                best_score = score
                best_match = master_row

        # Add the best match to the results
        matched_products.append({
            'seller_sku': seller_row['sku'],
            'seller_item_name': seller_row['seller_item_name'],
            'master_sku': best_match['sku'],
            'master_product_name': best_match['product_name_ar'],
            'similarity_score': best_score / 100  # Convert to 0-1 range
        })

    return pd.DataFrame(matched_products)