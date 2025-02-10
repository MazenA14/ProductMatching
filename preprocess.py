import re
from langdetect import detect

def preprocess_product_name(product_name):
    # Convert to lowercase
    product_name = product_name.lower()

    # Remove special characters and extra spaces
    product_name = re.sub(r'[^\w\s]', '', product_name)
    product_name = re.sub(r'\s+', ' ', product_name).strip()

    # Normalize Arabic text
    if detect(product_name) == 'ar':
        product_name = re.sub(r'[\u064B-\u065F]', '', product_name)  # Remove Arabic diacritics

    return product_name