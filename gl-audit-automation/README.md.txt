# GL Consolidation & Audit Automation Tool

## 📌 Problem Statement
Audit teams often receive multiple account-wise General Ledger (GL) files exported from ERP systems. These files:
- Contain non-tabular report headers
- Vary in structure
- Require filtering based on code combinations
- Must be consolidated into a standardized audit working paper

Manual consolidation is time-consuming and error-prone.

---

## ✅ Solution
This Python-based tool automates the end-to-end process of:
- Reading ERP-style GL reports
- Skipping non-data header sections
- Filtering line items where Code Combination starts with "36"
- Mapping GL data into a standardized Book3 audit format
- Appending account codes automatically
- Producing an audit-ready consolidated Excel file

---

## ⚙️ Key Features
- Handles multiple account-wise GL files
- Robust to missing columns and format differences
- Uses a predefined audit template
- Prevents Excel lock-file errors
- Designed for audit and finance workflows

---

## 🧠 Skills Demonstrated
- Audit automation
- Python (pandas, openpyxl)
- Data cleaning and transformation
- ERP GL structure understanding
- Process standardization
- Error handling

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python combine_gls.py
