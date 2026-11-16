# CS 26 Exam 2 – Technical Documentation
## Daily Sales Ledger

**Student:** Surname, Firstname  
**Course:** CS 26 – Software Development Fundamentals  
**Program type:** Python console program  
**Coverage:** Lists, tuples, dictionaries, functions, modules, file handling, error handling, testing, and debugging

---

## A. Program Title and Overview

**Program name:** Daily Sales Ledger

The Daily Sales Ledger is a Python console program for the sales counter of a small NutriPlus supplement distributor. The **encoder** records each sale. At closing, the **cashier** reviews the records, counts the cash drawer, and prints the daily report.

The program numbers each order slip and computes the amount due. It tracks bottles a customer will pick up later ("to follow"). It totals the day's sales by package and by payment mode, and tells the cashier if the drawer is short or over. The program saves every record to a file and loads it again on the next run.

## B. Problem Description

### Current problem
The encoder writes each sale on a paper order slip. At closing, the cashier adds the slips on a calculator, sorts them by payment mode, and counts the drawer. This causes four problems:

1. **Wrong amounts.** The encoder computes discounts by hand and can write the wrong total.
2. **Slow report.** The cashier adds package and payment totals one slip at a time.
3. **Lost "to follow" bottles.** When stock runs short, the customer takes some bottles now and the rest later. Paper notes on the remaining bottles get lost.
4. **Unclear cash count.** The cashier has no quick way to see if the drawer is short or over.

The program checks each entry, does the math, and prints the day's totals on request.

### Inputs
| Input | Example | Rule |
|---|---|---|
| Date of sale | `2026-11-15` | Must be a real date in `YYYY-MM-DD` form. Blank means today. |
| Customer name | `Liza Ramos` | Required |
| Member type | `DISTRIBUTOR` | One of: DISTRIBUTOR, STOCKIST, CENTER, WALK-IN |
| Package | `PLUS` | One of: STARTER, PLUS, PREMIUM, RETAIL |
| Quantity | `2` | Whole number, 1 or more |
| Discount per package | `500` | From 0 up to the package's unit price |
| Bottles released now | `4` | From 0 up to the total bottles in the sale |
| Payment mode | `CASH` | One of: CASH, BANK, E-WALLET, CHEQUE, CREDIT |
| Reference number | `BNK-20441` | Required when the payment is not CASH |
| Remarks | `promo price` | Optional |
| Cash count | `9` pieces of 1,000 | Whole number, 0 or more, for each denomination |

### Processing
- **Validate** each input against the rules above. Ask again when the entry breaks a rule.
- **Discounted price** = unit price − discount
- **Sales amount** = discounted price × quantity
- **Total bottles** = bottles per package × quantity
- **Bottles to follow** = total bottles − bottles released
- **Order slip number** = `MMDDYY-NN`. NN is the highest number already used that day, plus 1.
- **Daily totals**: add the sales amounts of one date, grouped by package and by payment mode.
- **Cash on hand** = sum of (denomination × number of pieces)
- **Cash status** = compare cash on hand with total CASH sales: BALANCED, SHORT, or OVER.

**Worked example:** 2 × PLUS (unit price 10,500.00, 3 bottles each) with a 500.00 discount and 4 bottles released:
discounted price = 10,500 − 500 = **10,000.00**; sales = 10,000 × 2 = **20,000.00**; bottles = 3 × 2 = **6**; to follow = 6 − 4 = **2**.

### Outputs
- A confirmation of each sale, showing its order slip number, amount, and bottles to follow
- A table of sale records for a chosen date range
- A daily sales report: totals by package, totals by payment mode, grand total, and bottles still to follow
- The cash count result: BALANCED, SHORT by an amount, or OVER by an amount
- The file `sales.json`, which keeps all records between program runs

## C. Program Objectives

1. Compute the discounted price, sales amount, and bottles to follow of a sale. Example: 2 × PLUS with a 500.00 discount gives 20,000.00.
2. Give each sale a unique order slip number (`MMDDYY-NN`), even after the user deletes a slip.
3. Let the user view records by date range, release bottles to follow, and delete a record.
4. Print a daily report with totals by package and payment mode, and compare the counted cash with cash sales.
5. Save records to `sales.json`, load them at start, and keep running when the file is missing or damaged.

### Program design

I wrote this design before writing any code.

#### Main menu flowchart

```text
        +-------+
        | START |
        +-------+
            |
            v
 +-----------------------+
 | Load records from     |
 | sales.json            |
 +-----------------------+
            |
            v
 +-----------------------+      file damaged     +------------------------+
 | Was the file read     |---------------------->| Show error message,    |
 | correctly?            |                       | END (do not overwrite) |
 +-----------------------+                       +------------------------+
            | yes (or file missing = empty list)
            v
 +-----------------------+
 | Show menu, read       |<------------------------------+
 | choice 1-6            |                               |
 +-----------------------+                               |
            |                                            |
            v                                            |
   +-----------------+   1  +-------------------+        |
   | Which choice?   |----->| Encode a sale     |------->|
   |                 |   2  +-------------------+        |
   |                 |----->| View records      |------->|
   |                 |   3  +-------------------+        |
   |                 |----->| Update a record   |------->|
   |                 |   4  +-------------------+        |
   |                 |----->| Delete a record   |------->|
   |                 |   5  +-------------------+        |
   |                 |----->| Daily report      |------->|
   |                 |other +-------------------+        |
   |                 |----->| "Invalid choice"  |------->+
   +-----------------+      +-------------------+
            | 6
            v
        +-------+
        |  END  |
        +-------+
```

#### Pseudocode: main program
```text
records <- load records from sales.json
IF the file is damaged THEN
    display error and stop
REPEAT
    display menu
    choice <- input
    IF choice = 1 THEN encode a sale
    ELSE IF choice = 2 THEN view records
    ELSE IF choice = 3 THEN update a record
    ELSE IF choice = 4 THEN delete a record
    ELSE IF choice = 5 THEN show daily report
    ELSE IF choice = 6 THEN stop repeating
    ELSE display "Invalid choice"
UNTIL choice = 6
```

#### Pseudocode: encode a sale
```text
ask date, customer name, member type, package          (repeat each until valid)
unit_price <- price of package
ask quantity                                           (repeat until quantity >= 1)
ask discount                                           (repeat until 0 <= discount <= unit_price)
total_bottles <- bottles per package * quantity
ask bottles released                                   (repeat until 0 <= released <= total_bottles)
ask payment mode
IF payment mode is not CASH THEN ask reference number  (required)
ask remarks                                            (optional)
discounted_price <- unit_price - discount
sales_amount <- discounted_price * quantity
to_follow <- total_bottles - released
slip_no <- next slip number for the date
display summary and ask "Save this sale?"
IF yes THEN add record to records and save to sales.json
```

#### Pseudocode: next order slip number
```text
prefix <- MMDDYY of the date
highest <- 0
FOR each record in records
    IF record date = date AND its number after "-" > highest THEN
        highest <- that number
next_slip <- prefix + "-" + (highest + 1) written with 2 digits
```

#### Pseudocode: daily report and cash count
```text
ask report date
FOR each record with that date
    add sales amount to its package total
    add sales amount to its payment mode total
    add bottles to follow to the to-follow total
display package totals, payment totals, grand total, bottles to follow
IF user wants to count cash THEN
    cash_on_hand <- 0
    FOR each denomination (1000, 500, 200, 100, 50, 20, 10, 5, 1, 0.25)
        ask number of pieces
        cash_on_hand <- cash_on_hand + denomination * pieces
    difference <- cash_on_hand - CASH payment total
    IF difference = 0 THEN display "BALANCED"
    ELSE IF difference > 0 THEN display "OVER by" difference
    ELSE display "SHORT by" (-difference)
```

## D. Program Requirements and Features

| Feature | Menu option | Status |
|---|---|---|
| Main menu that rejects choices outside 1–6 | — | Implemented |
| Encode a sale with validation and automatic computation | 1 | Implemented |
| Automatic order slip number (`MMDDYY-NN`) | 1 | Implemented |
| View records by date range | 2 | Implemented |
| Release bottles to follow / change reference number | 3 | Implemented |
| Delete a record (asks to confirm first) | 4 | Implemented |
| Daily sales report by package and payment mode | 5 | Implemented |
| Cash count with BALANCED / SHORT / OVER result | 5 | Implemented |
| Save and load records with `sales.json` | — | Implemented |

**Assumptions**
- One encoder uses the program at a time, on one computer.
- You run `main.py` from inside the `cs26-project` folder, so `sales.json` lands next to the code.
- One sale holds 1 to 100 packages. Larger orders go on separate slips.
- The cash count accepts 0 to 10,000 pieces per denomination.
- Only CASH payments go into the drawer. The cash count ignores bank, e-wallet, cheque, and credit payments.
- Prices are in Philippine pesos. The package catalog below is sample data:

| Package | Unit price | Bottles per package |
|---|---:|---:|
| STARTER | 3,500.00 | 1 |
| PLUS | 10,500.00 | 3 |
| PREMIUM | 17,500.00 | 5 |
| RETAIL | 2,800.00 | 1 |

**Limitations**
- If saving fails (for example, `sales.json` is read-only), the change stays in memory only. Closing the program loses it.
- A sale has one package type. A customer buying two package types needs two slips.
- View lists records in the order you encoded them, not sorted by date.
- `load_sales` checks field names, package names, and payment modes in `sales.json`, but trusts the numbers. A hand-edited negative quantity loads without complaint.
- The records table leaves out member type, discount, reference number, and remarks so it fits one line.

## E. Program Structure and Modules
```text
cs26-project/
├── main.py             # run this: menu, input, output
├── ledger.py           # data and calculations, no input() or print()
├── storage.py          # reads and writes sales.json
├── sales.json          # created on the first save; holds the records
└── sample_sales.json   # 6 sample records for testing and demos
```

- **`main.py`** talks to the user. It holds the input helpers, the table printer, the five menu actions, and the menu loop. `main()` loads the `sales` list at start.
- **`ledger.py`** holds the fixed choices, the package catalog, and the functions that compute: totals, slip numbers, searches, and the cash check.
- **`storage.py`** holds `load_sales()` and `save_sales()`. Only this module opens files.
- **`sales.json`** keeps the records between runs. To start with sample data, copy `sample_sales.json` to `sales.json`.

`main.py` imports the module by name and calls its parts with a dot:

```python
import ledger
import storage

sales = storage.load_sales()
result = ledger.compute_sale(package, quantity, discount, released)
slip_no = ledger.next_slip_no(sales, sale_date)
member_type = ask_choice("Member type:", ledger.MEMBER_TYPES)
```

The `ledger.` prefix shows where each name comes from. Python finds `ledger.py` because it sits in the same folder as `main.py`.

I named the module `ledger.py` instead of `sales.py`. `main.py` already uses `sales` for the list of records, and `import sales` would clash with it.

The split keeps the math apart from the screen. To check a formula, I can call `ledger.compute_sale(...)` without typing through the whole menu.

### Menu loop
`main()` repeats until the user picks 6. The program compares the choice as text (`"1"`, `"2"`, …) instead of converting it with `int()`. If you type a letter, the program shows "Invalid choice" and the menu again, with no crash.

```python
choice = input("Choose (1-6): ").strip()

if choice == "1":
    encode_sale(sales)
...
elif choice == "6":
    print("Goodbye.")
    break
else:
    print("Invalid choice. Type a number from 1 to 6.")
```

`.strip()` removes spaces around the answer, so `" 6 "` still counts as 6.

## F. Data Structures

### List
`sales` holds the sale records. `main()` fills it from `sales.json` at start. The encoder adds one record per sale with `append()`, and delete removes one with `remove()`.

```python
sales = storage.load_sales()      # [] on the first run
...
sales.append(record)              # encode_sale
sales.remove(record)              # delete_record
```

A list fits because the number of sales changes during the day.

A second tuple, `REQUIRED_FIELDS` in `storage.py`, lists the fields every loaded record must have:

```python
REQUIRED_FIELDS = ("slip_no", "date", "customer", "package", "quantity",
                   "amount", "released", "to_follow", "payment_mode")
```

### Tuple
Three tuples in `ledger.py` hold the fixed choices: member types, payment modes, and cash denominations.

```python
MEMBER_TYPES = ("DISTRIBUTOR", "STOCKIST", "CENTER", "WALK-IN")
PAYMENT_MODES = ("CASH", "BANK", "E-WALLET", "CHEQUE", "CREDIT")
DENOMINATIONS = (1000, 500, 200, 100, 50, 20, 10, 5, 1, 0.25)
```

These values stay the same while the program runs. A tuple is immutable, so no part of the program can change them by mistake.

### Dictionary
`PACKAGES` in `ledger.py` maps each package name to its price and bottle count.

```python
PACKAGES = {
    "STARTER": {"price": 3500.0, "bottles": 1},
    "PLUS": {"price": 10500.0, "bottles": 3},
    "PREMIUM": {"price": 17500.0, "bottles": 5},
    "RETAIL": {"price": 2800.0, "bottles": 1},
}
```

The program looks up a package by name: `PACKAGES["PLUS"]["price"]` gives `10500.0`. With a list, you would have to remember that PLUS sits at index 1. Each sale record is also a dictionary:

```python
{"slip_no": "111526-01", "date": "2026-11-15", "customer": "Liza Ramos",
 "member_type": "DISTRIBUTOR", "package": "PLUS", "quantity": 2,
 "discount": 500.0, "price": 10000.0, "amount": 20000.0, "bottles": 6,
 "released": 4, "to_follow": 2, "payment_mode": "CASH",
 "reference_no": "", "remarks": ""}
```

Code reads `record["to_follow"]` instead of a position number, and `update_record` can change one field with `record["released"] += count`.

## G. Functions

**`ledger.py`: calculations**

| Function | Parameters | Returns | Purpose |
|---|---|---|---|
| `compute_sale` | `package`, `quantity`, `discount`, `released` | `dict` | Computes price, amount, bottles, and bottles to follow |
| `next_slip_no` | `sales`, `sale_date` | `str` | Builds the next `MMDDYY-NN` slip number |
| `find_sale` | `sales`, `slip_no` | `dict` or `None` | Returns the record with that slip number |
| `records_between` | `sales`, `date_from`, `date_to` | `list` | Returns the records dated within the range |
| `daily_summary` | `sales`, `report_date` | `dict` | Totals one day's sales by package and payment mode |
| `cash_on_hand` | `counts` | `float` | Adds up denomination × pieces |
| `cash_status` | `counted`, `expected` | `str` | Returns BALANCED, OVER by X, or SHORT by X |

**`storage.py`: file handling**

| Function | Parameters | Returns | Purpose |
|---|---|---|---|
| `load_sales` | `file_name` (default `"sales.json"`) | `list`, or `None` if damaged | Reads the records; a missing file gives `[]` |
| `save_sales` | `sales`, `file_name` (default `"sales.json"`) | `None` | Writes all records as JSON |

**`main.py`: input, output, and menu**

| Function | Parameters | Returns | Purpose |
|---|---|---|---|
| `save` | `sales` | `None` | Calls `storage.save_sales` and reports success or failure |
| `ask_text` | `prompt` | `str` | Asks until the user types something |
| `ask_whole_number` | `prompt`, `lowest`, `highest` | `int` | Asks until the user types a whole number in range |
| `ask_amount` | `prompt`, `highest` | `float` | Asks until the user types an amount from 0 to `highest` |
| `ask_choice` | `title`, `options` | one item of `options` | Shows a numbered list and returns the picked item |
| `ask_date` | `prompt` | `str` (`YYYY-MM-DD`) | Asks for a real date; blank gives today |
| `print_records` | `rows` | `None` | Prints records as a table |
| `encode_sale` | `sales` | `None` | Asks for a sale, shows a summary, adds it to `sales` on "y" |
| `view_records` | `sales` | `None` | Shows records between two dates and their total amount |
| `update_record` | `sales` | `None` | Releases bottles to follow or changes the reference number |
| `delete_record` | `sales` | `None` | Removes a record after the user types "y" |
| `daily_report` | `sales` | `None` | Prints the report and runs the cash count |
| `show_menu` | none | `None` | Prints the six menu options |
| `main` | none | `None` | Loads the records, then runs the menu loop |

### Excerpt 1: `compute_sale`

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

The function reads the unit price and bottle count from `PACKAGES`, then applies the formulas from Section B. It returns the four results in one dictionary, so `encode_sale` can read `result["amount"]` by name. For 2 × PLUS with a 500 discount and 4 bottles released, it returns a price of 10,000.0, an amount of 20,000.0, 6 bottles, and 2 to follow.

`compute_sale` does no input or printing. I can call it with any numbers and check the answer by hand.

### Excerpt 2: `next_slip_no`

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

Slicing builds the prefix: for `"2026-11-15"`, `[5:7]` gives `"11"`, `[8:10]` gives `"15"`, and `[2:4]` gives `"26"`. The loop visits each record from the same date. `split("-")` cuts `"111526-02"` into `["111526", "02"]`, and `int()` turns `"02"` into 2. The function keeps the highest number and adds 1. The last `if` adds a leading zero, so slip 3 prints as `03`.

The function uses the highest number, not the count of records. Suppose the day has slips 01 and 02, and the user deletes 01. A count would give 02 again. The highest number gives 03.

### Excerpt 3: `records_between`

```python
def records_between(sales, date_from, date_to):
    rows = []
    for record in sales:
        if date_from <= record["date"] <= date_to:
            rows.append(record)
    return rows
```

The dates are text in `YYYY-MM-DD` form. Python compares text character by character, and this form puts the year first, so `"2026-11-14" < "2026-11-15"` matches the calendar. The loop copies each matching record into `rows`. `view_records` in `main.py` first rejects a From date after the To date, then calls this function, adds up the amounts, and prints the table. If `rows` comes back empty, it prints "No sales in that date range."

### Excerpt 4: `daily_summary`

```python
by_package = {}
for name in PACKAGES:
    by_package[name] = {"quantity": 0, "amount": 0.0}
...
for record in sales:
    if record["date"] == report_date:
        count += 1
        total += record["amount"]
        to_follow += record["to_follow"]
        by_package[record["package"]]["quantity"] += record["quantity"]
        by_package[record["package"]]["amount"] += record["amount"]
        by_payment[record["payment_mode"]] += record["amount"]
```

The first loop gives each package a starting total of zero, so the report lists PLUS with 0.00 even on a day nobody bought it. The second loop reads each record from the report date and adds it in three places. `record["package"]` names the right row: a PREMIUM sale adds to `by_package["PREMIUM"]`. The function returns all the totals in one dictionary for `daily_report` to print.

### Excerpt 5: `cash_status`

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

Floats can carry tiny errors: `0.1 + 0.2` gives `0.30000000000000004`. `round(..., 2)` cuts the difference to centavos before the `if` checks it, so a matching drawer reads BALANCED. A drawer of 9,000.00 against 9,500.00 cash sales gives a difference of -500, and the function returns `SHORT by 500.00`.

`update_record` and `delete_record` both start with `find_sale`. It returns the matching dictionary, or `None` when no slip matches, so each caller checks `if record is None` before using it. Deleting uses `sales.remove(record)` and asks for "y" first, because the user cannot undo it.

### Input helpers
`encode_sale` never calls `int()` or `float()` itself. It calls helpers like `ask_whole_number`, which loop until the answer passes:

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

If you type `two`, `int()` raises `ValueError`. The `except` prints a message, and `continue` asks again. If you type `0` for quantity, the range check catches it. The same helper handles quantity (1–100), bottles released (0 to total bottles), and menu picks inside `ask_choice`.

## H. File Handling

| Item | Detail |
|---|---|
| File name | `sales.json`, in the same folder as `main.py` |
| Format | JSON text: a list of sale dictionaries |
| Module | `storage.py` (uses Python's built-in `json` module) |
| Modes | `"r"` to read at start, `"w"` to rewrite after each change |
| Persistence | Yes. Records survive closing and reopening the program. |

Part of a saved file:

```json
[
  {
    "slip_no": "111526-01",
    "date": "2026-11-15",
    "customer": "Liza Ramos",
    "package": "PLUS",
    "quantity": 2,
    ...
  }
]
```

JSON matches Python's structures: a JSON list loads as a Python list, and each `{...}` loads as a dictionary. You can open the file in Notepad and read it.

### Saving

```python
def save_sales(sales, file_name=FILE_NAME):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(sales, file, indent=2)
```

`"w"` mode creates the file if it does not exist, or empties it and writes the whole list again. `json.dump` turns the list into text, and `indent=2` puts each field on its own line. `with open(...)` closes the file when the block ends, even if an error happens inside it.

`main.py` calls `save(sales)` after each change: a new sale, a bottle release, a new reference number, or a delete. You never need a separate "save" step.

### Loading

```python
def load_sales(file_name=FILE_NAME):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return None

    if type(records) != list:
        return None
    for record in records:
        if type(record) != dict:
            return None
        for field in REQUIRED_FIELDS:
            if field not in record:
                return None
        if record["package"] not in ledger.PACKAGES:
            return None
        if record["payment_mode"] not in ledger.PAYMENT_MODES:
            return None
    return records
```

`main()` calls this once, at start. It has three results:

- **File missing:** `open()` raises `FileNotFoundError`. That happens on the first run, so the function returns an empty list and you start fresh.
- **File damaged:** `json.load()` raises `json.JSONDecodeError` when the text is not valid JSON, for example a file cut off mid-save. The function also rejects valid JSON in the wrong shape: not a list, a record missing a field from `REQUIRED_FIELDS`, or a package or payment mode the program does not know. In each case it returns `None`.
- **File good:** it returns the list.

When `main()` gets `None`, it prints "Cannot open sales.json: the file is damaged or not in the right format." and stops. It does not start with an empty list, because the first save would then overwrite the damaged file and destroy whatever records you could still recover from it.

## I. Error Handling

### Expected errors

| Expected error | Where | How the program catches it | What the user sees |
|---|---|---|---|
| Letters typed for a whole number (`two`) | `ask_whole_number` | `except ValueError` around `int()` | `Please type a whole number.` and the question again |
| Number out of range (quantity `0`, released `7` of 6) | `ask_whole_number` | `if` range check | `Please type a number from 1 to 100.` |
| Text or `nan` typed for an amount | `ask_amount` | `except ValueError` around `float()`, then `if 0 <= amount <= highest` | `Please type an amount from 0 to 10,500.00.` |
| Date that does not exist (`2026-02-30`) | `ask_date` | `except ValueError` around `strptime()` | `Not a real date. Example: 2026-11-15` |
| Blank required field | `ask_text` | `if text != ""` | `This field is required.` |
| Menu choice outside 1–6 (`7`, `abc`) | `main` | compares text, `else` branch | `Invalid choice. Type a number from 1 to 6.` |
| Slip number not found | `update_record`, `delete_record` | `find_sale` returns `None` | `No record with that slip number.` |
| `sales.json` missing | `load_sales` | `except FileNotFoundError` | Starts with 0 records |
| `sales.json` damaged | `load_sales` | `except json.JSONDecodeError`, plus shape checks | `Cannot open sales.json ...`, then the program stops |
| `sales.json` read-only | `save` | `except OSError` | `Could not save to sales.json ...` |
| Ctrl+C, or Ctrl+Z then Enter | bottom of `main.py` | `except (KeyboardInterrupt, EOFError)` | `Program stopped. All saved records are in sales.json.` |

### Input errors vs programming errors

The handlers above cover **input errors**: mistakes the user or the file can make. Each `except` names one exception type and sits where the program can give a useful message, usually inside a loop that asks again.

```python
def ask_whole_number(prompt, lowest, highest):
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("  Please type a whole number.")
            continue
        ...
```

The program has no bare `except:` and no `except Exception:`. A **programming error**, such as a misspelled dictionary key, still stops the program with a traceback. A hidden bug would print wrong totals with no warning. A traceback shows the line number, so I can find and fix the bug.

My error-handling review found this kind of crash. A record in `sales.json` without a `"released"` field crashed `update_record` with `KeyError: 'released'`. A record with package `"GOLD"` crashed the report with `KeyError: 'GOLD'`. I did not add a `try` around those lines. I fixed the cause: `load_sales` now rejects such a file at start, before any code reads the bad record.

### Stopping the program safely

```python
try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\nProgram stopped. All saved records are in sales.json.")
```

Ctrl+C raises `KeyboardInterrupt`. Ctrl+Z then Enter on Windows ends the input, and the next `input()` raises `EOFError`. The tuple after `except` catches both. The program saves after each change, so stopping it this way loses only a sale you had not confirmed yet.

## J. Testing, Debugging, and Results

### How I tested
I tested each feature in the milestone where I built it and logged the raw terminal output in `devlog.md`. The table below picks 12 cases from that log, covering normal use, boundaries, invalid input, and file failures. T01–T07 and T12 start with no `sales.json`. T08 and T09 start from a copy of `sample_sales.json`.

*(Student: fill in Actual result and Status from your own runs in `devlog.md`. Remove this line before submitting.)*

### Test cases

| Test ID | Scenario | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T01 | Normal sale | `2026-11-15`, `Liza Ramos`, DISTRIBUTOR, PLUS, qty `2`, discount `500`, released `4`, CASH, `y` | Slip `111526-01`, amount 20,000.00, 2 to follow, `Saved to sales.json.` | | |
| T02 | New slip after a delete | On 2026-11-15, add slips 01 and 02, delete 01, add one more | New slip is `111526-03`, not a second `02` | | |
| T03 | Discount equal to full price (boundary) | RETAIL, qty `1`, discount `2800` | Amount 0.00, sale allowed | | |
| T04 | Release all bottles to follow, then one more (boundary) | Slip with 3 to follow: option 3, release `3`; option 3 again | `Bottles still to follow: 0`, then `All bottles on this slip are already released.` | | |
| T05 | Invalid quantity | Quantity `0`, then `two` | `Please type a number from 1 to 100.`, then `Please type a whole number.` | | |
| T06 | Date that does not exist | Date `2026-02-30` | `Not a real date. Example: 2026-11-15` | | |
| T07 | `nan` as discount | PLUS, discount `nan` | `Please type an amount from 0 to 10,500.00.` | | |
| T08 | Daily report | Sample data, option 5, `2026-11-15`, `n` | 3 transactions; CASH 9,500.00; E-WALLET 15,500.00; TOTAL 25,000.00; 3 to follow | | |
| T09 | Cash drawer short | Same report, `y`, 9 pieces of 1,000 and 0 for the rest | `Cash counted: 9,000.00`, `Result: SHORT by 500.00` | | |
| T10 | First run, no file | Delete `sales.json`, run, `6` | `Loaded 0 sale record(s) from sales.json.` | | |
| T11 | Damaged file | Replace `sales.json` with `[{"slip_no": "111526-01",`, run | `Cannot open sales.json: ...`; program stops; file text unchanged | | |
| T12 | Records survive a restart | After T01, exit, run again, view `2026-11-15` to `2026-11-15` | `Loaded 1 ...`, slip `111526-01` listed | | |

### Debugging

**Defect: the program accepted `nan` as a discount.**
*(Found during an AI-assisted review of the error handling.)*

- **Symptom:** At "Discount per package" I typed `nan`. The summary showed `Price after discount: nan` and `Amount due: nan`, and the program let me save the sale.
- **Cause:** `float("nan")` does not raise `ValueError`; it returns a special "not a number" value. Every comparison with it is False. The old check was:

  ```python
  if amount < 0 or amount > highest:
      print(f"  Please type an amount from 0 to {highest:,.2f}.")
  else:
      return amount
  ```

  Both `nan < 0` and `nan > highest` are False, so the code went to `else` and returned `nan`.
- **Correction:** I flipped the check to test the good case:

  ```python
  if 0 <= amount <= highest:
      return amount
  print(f"  Please type an amount from 0 to {highest:,.2f}.")
  ```

  `0 <= nan` is False, so `nan` now reaches the error message.
- **Verification:** I reran the encode steps. `nan` printed `Please type an amount from 0 to 10,500.00.` and asked again. `inf`, `20000`, and `-1` still got the same message, and `500` still gave an amount of 20,000.00 (T01, T07).

**Other checks.** After I split the code into modules (milestone 5), I ran one long input script through the program before and after the split. Both runs printed the same 380 lines, which showed the move changed no behaviour. `devlog.md` lists the other issues I found, with the fix and check for each.

## K. Conclusion

The Daily Sales Ledger replaces paper slips and calculator totals at a supplement sales counter. The encoder records a sale in one pass, and the program computes the amount, numbers the slip, and tracks bottles still owed. At closing, the cashier gets totals by package and payment mode and a BALANCED, SHORT, or OVER result for the cash drawer. Records stay in `sales.json` between runs, and the program refuses to overwrite a damaged file.

The code uses a list for the records, tuples for fixed choices, and dictionaries for the package catalog and each sale. Three modules split the work: `main.py` talks to the user, `ledger.py` computes, and `storage.py` reads and writes the file.

**Limitations:** one package type per slip, no sorting or search in the record view, and no check on the numbers inside a hand-edited `sales.json`.

**Possible improvements**
1. Search records by customer name, and sort the view by date and slip number.
2. Save each daily report to a text file (for example `report_2026-11-15.txt`) so the cashier can print or email it.

## L. References
- Python Software Foundation. *Python 3 documentation*: `json` module, `datetime` module, and "Errors and Exceptions" tutorial. https://docs.python.org/3/
- CS 26 class reports: Python Lists (G1), Python Dictionaries (G3), Functions (G4), Python Tuples, Modular Programming in Python (G6).
- CS 26 Exam 2 sample documentation (Simple Inventory Tracker), used as a model for structure.

**Acknowledgment of assistance**
*(Student: edit this so it states what happened.)* I used Claude, an AI assistant by Anthropic, to help plan the milestones, draft the Python code, and draft parts of this documentation. The AI-assisted review found the defects marked as such in `devlog.md` and Section J. I ran the tests in Section J myself and recorded the actual results from my own runs.
