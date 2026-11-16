# ledger.py
# Data and calculations for the Daily Sales Ledger.
# No input() or print() here: main.py talks to the user, this module does the math.

# ---------- Fixed choices ----------
# Tuples, because these values stay the same while the program runs.
MEMBER_TYPES = ("DISTRIBUTOR", "STOCKIST", "CENTER", "WALK-IN")
PAYMENT_MODES = ("CASH", "BANK", "E-WALLET", "CHEQUE", "CREDIT")
DENOMINATIONS = (1000, 500, 200, 100, 50, 20, 10, 5, 1, 0.25)

# ---------- Package catalog ----------
# Dictionary: package name -> price per package and bottles per package.
PACKAGES = {
    "STARTER": {"price": 3500.0, "bottles": 1},
    "PLUS": {"price": 10500.0, "bottles": 3},
    "PREMIUM": {"price": 17500.0, "bottles": 5},
    "RETAIL": {"price": 2800.0, "bottles": 1},
}


def compute_sale(package, quantity, discount, released):
    # Return the computed values of one sale as a dictionary.
    unit_price = PACKAGES[package]["price"]
    price = unit_price - discount
    bottles = PACKAGES[package]["bottles"] * quantity
    return {
        "price": price,
        "amount": price * quantity,
        "bottles": bottles,
        "to_follow": bottles - released,
    }


def next_slip_no(sales, sale_date):
    # Slip number = MMDDYY-NN. NN = highest number used on that date + 1.
    prefix = sale_date[5:7] + sale_date[8:10] + sale_date[2:4]
    highest = 0
    for record in sales:
        if record["date"] == sale_date:
            number = int(record["slip_no"].split("-")[1])
            if number > highest:
                highest = number
    next_number = highest + 1
    if next_number < 10:
        return prefix + "-0" + str(next_number)
    return prefix + "-" + str(next_number)


def find_sale(sales, slip_no):
    # Return the record with this slip number, or None if there is none.
    for record in sales:
        if record["slip_no"] == slip_no:
            return record
    return None


def records_between(sales, date_from, date_to):
    # Return the records dated from date_from to date_to, both included.
    # YYYY-MM-DD text compares in the same order as the dates.
    rows = []
    for record in sales:
        if date_from <= record["date"] <= date_to:
            rows.append(record)
    return rows


def daily_summary(sales, report_date):
    # Add up one day's sales by package and by payment mode.
    by_package = {}
    for name in PACKAGES:
        by_package[name] = {"quantity": 0, "amount": 0.0}
    by_payment = {}
    for mode in PAYMENT_MODES:
        by_payment[mode] = 0.0

    count = 0
    total = 0.0
    to_follow = 0
    for record in sales:
        if record["date"] == report_date:
            count += 1
            total += record["amount"]
            to_follow += record["to_follow"]
            by_package[record["package"]]["quantity"] += record["quantity"]
            by_package[record["package"]]["amount"] += record["amount"]
            by_payment[record["payment_mode"]] += record["amount"]

    return {
        "count": count,
        "by_package": by_package,
        "by_payment": by_payment,
        "total": total,
        "to_follow": to_follow,
    }


def cash_on_hand(counts):
    # counts is a dictionary: denomination -> number of pieces.
    total = 0.0
    for value in DENOMINATIONS:
        total += value * counts[value]
    return total


def cash_status(counted, expected):
    # round() removes tiny float errors, e.g. 0.30000000000000004 -> 0.3
    difference = round(counted - expected, 2)
    if difference == 0:
        return "BALANCED"
    elif difference > 0:
        return f"OVER by {difference:,.2f}"
    else:
        return f"SHORT by {-difference:,.2f}"
