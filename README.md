# Product Matching System

## Overview
This project aims to match product names from a seller's sheet to a master product list.

## Instructions
1. Run `pip install -r requirements.txt`
2. Run `python main.py`
3. Results will show two accuracy percentages (Second one is more accurate, this only works if the seller file is already matched, used in testing only)
4. Two CSV files are produced
- "matched_results.csv" contains all rows products
- "mismatched_results.csv" contains all rows that were matched incorrectly, this only works if the seller file is already matched, used in testing only
5. Runtime of this code on 83562 rows is around 7 minutes