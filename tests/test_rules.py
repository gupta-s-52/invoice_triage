import pytest

from triage.rules import Invoice, triage


def inv(**overrides):
    base = dict(
        invoice_id="INV-X",
        vendor_id="V-1",
        invoice_date="2026-02-01",
        due_date="2026-03-01",
        currency="USD",
        amount=100.0,
        po_number="PO-1",
        grn_received="Y",
        tax_id="AB12CD34",
        payment_terms="NET30",
        bank_account_last4="1234",
    )
    base.update(overrides)
    return Invoice(**base)


def test_missing_po():
    res = triage(inv(po_number=""))
    assert res.bucket == "MISSING_PO"


def test_rule_order_tax_beats_outlier():
    res = triage(inv(amount=999999.0, tax_id=""))
    assert res.bucket == "TAX_DATA_ISSUE"
