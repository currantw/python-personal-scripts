#!/usr/bin/env python3
"""
Process American Express activity CSV into a cleaned Excel file with columns:
- Date (transaction date)
- Source ("American Express Cobalt")
- Expense (cleaned description)
- Taylor Paid (amount if Card Member is Taylor Curran; else 0)
- Anvita Paid (amount if Card Member is Anvita Akkur; else 0)
- Taylor Portion (0.6 if groceries; else blank)

Usage:
    python process_amex_expenses.py --input activity.csv --output amex_expenses_full.xlsx
"""

import argparse
import re
import sys


import pandas as pd


# Regex patterns for grocery stores
GROCERY_PATTERNS = [
    re.compile(r"\bSAVE[-\s]?ON\b", re.IGNORECASE),
    re.compile(r"\bWHOLE[-\s]?FOODS\b", re.IGNORECASE),
    re.compile(r"\bSAFEWAY\b", re.IGNORECASE),
    re.compile(r"\bNO[-\s]?FRILLS\b", re.IGNORECASE),
    re.compile(r"\bSUPERSTORE\b", re.IGNORECASE),
    re.compile(r"\bTHRIFTY\b", re.IGNORECASE),
    re.compile(r"\bWALMART\b", re.IGNORECASE),
    re.compile(r"\b7\sELEVEN\b", re.IGNORECASE),
]

TAYLOR_NAME = "TAYLOR"
ANVITA_NAME = "ANVITA"


def clean_description(desc: str) -> str:
    """Simplify merchant description: remove store numbers, URLs, long numbers/phones, collapse spaces."""
    if not isinstance(desc, str):
        return ""

    s = desc
    s = re.sub(r"#\d+", "", s)  # remove store numbers like "#12345"
    s = re.sub(r"http\S+", "", s, flags=re.IGNORECASE)  # remove URLs
    s = re.sub(r"\+?\d[\d\-\s\(\)]{6,}", "", s)  # remove phone-like numbers
    s = re.sub(r"\b\d{7,}\b", "", s)  # remove long digit runs
    s = " ".join(s.split())  # normalize whitespace
    return s.strip()


def is_grocery(merchant: str) -> bool:
    """Check if the description matches any grocery store pattern."""
    if not isinstance(merchant, str):
        return False
    return any(pattern.search(merchant) for pattern in GROCERY_PATTERNS)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="Path to Amex activity CSV")
    p.add_argument("--output", "-o", required=True, help="Path to output Excel file")
    args = p.parse_args()

    # Read CSV (expects columns like: Date, Date Processed, Description, Card Member, Account #, Amount)
    try:
        df = pd.read_csv(args.input)
    except Exception as e:
        print(f"Error reading input CSV: {e}", file=sys.stderr)
        sys.exit(1)

    # Keep only expenses (positive amounts). Payments/credits are negative in Amex export.
    if "Amount" not in df.columns:
        print("Input CSV missing 'Amount' column.", file=sys.stderr)
        sys.exit(1)
    expenses = df[df["Amount"] > 0].copy()

    # Required input columns
    for col in ("Date", "Description", "Card Member"):
        if col not in expenses.columns:
            print(f"Input CSV missing '{col}' column.", file=sys.stderr)
            sys.exit(1)

    # Transform
    expenses["Expense"] = expenses["Description"].apply(clean_description)
    expenses["Source"] = "American Express Cobalt"

    def paid_for(row, who: str) -> float:
        cm = str(row.get("Card Member", "")).upper()
        return float(row["Amount"]) if who in cm else 0.0

    expenses["Taylor Paid"] = expenses.apply(lambda r: paid_for(r, TAYLOR_NAME), axis=1)
    expenses["Anvita Paid"] = expenses.apply(lambda r: paid_for(r, ANVITA_NAME), axis=1)
    expenses["Taylor Portion"] = expenses["Expense"].apply(lambda x: 0.6 if is_grocery(x) else "")

    out = expenses[
        ["Date", "Source", "Expense", "Taylor Paid", "Anvita Paid", "Taylor Portion"]
    ].copy()

    try:
        out.to_excel(args.output, index=False)
    except Exception as e:
        print(f"Error writing Excel: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
