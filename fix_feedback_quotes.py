import pandas as pd
import csv

def fix_quotes(input_path, output_path):
    df = pd.read_csv(input_path, dtype=str)
    df = df.fillna("")  # Fill any missing feedback with empty string

    df.to_csv(output_path, quoting=csv.QUOTE_ALL, index=False)

if __name__ == "__main__":
    fix_quotes("sample_feedback.csv", "sample_feedback_cleaned.csv")
    print("Cleaned file saved as sample_feedback_cleaned.csv")
