from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Callable
import re

ALLOWED_TERMS = {"NET30", "NET45", "NET60"}
TAX_ID_RE = re.compile(r"^[A-Za-z0-9]{8,15}$")

@dataclass(frozen=True)
class Invoice:
    invoice_id: str
    vendor_id: str
    invoice_date: str
    due_date: str
    currency: str
    amount: float
    po_number: str
    grn_received: str
    tax_id: str
    payment_terms: str
    bank_account_last4: str

@dataclass(frozen=True)
class TriageResult:
    bucket: str
    owner_queue: str
    reason: str

Rule = Callable[[Invoice], Optional[TriageResult]]

# TODO: Implement each rule below and add them to RULES in the correct order.

def rule_missing_po(inv: Invoice) -> Optional[TriageResult]:
    if inv.po_number == "" or inv.po_number == "NULL":
        return TriageResult(
            bucket="MISSING_PO",
            owner_queue="AP-Helpdesk",
            reason="PO missing"
        )
    return None

def rule_no_grn(inv: Invoice) -> Optional[TriageResult]:
    if inv.po_number != "" and inv.po_number != "NULL" and inv.grn_received == "N":
        return TriageResult(
            bucket="NO_GRN",
            owner_queue="Receiving",
            reason="Goods receipt not posted"
        )
    return None

def rule_tax_data_issue(inv: Invoice) -> Optional[TriageResult]:
    if inv.tax_id == "" or not TAX_ID_RE.match(inv.tax_id):
        return TriageResult(
            bucket="TAX_DATA_ISSUE",
            owner_queue="Vendor-MDM",
            reason="Tax ID missing/invalid"
        )
    return None

def rule_amount_outlier(inv: Invoice) -> Optional[TriageResult]:
    if inv.amount > 10000:
        return TriageResult(
            bucket="AMOUNT_OUTLIER",
            owner_queue="AP-Triage",
            reason="High value invoice requires review"
        )
    return None

def rule_terms_mismatch(inv: Invoice) -> Optional[TriageResult]:
    if inv.payment_terms not in ALLOWED_TERMS:
        return TriageResult(
            bucket="TERMS_MISMATCH",
            owner_queue="AP-VendorMgmt",
            reason="Payment terms not standard"
        )
    return None

RULES: list[Rule] = [
    rule_missing_po,
    rule_no_grn,
    rule_tax_data_issue,
    rule_amount_outlier,
    rule_terms_mismatch,
]

def triage(inv: Invoice) -> TriageResult:
    """Apply ordered rules; first match wins; otherwise CLEAN."""
    for rule in RULES:
        res = rule(inv)
        if res is not None:
            return res
    return TriageResult(bucket="CLEAN", owner_queue="AP-AutoPay", reason="Pass")
