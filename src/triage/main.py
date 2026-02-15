from __future__ import annotations

import sys

from .io import read_invoices, write_results
from .rules import triage

def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python -m triage.main <input_csv> <out_dir>", file=sys.stderr)
        return 2

    in_csv, out_dir = argv[1], argv[2]
    invoices = read_invoices(in_csv)
    triaged = [(inv, triage(inv)) for inv in invoices]
    write_results(out_dir, triaged)
    print(f"Wrote results to {out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
