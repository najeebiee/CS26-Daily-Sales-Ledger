# CS 26 Exam 2 – Technical Documentation
## Daily Sales Ledger

**Student:** Mapantas, Najeeb C.  
**Course:** CS 26 – Software Development Fundamentals  
**Program type:** Python console program

---

## A. Program Overview

The Daily Sales Ledger is a console program for the sales counter of a small supplement distributor. The **encoder** records each sale. At closing, the **cashier** prints the daily report and counts the cash drawer.

The program numbers each order slip, computes the amount due, tracks bottles the customer will pick up later ("to follow"), totals the day's sales, and checks if the drawer is short or over. Records are saved to `sales.json`.

## B. Problem Description

**Problem:** Sales are written on paper slips and added up on a calculator. Totals can be wrong, the report is slow, notes on "to follow" bottles get lost, and there is no quick way to check the cash drawer.

### Inputs
| Input | Example | Rule |
|---|---|---|
| Date | `2026-11-15` | Real date, `YYYY-MM-DD`. Blank = today. |
| Customer name | `Liza Ramos` | Required |
| Member type | `DISTRIBUTOR` | DISTRIBUTOR, STOCKIST, CENTER, WALK-IN |
| Package | `PLUS` | STARTER, PLUS, PREMIUM, RETAIL |
| Quantity | `2` | Whole number, 1–100 |
| Discount per package | `500` | 0 up to the unit price |
| Bottles released now | `4` | 0 up to total bottles |
| Payment mode | `CASH` | CASH, BANK, E-WALLET, CHEQUE, CREDIT |
| Reference number | `BNK-20441` | Required if not CASH |
| Remarks | `promo price` | Optional |
| Cash count | `9` pieces of 1,000 | Whole number, 0 or more |

### Processing
- Discounted price = unit price − discount
- Sales amount = discounted price × quantity
- Total bottles = bottles per package × quantity
- Bottles to follow = total bottles − bottles released
- Slip number = `MMDDYY-NN`, where NN = highest number used that day + 1
- Cash on hand = sum of (denomination × pieces)
- Cash status = cash on hand compared with CASH sales: BALANCED, SHORT, or OVER

**Example:** 2 × PLUS (10,500.00, 3 bottles each), 500 discount, 4 released → price 10,000.00, amount 20,000.00, 6 bottles, 2 to follow.

### Outputs
- Sale confirmation with slip number, amount, and bottles to follow
- Table of records for a date range
- Daily report: totals by package and payment mode, grand total, bottles to follow
- Cash result: BALANCED, SHORT by X, or OVER by X
- `sales.json`, which keeps the records between runs

## C. Program Objectives

1. Compute the price, amount, and bottles to follow of each sale.
2. Give each sale a unique slip number, even after a delete.
3. View records by date range, release bottles, and delete records.
4. Print a daily report and check the cash drawer.
5. Save and load records, and handle a missing or damaged file.

### Program design

#### Flowchart
```text
        START
          |
   Load sales.json ---- damaged ----> show error, END
          |
          v
   Show menu, read choice  <-----------------+
          |                                  |
   1 Encode a sale ------------------------->|
   2 View records -------------------------->|
   3 Update a record ----------------------->|
   4 Delete a record ----------------------->|
   5 Daily report -------------------------->|
   other: "Invalid choice" ----------------->+
          |
          6
          v
         END
```

#### Pseudocode: main program
```text
records <- load sales.json
IF file is damaged THEN show error and stop
REPEAT
    show menu, read choice
    run the matching action (1-5), or show "Invalid choice"
UNTIL choice = 6
```

#### Pseudocode: encode a sale
```text
ask date, customer, member type, package, quantity, discount,
    bottles released, payment mode          (repeat each until valid)
IF payment mode is not CASH THEN ask reference number
compute price, amount, bottles, to_follow
slip_no <- highest slip number for the date + 1
show summary; IF user types "y" THEN add record and save
```

#### Pseudocode: daily report and cash count
```text
FOR each record on the report date
    add amount to its package total and payment total
    add to_follow to the to-follow total
show totals
IF user wants a cash count THEN
    cash <- sum of denomination * pieces
    compare cash with the CASH total: BALANCED, OVER, or SHORT
```

## D. Requirements and Features

| Feature | Menu option |
|---|---|
| Encode a sale with validation and automatic math | 1 |
| Automatic slip number (`MMDDYY-NN`) | 1 |
| View records by date range | 2 |
| Release bottles / change reference number | 3 |
| Delete a record (asks to confirm) | 4 |
| Daily report and cash count | 5 |
| Save and load `sales.json` | automatic |

**Package catalog (sample data, in pesos)**

| Package | Unit price | Bottles |
|---|---:|---:|
| STARTER | 3,500.00 | 1 |
| PLUS | 10,500.00 | 3 |
| PREMIUM | 17,500.00 | 5 |
| RETAIL | 2,800.00 | 1 |

**Assumptions:** one user at a time; run `main.py` from the `cs26-project` folder; only CASH payments go into the drawer.

**Limitations:** one package type per slip; records are not sorted; if saving fails, the change is lost when the program closes; numbers inside a hand-edited `sales.json` are not checked.

## E. Program Structure and Modules

```text
cs26-project/
├── main.py             # run this: menu, input, output
├── ledger.py           # data and calculations (no input or print)
├── storage.py          # reads and writes sales.json
└── sample_sales.json   # 6 sample records for testing
```

`main.py` imports the other two modules and calls them with a dot:

```python
import ledger
import storage

sales = storage.load_sales()
result = ledger.compute_sale(package, quantity, discount, released)
```

The module is named `ledger.py`, not `sales.py`, because `sales` is already the name of the records list.

The menu compares the choice as text (`"1"`, `"2"`, …), so typing a letter shows "Invalid choice" instead of crashing.

## F. Data Structures

**List** – `sales` holds all sale records. New sales are added with `append()` and deleted with `remove()`. A list fits because the number of sales changes.

**Tuple** – fixed choices that never change:

```python
MEMBER_TYPES = ("DISTRIBUTOR", "STOCKIST", "CENTER", "WALK-IN")
PAYMENT_MODES = ("CASH", "BANK", "E-WALLET", "CHEQUE", "CREDIT")
DENOMINATIONS = (1000, 500, 200, 100, 50, 20, 10, 5, 1, 0.25)
```

**Dictionary** – `PACKAGES` maps a package name to its price and bottles, so `PACKAGES["PLUS"]["price"]` gives `10500.0`. Each sale record is also a dictionary:

```python
{"slip_no": "111526-01", "date": "2026-11-15", "customer": "Liza Ramos",
 "package": "PLUS", "quantity": 2, "amount": 20000.0,
 "released": 4, "to_follow": 2, "payment_mode": "CASH", ...}
```

## G. Functions

| Module | Function | Purpose |
|---|---|---|
| `ledger` | `compute_sale` | Computes price, amount, bottles, to follow |
| `ledger` | `next_slip_no` | Builds the next `MMDDYY-NN` slip number |
| `ledger` | `find_sale` | Returns the record with a slip number, or `None` |
| `ledger` | `records_between` | Returns records within a date range |
| `ledger` | `daily_summary` | Totals one day by package and payment mode |
| `ledger` | `cash_on_hand` | Adds up denomination × pieces |
| `ledger` | `cash_status` | Returns BALANCED, OVER by X, or SHORT by X |
| `storage` | `load_sales` | Reads `sales.json` (`[]` if missing, `None` if damaged) |
| `storage` | `save_sales` | Writes all records to `sales.json` |
| `main` | `ask_text`, `ask_whole_number`, `ask_amount`, `ask_choice`, `ask_date` | Ask until the input is valid |
| `main` | `encode_sale`, `view_records`, `update_record`, `delete_record`, `daily_report` | Menu options 1–5 |
| `main` | `main` | Loads records and runs the menu loop |

### `compute_sale`
```python
def compute_sale(package, quantity, discount, released):
    unit_price = PACKAGES[package]["price"]
    price = unit_price - discount
    bottles = PACKAGES[package]["bottles"] * quantity
    return {
        "price": price,
        "amount": price * quantity,
        "bottles": bottles,
        "to_follow": bottles - released,
    }
```
Applies the formulas from Section B and returns the results in a dictionary.

### `next_slip_no`
```python
def next_slip_no(sales, sale_date):
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
```
Uses the **highest** number, not the record count. If slips 01 and 02 exist and 01 is deleted, the next slip is 03, not a second 02.

### `cash_status`
```python
def cash_status(counted, expected):
    difference = round(counted - expected, 2)
    if difference == 0:
        return "BALANCED"
    elif difference > 0:
        return f"OVER by {difference:,.2f}"
    else:
        return f"SHORT by {-difference:,.2f}"
```
`round(..., 2)` removes tiny float errors (like `0.30000000000000004`) so a matching drawer reads BALANCED.

## H. File Handling

Records are stored in `sales.json` as a JSON list of dictionaries. `storage.py` uses Python's `json` module.

```python
def save_sales(sales, file_name=FILE_NAME):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(sales, file, indent=2)
```

```python
def load_sales(file_name=FILE_NAME):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return None
    # also returns None if the data is not a list of valid records
    ...
    return records
```

- The program saves after every change (new sale, release, reference change, delete).
- **File missing** (first run): start with an empty list.
- **File damaged:** show an error and stop, so the damaged file is not overwritten.

## I. Error Handling

| Error | How it is handled | Message |
|---|---|---|
| Letters for a number (`two`) | `except ValueError` | `Please type a whole number.` |
| Number out of range (`0`) | `if` range check | `Please type a number from 1 to 100.` |
| Letters for an amount (`abc`) | `except ValueError` | `Please type an amount, like 500 or 250.50.` |
| Amount out of range (`20000`, `nan`) | `if 0 <= amount <= highest` | `Please type an amount from 0 to 10,500.00.` |
| Fake date (`2026-02-30`) | `except ValueError` | `Not a real date. Example: 2026-11-15` |
| Blank required field | `if` check | `This field is required.` |
| Menu choice not 1–6 | `else` branch | `Invalid choice. Type a number from 1 to 6.` |
| Slip not found | `find_sale` returns `None` | `No record with that slip number.` |
| `sales.json` missing | `except FileNotFoundError` | Starts with 0 records |
| `sales.json` damaged | `except json.JSONDecodeError` + checks | `Cannot open sales.json ...`, then stops |
| `sales.json` read-only | `except OSError` | `Could not save to sales.json ...` |
| Ctrl+C / Ctrl+Z | `except (KeyboardInterrupt, EOFError)` | `Program stopped. All saved records are in sales.json.` |

Example input helper:

```python
def ask_whole_number(prompt, lowest, highest):
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("  Please type a whole number.")
            continue
        if number < lowest or number > highest:
            print(f"  Please type a number from {lowest} to {highest}.")
        else:
            return number
```

The program does not use a bare `except:`, so real bugs still show a traceback and can be fixed.

## J. Testing and Debugging

T01–T07 and T12 start with no `sales.json`. T08–T09 start from a copy of `sample_sales.json`.

*(Student: fill in Actual result and Status from your own runs. Remove this line before submitting.)*

| ID | Scenario | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T01 | Normal sale | `2026-11-15`, `Liza Ramos`, DISTRIBUTOR, PLUS, qty `2`, discount `500`, released `4`, CASH, `y` | Slip `111526-01`, amount 20,000.00, 2 to follow | | |
| T02 | Slip after a delete | Add slips 01 and 02, delete 01, add one more | New slip is `111526-03` | | |
| T03 | Discount = full price | RETAIL, qty `1`, discount `2800` | Amount 0.00, allowed | | |
| T04 | Release all, then one more | Release `3` of 3, then option 3 again | `Bottles still to follow: 0`, then `All bottles on this slip are already released.` | | |
| T05 | Invalid quantity | `0`, then `two` | `Please type a number from 1 to 100.`, then `Please type a whole number.` | | |
| T06 | Fake date | `2026-02-30` | `Not a real date. Example: 2026-11-15` | | |
| T07 | `nan` discount | PLUS, discount `nan` | `Please type an amount from 0 to 10,500.00.` | | |
| T08 | Daily report | Option 5, `2026-11-15`, `n` | 3 sales; CASH 9,500.00; E-WALLET 15,500.00; TOTAL 25,000.00; 3 to follow | | |
| T09 | Cash short | Same, `y`, 9 × 1,000, 0 for the rest | `SHORT by 500.00` | | |
| T10 | No file | Delete `sales.json`, run, `6` | `Loaded 0 sale record(s) ...` | | |
| T11 | Damaged file | Put `[{"slip_no": "111526-01",` in `sales.json`, run | `Cannot open sales.json ...`; file unchanged | | |
| T12 | Restart | After T01, exit, run again, view the day | `Loaded 1 ...`, slip `111526-01` listed | | |

### Debugging: `nan` accepted as a discount
*(Found during an AI-assisted review.)*

- **Symptom:** typing `nan` as the discount gave `Amount due: nan`, and the sale could be saved.
- **Cause:** `float("nan")` does not raise an error, and every comparison with `nan` is False, so `if amount < 0 or amount > highest` let it through.
- **Fix:** check the good case instead: `if 0 <= amount <= highest: return amount`.
- **Check:** `nan` now shows the error message; normal amounts still work (T01, T07).

## K. Conclusion

The Daily Sales Ledger replaces paper slips and calculator totals. It computes each sale, numbers the slips, tracks bottles owed, and gives the cashier daily totals and a cash check. It uses a list for records, tuples for fixed choices, dictionaries for packages and sales, and three modules to separate the menu, the math, and the file.

**Possible improvements:** search by customer name and sort by date; save each daily report to a text file.

## L. References

- Python 3 documentation (`json`, `datetime`, Errors and Exceptions): https://docs.python.org/3/
- CS 26 class reports: Lists, Dictionaries, Functions, Tuples, Modular Programming.
- CS 26 Exam 2 sample documentation (Simple Inventory Tracker).

**Acknowledgment**  
*(Student: edit this so it states what happened.)* I used Claude, an AI assistant by Anthropic, to help plan, draft code, and draft this documentation. I ran the tests in Section J myself.
