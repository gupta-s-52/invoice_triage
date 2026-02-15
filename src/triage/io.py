from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .rules import Invoice, TriageResult

REQUIRED_COLUMNS = {
    "invoice_id","vendor_id","invoice_date","due_date","currency","amount",
    "po_number","grn_received","tax_id","payment_terms","bank_account_last4"
}

def read_invoices(csv_path: str) -> list[Invoice]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        invoices: list[Invoice] = []
        for row in reader:
            invoices.append(
                Invoice(
                    invoice_id=row["invoice_id"],
                    vendor_id=row["vendor_id"],
                    invoice_date=row["invoice_date"],
                    due_date=row["due_date"],
                    currency=row["currency"],
                    amount=float(row["amount"]),
                    po_number=row["po_number"],
                    grn_received=row["grn_received"],
                    tax_id=row["tax_id"],
                    payment_terms=row["payment_terms"],
                    bank_account_last4=row["bank_account_last4"],
                )
            )
        return invoices

def write_results(out_dir: str, rows: Iterable[tuple[Invoice, TriageResult]]) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    results_path = out / "triage_results.csv"
    with results_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["invoice_id","triage_bucket","owner_queue","reason"])
        for inv, res in rows:
            writer.writerow([inv.invoice_id, res.bucket, res.owner_queue, res.reason])

    # summary.json
    counts: dict[str, int] = {}
    total_amount_at_risk = 0.0
    total = 0

    for inv, res in rows:
        counts[res.bucket] = counts.get(res.bucket, 0) + 1
        total += 1
        if res.bucket != "CLEAN":
            total_amount_at_risk += inv.amount

    summary = {
        "total_invoices": total,
        "counts_by_bucket": counts,
        "total_amount_at_risk": round(total_amount_at_risk, 2),
    }

    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
