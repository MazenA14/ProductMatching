def calculate_similarity_score(text1, text2):
    # Use fuzzywuzzy to calculate similarity
    from fuzzywuzzy import fuzz
    return fuzz.ratio(text1, text2) / 100  # Convert to 0-1 range