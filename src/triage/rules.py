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
    raise NotImplementedError

def rule_no_grn(inv: Invoice) -> Optional[TriageResult]:
    raise NotImplementedError

def rule_tax_data_issue(inv: Invoice) -> Optional[TriageResult]:
    raise NotImplementedError

def rule_amount_outlier(inv: Invoice) -> Optional[TriageResult]:
    raise NotImplementedError

def rule_terms_mismatch(inv: Invoice) -> Optional[TriageResult]:
    raise NotImplementedError

RULES: list[Rule] = [
    # rule_missing_po,
    # rule_no_grn,
    # rule_tax_data_issue,
    # rule_amount_outlier,
    # rule_terms_mismatch,
]

def triage(inv: Invoice) -> TriageResult:
    """Apply ordered rules; first match wins; otherwise CLEAN."""
    for rule in RULES:
        res = rule(inv)
        if res is not None:
            return res
    return TriageResult(bucket="CLEAN", owner_queue="AP-AutoPay", reason="Pass")
