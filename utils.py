import pandas as pd

def export_to_excel(df, filename="filtered_expenses.xlsx"):
    df.to_excel(filename, index=False)
    return filename
