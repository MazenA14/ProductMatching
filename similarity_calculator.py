from fuzzywuzzy import fuzz
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

def calculate_similarity(name1, name2):
    """
    Calculate the similarity score between two names using fuzzywuzzy.
    """
    return fuzz.token_set_ratio(name1, name2) / 100.0

def match_products(seller_df, master_df):
    """
    Match seller products to master products based on similarity scores.
    """
    similarity_scores = []
    confidence_levels = []
    matched_skus = []

    print("Matching products...")

    # Iterate over each seller product
    for _, seller_row in tqdm(seller_df.iterrows(), total=seller_df.shape[0]):
        seller_name = seller_row['seller_item_name_normalized']

        # Calculate similarity scores against all master products
        scores_name = master_df['product_name_normalized'].apply(
            lambda x: calculate_similarity(seller_name, x)
        )
        scores_name_ar = master_df['product_name_ar_normalized'].apply(
            lambda x: calculate_similarity(seller_name, x)
        )

        # Find the best match (highest similarity score)
        best_match_index = scores_name.idxmax() if scores_name.max() >= scores_name_ar.max() else scores_name_ar.idxmax()
        best_match_score = max(scores_name.max(), scores_name_ar.max())

        # Get the SKU of the best match
        best_match_sku = master_df.loc[best_match_index, 'sku']

        # Append the results
        similarity_scores.append(best_match_score)
        confidence_levels.append(1.0 if best_match_score >= 0.65 else 0.5)
        matched_skus.append(best_match_sku)

    # Add the results to the seller DataFrame
    seller_df['similarity_score'] = similarity_scores
    seller_df['confidence_level'] = confidence_levels
    seller_df['matched_sku'] = matched_skus

    return seller_df