# 🧠 GBS GitHub Copilot Weekly Challenge — Week 1 (Python)
## Invoice Exception Triage Mini‑Service

**Audience:** GBS Developers  
**Difficulty:** ⭐ Easy  
**Timebox:** ~60–90 minutes  
**Primary Tool:** GitHub Copilot  
**Language:** Python 3.11+  
**Data:** Synthetic only (no real P&G data)

---

## 🎯 Objective
Build a small **Python CLI** that simulates a common GBS pattern:

> Automatically **triage supplier invoice exceptions** into the correct handling queues using deterministic business rules.

This is intentionally **rules-based** (no ML) so you can focus on:
- translating business rules into clean code
- using GitHub Copilot to accelerate implementation
- writing fast, meaningful unit tests
- keeping the solution readable and maintainable

---

## 📦 What’s Included in This Repo
This repo is a **starter scaffold** following the recommended GitHub structure:
- `.github/workflows/ci.yml` CI pipeline
- `src/triage/` package scaffold
- `tests/` scaffold
- `data/invoices.csv` synthetic sample input

> You will implement the logic where you see **TODO** markers.

---

## 📁 Repository Structure
```text
.github/
  workflows/
    ci.yml
src/
  triage/
    __init__.py
    io.py
    rules.py
    main.py
tests/
  test_rules.py
data/
  invoices.csv
README.md
requirements-dev.txt
.gitignore
```

---

## 📄 Input Data
File: `data/invoices.csv`

Columns:
- `invoice_id`
- `vendor_id`
- `invoice_date`
- `due_date`
- `currency`
- `amount`
- `po_number`
- `grn_received`
- `tax_id`
- `payment_terms`
- `bank_account_last4`

All data is **synthetic**.

---

## 🧠 Triage Rules (Order Matters)
Rules are applied **top‑down**. The **first matching rule wins**.

### A — `MISSING_PO`
- `po_number` empty or `"NULL"`
- **Owner queue:** `AP-Helpdesk`
- **Reason:** `PO missing`

### B — `NO_GRN`
- `po_number` present AND `grn_received = N`
- **Owner queue:** `Receiving`
- **Reason:** `Goods receipt not posted`

### C — `TAX_DATA_ISSUE`
- `tax_id` missing OR invalid
- Valid = **alphanumeric**, length **8–15**
- **Owner queue:** `Vendor-MDM`
- **Reason:** `Tax ID missing/invalid`

### D — `AMOUNT_OUTLIER`
- `amount > 10000` (no currency conversion)
- **Owner queue:** `AP-Triage`
- **Reason:** `High value invoice requires review`

### E — `TERMS_MISMATCH`
- `payment_terms` not in `NET30, NET45, NET60`
- **Owner queue:** `AP-VendorMgmt`
- **Reason:** `Payment terms not standard`

### F — `CLEAN`
- No rule matched
- **Owner queue:** `AP-AutoPay`
- **Reason:** `Pass`

---

## 📤 Required Outputs
### 1) `out/triage_results.csv`
Columns:
```
invoice_id,triage_bucket,owner_queue,reason
```

### 2) `out/summary.json`
Structure:
```json
{
  "total_invoices": 5,
  "counts_by_bucket": {
    "MISSING_PO": 1,
    "NO_GRN": 1,
    "TAX_DATA_ISSUE": 2,
    "CLEAN": 1
  },
  "total_amount_at_risk": 14500.0
}
```

> **total_amount_at_risk** = sum of `amount` for all invoices where `triage_bucket != CLEAN`.

---

## ▶️ How to Run
From the repo root:

```bash
python -m triage.main data/invoices.csv out/
```

---

## 🧪 How to Test
```bash
pip install -r requirements-dev.txt
PYTHONPATH=src pytest -q
```

---

## ✅ Definition of Done
**Must-have**
- CLI runs successfully
- Both output files generated
- Tests passing locally and in CI
- Clear, readable rule implementation

**Nice-to-have**
- Type hints + docstrings
- `--strict` mode: fail if required columns missing
- “Explain mode”: print which rule matched and why

---

## 🤖 Copilot-First Prompt Ideas
Try prompts like:
- “Implement an ordered rule engine for these rules and return bucket/owner/reason.”
- “Write pytest tests for each rule and at least one rule-order test.”
- “Refactor into small functions with type hints and docstrings.”

---

## 🔐 Access / Onboarding (internal)
If you don’t have GitHub Copilot access yet, follow the internal [**<File>codePG--Github-Copilot.aspx</File>**](https://pgone.sharepoint.com/sites/GBSaccelerators/SitePages/codePG--Github-Copilot.aspx?web=1) guidance for onboarding and office hours. citeturn8search102

---

Happy building! 👩‍💻👨‍💻
