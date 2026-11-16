# storage.py
# Saves and loads the sale records as JSON text in sales.json.

import json
import ledger

FILE_NAME = "sales.json"

# Every record must have these fields before the program trusts it.
REQUIRED_FIELDS = ("slip_no", "date", "customer", "package", "quantity",
                   "amount", "released", "to_follow", "payment_mode")


def load_sales(file_name=FILE_NAME):
    # Returns the list of records.
    # Missing file -> empty list (first run, no sales yet).
    # Damaged file -> None, so main.py stops instead of overwriting it.
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return None

    # The file must hold a list of dictionaries with all required fields.
    if type(records) != list:
        return None
    for record in records:
        if type(record) != dict:
            return None
        for field in REQUIRED_FIELDS:
            if field not in record:
                return None
        # The report looks these up in ledger.PACKAGES and ledger.PAYMENT_MODES.
        if record["package"] not in ledger.PACKAGES:
            return None
        if record["payment_mode"] not in ledger.PAYMENT_MODES:
            return None
    return records


def save_sales(sales, file_name=FILE_NAME):
    # "w" mode creates the file, or replaces everything in it.
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(sales, file, indent=2)
