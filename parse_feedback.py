import pandas as pd

def parse_feedback(file):
    df = pd.read_csv(file)
    
    feedback_column = 'feedback' if 'feedback' in df.columns else df.columns[0]
    combined_text = "\n".join(df[feedback_column].dropna().astype(str).tolist())

    return combined_text
