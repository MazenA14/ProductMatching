from data_loader import load_data
from feature_extractor import add_features
from similarity_calculator import match_products
from evaluator import evaluate_model
import pandas as pd

def main():
    master_file = 'master_sheet.xlsx'  # Path to master sheet
    seller_file = 'seller_sheet.xlsx'  # Path to seller sheet

    # Load and preprocess data
    master_df, seller_df = load_data(master_file, seller_file)

    # Extract features (optional, if needed)
    master_df = add_features(master_df, 'product_name')
    seller_df = add_features(seller_df, 'seller_item_name')

    # Match products
    seller_df = match_products(seller_df, master_df)

    # Remove unnecessary columns from the output
    seller_df = seller_df.drop(columns=['seller_item_name_normalized', 'features'])

    # Calculate accuracy based on similarity scores
    accuracy = evaluate_model(seller_df, similarity_threshold=0.65)

    # Save the matched results to a file with UTF-8 encoding
    output_file = 'matched_results.csv'  # Output file name
    seller_df.to_csv(output_file, index=False, encoding='utf-8-sig')  # Fix encoding issue
    print(f"Matched results saved to {output_file}")
    print(f'Model Accuracy (based on similarity scores >= 0.65): {accuracy * 100:.2f}%')

    ############################################################

    file_path = "matched_results.csv"  # Path to the original CSV file
    more_accuracy, matching_rows =  calculate_matching_percentage(file_path)
    if more_accuracy is not None:
        # print(f"Matching rows: {matching_rows}")
        print(f"Model accuracy using two sku columns (Most accurate method, but can't be used the first sku is returned to item code of seller): {more_accuracy:.2f}%")
    else:
        print("Error calculating more accurate model accuracy.")

def calculate_matching_percentage(file_path):
    """
    Reads a comma-separated CSV file and calculates the percentage of rows where the first column matches the seventh column.
    Skips problematic lines that cause errors and saves rows where the columns do not match to a new CSV file.

    :param file_path: Path to the CSV file.
    :return: Percentage of matching rows.
    """
    try:
        # Read the CSV file into a DataFrame, skipping problematic lines
        df = pd.read_csv(file_path, delimiter=',', encoding='utf-8', on_bad_lines='skip')

        # Debug: Print the shape and columns of the DataFrame
        # print("DataFrame shape:", df.shape)
        # print("Columns in the file:", df.columns.tolist())

        # Ensure the DataFrame has at least 7 columns
        if df.shape[1] < 7:
            raise ValueError("The CSV file must have at least 7 columns.")

        # Clean the data: Remove extra spaces and convert to string
        # df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.strip()
        # df.iloc[:, 6] = df.iloc[:, 6].astype(str).str.strip()

        # Find rows where the first column does not match the seventh column
        mismatched_rows = df[df.iloc[:, 0] != df.iloc[:, 6]]

        # Save mismatched rows to a new CSV file
        if not mismatched_rows.empty:
            mismatched_rows.to_csv("mismatched_rows.csv", index=False, encoding='utf-8')
            print("Mismatched rows saved to 'mismatched_rows.csv'.")
        else:
            print("All rows match between the first and seventh columns.")

        # Compare the first column (index 0) and the seventh column (index 6)
        matching_rows = df[df.iloc[:, 0] == df.iloc[:, 6]].shape[0]

        # Calculate the total number of rows
        total_rows = df.shape[0]

        # Calculate the percentage of matching rows
        if total_rows > 0:
            matching_percentage = (matching_rows / total_rows) * 100
        else:
            matching_percentage = 0

        return matching_percentage, matching_rows

    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None, None

if __name__ == "__main__":
    main()