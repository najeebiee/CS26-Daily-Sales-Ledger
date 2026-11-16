# Daily Sales Ledger
# main.py: menu, input, and output. Run this file to start the program.
# Uses ledger.py for calculations and storage.py for sales.json.

import datetime
import ledger
import storage


# ---------- Input helpers ----------
# Each helper keeps asking until the answer is valid.

def ask_text(prompt):
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("  This field is required.")


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


def ask_amount(prompt, highest):
    while True:
        try:
            amount = float(input(prompt))
        except ValueError:
            print("  Please type an amount, like 500 or 250.50.")
            continue
        # Check that the amount IS in range. float("nan") fails every
        # comparison, so "nan" ends up at the error message too.
        if 0 <= amount <= highest:
            return amount
        print(f"  Please type an amount from 0 to {highest:,.2f}.")


def ask_choice(title, options):
    # Show the options as a numbered list and return the one picked.
    print(title)
    for index, option in enumerate(options):
        print(f"  {index + 1}. {option}")
    pick = ask_whole_number("Choose: ", 1, len(options))
    return options[pick - 1]


def ask_date(prompt):
    while True:
        text = input(prompt + " (YYYY-MM-DD, blank = today): ").strip()
        if text == "":
            return str(datetime.date.today())
        try:
            # strptime() fails with ValueError if the date does not exist.
            parsed = datetime.datetime.strptime(text, "%Y-%m-%d")
            # Rewrite the date with 2-digit month and day, e.g. 2026-1-5 -> 2026-01-05.
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            print("  Not a real date. Example: 2026-11-15")


# ---------- Output helpers ----------

def save(sales):
    # Write all records to sales.json after every change.
    try:
        storage.save_sales(sales)
        print("Saved to sales.json.")
    except OSError:
        # OSError covers PermissionError, e.g. the file is read-only.
        print("Could not save to sales.json. Check that the file is not read-only.")


def print_records(rows):
    # Print records as a table. :<10 pads text to 10 characters, :>12 right-aligns.
    print()
    print(f"{'Slip No':<10} {'Date':<10} {'Customer':<16} {'Package':<8} {'Qty':>3} "
          f"{'Amount':>12} {'Payment':<9} {'Follow':>6}")
    print("-" * 82)
    for record in rows:
        print(f"{record['slip_no']:<10} {record['date']:<10} {record['customer'][:16]:<16} "
              f"{record['package']:<8} {record['quantity']:>3} {record['amount']:>12,.2f} "
              f"{record['payment_mode']:<9} {record['to_follow']:>6}")


# ---------- Menu actions ----------

def encode_sale(sales):
    print()
    print("--- ENCODE A SALE ---")
    sale_date = ask_date("Date")
    customer = ask_text("Customer name: ")
    member_type = ask_choice("Member type:", ledger.MEMBER_TYPES)
    package = ask_choice("Package:", list(ledger.PACKAGES.keys()))
    unit_price = ledger.PACKAGES[package]["price"]
    print(f"  Price per package: {unit_price:,.2f}")
    quantity = ask_whole_number("Quantity (1-100): ", 1, 100)
    discount = ask_amount("Discount per package (0 if none): ", unit_price)
    total_bottles = ledger.PACKAGES[package]["bottles"] * quantity
    released = ask_whole_number(f"Bottles released now (0-{total_bottles}): ", 0, total_bottles)
    payment_mode = ask_choice("Payment mode:", ledger.PAYMENT_MODES)
    reference_no = ""
    if payment_mode != "CASH":
        reference_no = ask_text("Reference number: ")
    remarks = input("Remarks (optional): ").strip()

    result = ledger.compute_sale(package, quantity, discount, released)
    slip_no = ledger.next_slip_no(sales, sale_date)

    print()
    print(f"Slip {slip_no} | {customer} | {quantity} x {package}")
    print(f"  Price after discount: {result['price']:,.2f}")
    print(f"  Amount due:           {result['amount']:,.2f}")
    print(f"  Bottles: {result['bottles']} total, {released} released, {result['to_follow']} to follow")

    answer = input("Save this sale? (y/n): ").strip().lower()
    if answer == "y":
        record = {
            "slip_no": slip_no,
            "date": sale_date,
            "customer": customer,
            "member_type": member_type,
            "package": package,
            "quantity": quantity,
            "discount": discount,
            "price": result["price"],
            "amount": result["amount"],
            "bottles": result["bottles"],
            "released": released,
            "to_follow": result["to_follow"],
            "payment_mode": payment_mode,
            "reference_no": reference_no,
            "remarks": remarks,
        }
        sales.append(record)
        print(f"Sale {slip_no} added. Total records: {len(sales)}")
        save(sales)
    else:
        print("Sale cancelled.")


def view_records(sales):
    print()
    print("--- VIEW SALES RECORDS ---")
    date_from = ask_date("From")
    date_to = ask_date("To")
    if date_from > date_to:
        print("The 'From' date is after the 'To' date.")
        return

    rows = ledger.records_between(sales, date_from, date_to)
    if len(rows) == 0:
        print("No sales in that date range.")
        return

    total = 0
    for record in rows:
        total += record["amount"]
    print_records(rows)
    print(f"\n{len(rows)} record(s), total amount {total:,.2f}")


def update_record(sales):
    print()
    print("--- UPDATE A RECORD ---")
    record = ledger.find_sale(sales, ask_text("Slip number: "))
    if record is None:
        print("No record with that slip number.")
        return
    print_records([record])

    action = ask_choice("What do you want to update?",
                        ("Release bottles to follow", "Change reference number", "Cancel"))
    if action == "Release bottles to follow":
        if record["to_follow"] == 0:
            print("All bottles on this slip are already released.")
            return
        count = ask_whole_number(f"Bottles to release (1-{record['to_follow']}): ",
                                 1, record["to_follow"])
        record["released"] += count
        record["to_follow"] -= count
        print(f"Released {count}. Bottles still to follow: {record['to_follow']}")
        save(sales)
    elif action == "Change reference number":
        record["reference_no"] = ask_text("New reference number: ")
        print(f"Reference number is now {record['reference_no']}.")
        save(sales)
    else:
        print("No changes made.")


def delete_record(sales):
    print()
    print("--- DELETE A RECORD ---")
    record = ledger.find_sale(sales, ask_text("Slip number: "))
    if record is None:
        print("No record with that slip number.")
        return
    print_records([record])

    answer = input("Delete this record? This cannot be undone. (y/n): ").strip().lower()
    if answer == "y":
        sales.remove(record)
        print(f"Record {record['slip_no']} deleted.")
        save(sales)
    else:
        print("Record kept.")


def daily_report(sales):
    print()
    print("--- DAILY SALES REPORT ---")
    report_date = ask_date("Report date")
    summary = ledger.daily_summary(sales, report_date)
    if summary["count"] == 0:
        print("No sales on that date.")
        return

    print()
    print(f"Sales on {report_date}: {summary['count']} transaction(s)")
    print()
    print(f"{'Package':<10} {'Qty':>5} {'Amount':>14}")
    for name, totals in summary["by_package"].items():
        print(f"{name:<10} {totals['quantity']:>5} {totals['amount']:>14,.2f}")
    print()
    print(f"{'Payment':<10} {'Amount':>20}")
    for mode, amount in summary["by_payment"].items():
        print(f"{mode:<10} {amount:>20,.2f}")
    print()
    print(f"{'TOTAL':<10} {summary['total']:>20,.2f}")
    print(f"Bottles still to follow: {summary['to_follow']}")

    answer = input("\nCount the cash drawer now? (y/n): ").strip().lower()
    if answer != "y":
        return
    counts = {}
    for value in ledger.DENOMINATIONS:
        counts[value] = ask_whole_number(f"  Pieces of {value:,.2f}: ", 0, 10000)
    counted = ledger.cash_on_hand(counts)
    expected = summary["by_payment"]["CASH"]
    print(f"Cash counted: {counted:,.2f}   Cash sales: {expected:,.2f}")
    print("Result:", ledger.cash_status(counted, expected))


def show_menu():
    print()
    print("===== DAILY SALES LEDGER =====")
    print("1. Encode a sale")
    print("2. View sales records")
    print("3. Update a record")
    print("4. Delete a record")
    print("5. Daily sales report")
    print("6. Exit")


def main():
    # List of dictionaries, one per sale, read from sales.json.
    sales = storage.load_sales()
    if sales is None:
        # Stop here so the damaged file is never overwritten.
        print("Cannot open sales.json: the file is damaged or not in the right format.")
        print("Fix or move the file, then run the program again.")
        return
    print(f"Loaded {len(sales)} sale record(s) from sales.json.")

    while True:
        show_menu()
        # Keep the choice as text, so typing a letter cannot crash the program.
        choice = input("Choose (1-6): ").strip()

        if choice == "1":
            encode_sale(sales)
        elif choice == "2":
            view_records(sales)
        elif choice == "3":
            update_record(sales)
        elif choice == "4":
            delete_record(sales)
        elif choice == "5":
            daily_report(sales)
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Type a number from 1 to 6.")


# Ctrl+C raises KeyboardInterrupt; Ctrl+Z then Enter (end of input) raises EOFError.
# Every change is already saved, so the program can stop without losing records.
try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\nProgram stopped. All saved records are in sales.json.")
