import pandas as pd

# Load output.xlsx and calculate percentage of matching rows
output_sheet = pd.read_csv("matched_results.csv")  #, delimiter=',', encoding='utf-8', on_bad_lines='skip'
matching_rows = (output_sheet.iloc[:, 0] == output_sheet.iloc[:, 6]).sum()
total_rows = len(output_sheet)
percentage = (matching_rows / total_rows) * 100 if total_rows > 0 else 0

print(f"Percentage of matching rows: {percentage:.2f}%")
