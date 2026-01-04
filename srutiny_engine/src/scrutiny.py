import pandas as pd

# =====================================================
# 1. LOAD INPUT FILES (GitHub folder structure)
# =====================================================
ledger = pd.read_excel("../data/input_ledger.xlsx")
rules = pd.read_excel("../data/rules.xlsx")

prefix_master = pd.read_excel(
    "../data/gl_master.xlsx",
    sheet_name="GL_Prefix_Master"
)

override_master = pd.read_excel(
    "../data/gl_master.xlsx",
    sheet_name="GL_Overrides"
)

# =====================================================
# 2. NORMALISE LEDGER COLUMN NAMES
# (Excel file remains untouched)
# =====================================================
ledger = ledger.rename(columns={
    "Account Code": "GL_Code",
    "Debit Amount": "Debit",
    "Credit Amount": "Credit"
})

# =====================================================
# 3. DATA PREPARATION
# =====================================================
ledger["GL_Code"] = ledger["GL_Code"].astype(str)
ledger["GL_Prefix"] = ledger["GL_Code"].str[0]

ledger["Date"] = pd.to_datetime(ledger["Date"], errors="coerce")

ledger["Debit"] = pd.to_numeric(ledger["Debit"], errors="coerce").fillna(0)
ledger["Credit"] = pd.to_numeric(ledger["Credit"], errors="coerce").fillna(0)

prefix_master["GL_Prefix"] = prefix_master["GL_Prefix"].astype(str)
override_master["GL_Code"] = override_master["GL_Code"].astype(str)

# =====================================================
# 4. ATTACH PREFIX-LEVEL CONTEXT
# =====================================================
ledger = ledger.merge(
    prefix_master,
    on="GL_Prefix",
    how="left"
)

ledger.rename(
    columns={"Default_Nature": "Prefix_Nature"},
    inplace=True
)

# =====================================================
# 5. APPLY GL-LEVEL OVERRIDES (FINAL AUTHORITY)
# =====================================================
ledger = ledger.merge(
    override_master[["GL_Code", "Override_Nature", "Normal_Balance"]],
    on="GL_Code",
    how="left",
    suffixes=("", "_Override")
)

ledger["Final_Nature"] = ledger["Override_Nature"].combine_first(
    ledger["Prefix_Nature"]
)

# =====================================================
# 6. HANDLE RULE PRIORITY (DEFENSIVE)
# =====================================================
if "Priority" not in rules.columns:
    rules["Priority"] = 1

rules = rules.sort_values("Priority")

# =====================================================
# 7. SCRUTINY ENGINE WITH CONFLICT LOGGING
# =====================================================
flags = []
conflict_logs = []

for _, row in ledger.iterrows():

    rule_applied = False

    for _, rule in rules.iterrows():

        rule_id = rule["Rule_ID"]
        rule_name = rule["Rule_Name"]
        applies_to = rule["Applies_To"]
        check = rule["Check"]
        severity = rule["Severity"]
        description = rule["Description"]

        # ---- Rule skipped: nature mismatch
        if row["Final_Nature"] != applies_to:
            conflict_logs.append({
                "GL_Code": row["GL_Code"],
                "Rule_ID": rule_id,
                "Status": "Skipped",
                "Reason": f"Rule applies to {applies_to}, GL classified as {row['Final_Nature']}"
            })
            continue

        # ---- Rule skipped: higher priority rule already applied
        if rule_applied:
            conflict_logs.append({
                "GL_Code": row["GL_Code"],
                "Rule_ID": rule_id,
                "Status": "Skipped",
                "Reason": "Higher priority rule already triggered"
            })
            continue

        # ---- Evaluate rule condition
        violated = False

        if check == "Credit > 0" and row["Credit"] > 0:
            violated = True

        elif check == "Debit > 0" and row["Debit"] > 0:
            violated = True

        if violated:
            flagged_row = row.to_dict()
            flagged_row.update({
                "Rule_ID": rule_id,
                "Rule_Name": rule_name,
                "Severity": severity,
                "Flag_Reason": description
            })
            flags.append(flagged_row)
            rule_applied = True
        else:
            conflict_logs.append({
                "GL_Code": row["GL_Code"],
                "Rule_ID": rule_id,
                "Status": "Checked",
                "Reason": "Condition not violated"
            })

# =====================================================
# 8. OUTPUT FILES
# =====================================================
if flags:
    pd.DataFrame(flags).to_excel(
        "../outputs/output_flags.xlsx",
        index=False
    )

pd.DataFrame(conflict_logs).to_excel(
    "../outputs/rule_conflict_log.xlsx",
    index=False
)

print("Scrutiny completed successfully with conflict logging.")
