def evaluate_model(seller_df, similarity_threshold=0.65):  # Adjusted threshold to 0.65
    """
    Calculate accuracy based on the percentage of matches with a similarity score above the threshold.
    """
    # Count the number of matches with a similarity score above the threshold
    correct_matches = seller_df[seller_df['similarity_score'] >= similarity_threshold].shape[0]
    
    # Total number of matches
    total_matches = seller_df.shape[0]
    
    # Calculate accuracy
    accuracy = correct_matches / total_matches
    return accuracy