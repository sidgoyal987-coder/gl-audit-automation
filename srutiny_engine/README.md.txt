# GL Scrutiny Engine (Audit Analytics)

A rule-driven, context-aware General Ledger scrutiny engine designed for audit and finance analytics.

This project automates first-level GL review by applying configurable audit rules on accounting data using Python and Excel-based control files.

---

## 🔍 Key Features

- Rule-based scrutiny using Excel (no hardcoding)
- GL nature inference using prefix-based logic
- GL-level override support
- Debit/Credit behavior validation
- Rule conflict logging (why a rule was skipped)
- Audit-ready exception output

---

## 🗂 Project Structure


---

## 📊 Input Files

### 1. input_ledger.xlsx
Contains raw ledger data with:
- Account Code
- Debit Amount
- Credit Amount
- Date
- Voucher / Invoice details

### 2. gl_master.xlsx
Defines accounting context:
- GL prefix → default account nature
- GL-level overrides

### 3. rules.xlsx
Defines audit rules:
- Account nature applicability
- Debit / Credit checks
- Rule priority & severity

---

## ⚙️ How the Engine Works

1. Reads ledger data
2. Infers account nature using GL prefix
3. Applies GL-level overrides
4. Executes rules in priority order
5. Flags violations
6. Logs skipped rules with reasons

---

## ▶️ How to Run

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
