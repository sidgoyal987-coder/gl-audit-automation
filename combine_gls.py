import pandas as pd
import glob
import os
import re

INPUT_FOLDER = "input_gls"
TEMPLATE_FILE = "Book3.xlsx"
OUTPUT_FILE = "output/Book3_FINAL.xlsx"

# Read Book3 template (only headings)
template_df = pd.read_excel(TEMPLATE_FILE)

final_rows = []

all_files = [
    f for f in glob.glob(os.path.join(INPUT_FOLDER, "*.xlsx"))
    if not os.path.basename(f).startswith("~$")
]

for file in all_files:
    print("Processing:", file)

    account_code = re.search(r"\d{4}", file).group()

    # 🔴 IMPORTANT FIX IS HERE
    df = pd.read_excel(file, skiprows=13)

    # Filter: Code Combination starts with 36
    filter_col = df["Code Combination"].astype(str).str.strip()
    df = df[filter_col.str.startswith("36", na=False)]

    def get_col(col_name):
        return df[col_name] if col_name in df.columns else [""] * len(df)

    mapped_df = pd.DataFrame({
        "Gl Date": pd.to_datetime(get_col("Date"), errors="coerce", dayfirst=True),
        "Invoice Number": get_col("Invoice Number"),
        "Description": get_col("Description"),
        "Cheque Number": get_col("Cheque Number"),
        "Debit Amount": get_col("Debit Amount"),
        "Credit Amount": get_col("Credit Amount"),
        "Code Combination": get_col("Code Combination"),
        "Account Code": [account_code] * len(df)
    })

    final_rows.append(mapped_df)

combined_df = pd.concat(final_rows, ignore_index=True)
final_output = pd.concat([template_df, combined_df], ignore_index=True)

final_output.to_excel(OUTPUT_FILE, index=False)

print("✅ Book3_FINAL.xlsx created successfully with DATA")
