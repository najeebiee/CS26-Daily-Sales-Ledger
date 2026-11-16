# Development Log – Daily Sales Ledger

Raw notes kept while building the program. The test table and debugging
section of the documentation (Section J) are written from these entries.

**How to log each milestone**
- What was built or changed, and which file(s)
- Each test run: the exact input typed and the exact terminal output (copy and paste it, do not retype it)
- Every error or wrong result: the error message, the cause, the fix, and how the fix was checked
- Screenshots go in a `screenshots/` folder; refer to them by filename

---

## Milestone 0 – Problem analysis and design (no code)
**Date:** 2026-11-15

**Done**
- Wrote sections A (overview), B (problem, inputs, processing, outputs), and C (objectives) of the documentation.
- Wrote the program design before coding: main menu flowchart, plus pseudocode for the main program, encoding a sale, the next order slip number, and the daily report with cash count.
- Chose the sample package catalog: STARTER 3,500 / 1 bottle, PLUS 10,500 / 3, PREMIUM 17,500 / 5, RETAIL 2,800 / 1.

**Decisions**
- Order slip number format is `MMDDYY-NN`. NN is the highest number used that day + 1, not "number of records + 1". With the count rule, deleting slip 01 out of 01 and 02 would make the next slip 02 again: a duplicate.
- Non-cash payments require a reference number, so bank or e-wallet payments can be traced.
- Bottles to follow are stored in each record, so a customer's pickup can be updated later (menu option 3).

**Hand-computed check for later testing**
- 2 × PLUS, discount 500, 4 bottles released → price 10,000.00, sales 20,000.00, bottles 6, to follow 2

---

## Milestone 1 – Menu and data setup
**Date:** 2026-11-15

**Done**
- Created `main.py`: tuples `MEMBER_TYPES`, `PAYMENT_MODES`, `DENOMINATIONS`; dictionary `PACKAGES`; empty list `sales`.
- `show_menu()` prints options 1–6. `main()` loops until the user picks 6.
- Choices 1–5 print "not built yet".
- Kept the choice as text, so a letter cannot crash `int()`.

**Test runs** *(run `python main.py`, type each input, paste what the terminal shows)*

| Input | Expected | Actual (paste) |
|---|---|---|
| `1` | `Encode a sale: not built yet.` then the menu again | |
| `7` | `Invalid choice. Type a number from 1 to 6.` | |
| `abc` | `Invalid choice. Type a number from 1 to 6.` (no crash) | |
| *(press Enter only)* | `Invalid choice. Type a number from 1 to 6.` | |
| ` 6 ` *(spaces around)* | `Goodbye.` and the program ends | |

**Errors / fixes**
- *(write any error you hit, or "none observed")*

---

## Milestone 2 – Encode a sale
**Date:** 2026-11-15

**Done**
- Added input helpers: `ask_text`, `ask_whole_number`, `ask_amount`, `ask_choice`, `ask_date`.
- Added `compute_sale` (the formulas) and `next_slip_no` (slip numbering).
- Added `encode_sale`: asks for the sale, shows a summary, adds the record on "y". Menu option 1 now calls it.
- `ask_date` rewrites `2026-1-5` as `2026-01-05`, so slicing in `next_slip_no` reads the right characters.
- Records stay in memory only. Closing the program erases them (file saving comes in milestone 6).

**Test runs** *(choose 1 at the menu, type the inputs in order, paste what the terminal shows)*

| # | Scenario | Inputs in order | Expected | Actual (paste) |
|---|---|---|---|---|
| 2.1 | Normal sale | `2026-11-15`, `Liza Ramos`, `1` (DISTRIBUTOR), `2` (PLUS), `2`, `500`, `4`, `1` (CASH), Enter, `y` | Slip `111526-01`, price 10,000.00, amount 20,000.00, 6 bottles, 2 to follow | |
| 2.2 | Second sale, same date | `2026-11-15`, `Mark Dela Pena`, `2`, `3` (PREMIUM), `1`, `0`, `5`, `2` (BANK), `BNK-1`, Enter, `y` | Slip `111526-02`, amount 17,500.00, 0 to follow | |
| 2.3 | Discount equals full price (boundary) | `2026-11-15`, `Joy Santos`, `4`, `4` (RETAIL), `1`, `2800`, `0`, `1`, Enter, `n` | Amount 0.00, then `Sale cancelled.` | |
| 2.4 | Invalid quantity | at Quantity type `0`, then `two` | `Please type a number from 1 to 100.` then `Please type a whole number.` | |
| 2.5 | Discount too high | PLUS, at Discount type `20000` | `Please type an amount from 0 to 10,500.00.` | |
| 2.6 | Released more than bought | 2 × PLUS, at Bottles released type `7` | `Please type a number from 0 to 6.` | |
| 2.7 | Date that does not exist | at Date type `2026-02-30` | `Not a real date. Example: 2026-11-15` | |
| 2.8 | Bank payment, no reference | pick BANK, press Enter at Reference number | `This field is required.` | |
| 2.9 | Blank customer name | press Enter at Customer name | `This field is required.` | |

**Errors / fixes**
- *(write any error you hit, or "none observed")*

---

## Milestone 3 – View, update, delete records
**Date:** 2026-11-15

**Done**
- Added `find_sale` (returns the record or `None`) and `print_records` (table).
- Added `view_records` (date range + total), `update_record` (release bottles or change reference number), `delete_record` (asks "y" first).
- Menu options 2, 3, and 4 now call these.

**Setup before testing** *(records live in memory, so encode these 3 sales first in the same run)*

| Sale | Inputs at option 1 | Slip you should get |
|---|---|---|
| A | `2026-11-14`, `Liza Ramos`, `1`, `2` (PLUS), `2`, `0`, `4`, `1` (CASH), Enter, `y` | `111426-01` (2 to follow) |
| B | `2026-11-15`, `Mark Dela Pena`, `2`, `3` (PREMIUM), `1`, `0`, `5`, `2` (BANK), `BNK-1`, Enter, `y` | `111526-01` |
| C | `2026-11-15`, `Joy Santos`, `4`, `4` (RETAIL), `1`, `0`, `1`, `1` (CASH), Enter, `y` | `111526-02` |

**Test runs** *(run in this order, paste what the terminal shows)*

| # | Scenario | Inputs | Expected | Actual (paste) |
|---|---|---|---|---|
| 3.1 | View two days | `2`, `2026-11-14`, `2026-11-15` | 3 records, total amount 41,300.00 | |
| 3.2 | View a day with no sales | `2`, `2026-11-16`, `2026-11-16` | `No sales in that date range.` | |
| 3.3 | From date after To date | `2`, `2026-11-15`, `2026-11-14` | `The 'From' date is after the 'To' date.` | |
| 3.4 | Release more than owed, then all | `3`, `111426-01`, `1`, `3`, `2` | `Please type a number from 1 to 2.` then `Bottles still to follow: 0` | |
| 3.5 | Release when none left (boundary) | `3`, `111426-01`, `1` | `All bottles on this slip are already released.` | |
| 3.6 | Slip that does not exist | `3`, `999` | `No record with that slip number.` | |
| 3.7 | Change reference number | `3`, `111526-01`, `2`, `BNK-2` | `Reference number is now BNK-2.` | |
| 3.8 | Delete, confirmed | `4`, `111526-01`, `y` | `Record 111526-01 deleted.` | |
| 3.9 | Delete, cancelled | `4`, `111526-02`, `n` | `Record kept.` | |
| 3.10 | New slip after a delete | encode any sale on `2026-11-15` | Slip `111526-03` (02 is still the highest, so not 02 again) | |

**Errors / fixes**
- Found during an AI-assisted test run: after "Change reference number", the program printed "Reference number updated." but showed no value. The records table has no reference column, so the user could not confirm the change. Fix: the message now prints the new value (`Reference number is now BNK-2.`). Checked by rerunning test 3.7.
- *(add any error you hit yourself, or "none observed")*

---

## Milestone 4 – Daily sales report and cash count
**Date:** 2026-11-15

**Done**
- Added `daily_summary` (totals by package and payment mode), `cash_on_hand` (denomination × pieces), `cash_status` (BALANCED / OVER / SHORT).
- Added `daily_report`: prints the report, then offers the cash count. Menu option 5 now calls it.
- `cash_status` rounds the difference to 2 decimals before comparing, to avoid float errors like `0.30000000000000004`.

**Setup before testing** *(encode these 4 sales first in the same run)*

| Sale | Inputs at option 1 | Amount |
|---|---|---|
| A | `2026-11-15`, `Nina Uy`, `1`, `1` (STARTER), `2`, `0`, `2`, `1` (CASH), Enter, `y` | 7,000.00 cash |
| B | `2026-11-15`, `Carlo Reyes`, `3`, `3` (PREMIUM), `1`, `2000`, `2`, `3` (E-WALLET), `EW-1`, Enter, `y` | 15,500.00 e-wallet, 3 to follow |
| C | `2026-11-15`, `Paolo Lim`, `4`, `4` (RETAIL), `1`, `300`, `1`, `1` (CASH), Enter, `y` | 2,500.00 cash |
| D | `2026-11-14`, `Liza Ramos`, `1`, `2` (PLUS), `1`, `0`, `3`, `1` (CASH), Enter, `y` | 10,500.00 cash, different day |

**Hand-computed totals for 2026-11-15:** 3 transactions; STARTER 2 / 7,000.00; PREMIUM 1 / 15,500.00; RETAIL 1 / 2,500.00; CASH 9,500.00; E-WALLET 15,500.00; TOTAL 25,000.00; 3 bottles to follow. Sale D must not appear.

**Test runs** *(paste what the terminal shows)*

| # | Scenario | Inputs | Expected | Actual (paste) |
|---|---|---|---|---|
| 4.1 | Report for one day | `5`, `2026-11-15`, `n` | Totals match the hand-computed list above | |
| 4.2 | Cash matches | `5`, `2026-11-15`, `y`, then pieces `9`, `1`, `0` × 8 | Cash counted 9,500.00, `Result: BALANCED` | |
| 4.3 | Cash short | same, but pieces `9`, `0`, `0` × 8 | `Result: SHORT by 500.00` | |
| 4.4 | Over by one coin (boundary) | pieces `9`, `1`, `0` × 7, then `1` for 0.25 | `Result: OVER by 0.25` | |
| 4.5 | Invalid piece count | at Pieces of 1,000.00 type `-1`, then `abc` | `Please type a number from 0 to 10000.` then `Please type a whole number.` | |
| 4.6 | Day with no sales | `5`, `2026-11-16` | `No sales on that date.` | |

**Errors / fixes**
- *(write any error you hit, or "none observed")*

---

## Milestone 5 – Split into modules
**Date:** 2026-11-15

**Done**
- Created `ledger.py`: tuples, `PACKAGES`, and the calculation functions (`compute_sale`, `next_slip_no`, `find_sale`, `daily_summary`, `cash_on_hand`, `cash_status`).
- Moved the date filter out of `view_records` into a new `ledger.records_between`.
- `main.py` now starts with `import ledger` and calls `ledger.compute_sale(...)`, `ledger.PACKAGES`, and so on. It keeps input, output, the menu, and the `sales` list.

**Decisions**
- Named the module `ledger.py`, not `sales.py`. `main.py` already has a list called `sales`; `import sales` would clash with it.
- `ledger.py` has no `input()` or `print()`, so I can call its functions straight from Python to check the math.

**Regression check (AI-assisted run)**
- Before the split, ran one long script of inputs through `main.py` (menu, encode, view, update, delete, report, cash count) and saved the output: 380 lines.
- After the split, ran the same inputs again. Compared the two outputs: identical.

**Test runs** *(paste what the terminal shows)*

| # | Scenario | Inputs | Expected | Actual (paste) |
|---|---|---|---|---|
| 5.1 | Program still starts | `python main.py`, then `6` | Menu, then `Goodbye.` | |
| 5.2 | Encode still works | rerun test 2.1 | Slip `111526-01`, amount 20,000.00 | |
| 5.3 | Report still works | rerun setup + test 4.2 | `Result: BALANCED` | |
| 5.4 | Call `ledger` without the menu | `python -c "import ledger; print(ledger.compute_sale('PLUS', 2, 500, 4))"` | `{'price': 10000.0, 'amount': 20000.0, 'bottles': 6, 'to_follow': 2}` | |
| 5.5 | Missing module (failure) | rename `ledger.py` to `ledger_old.py`, run `python main.py`, then rename it back | `ModuleNotFoundError: No module named 'ledger'` | |

**Errors / fixes**
- *(write any error you hit, or "none observed")*

---

## Milestone 6 – Save and load with a file
**Date:** 2026-11-15

**Done**
- Created `storage.py`: `load_sales()` reads `sales.json` with `"r"`, `save_sales()` writes it with `"w"`, both inside `with open(...)`.
- Missing file → `load_sales()` returns `[]`. Damaged file (bad JSON, not a list, or a record missing a field from the `REQUIRED_FIELDS` tuple) → returns `None`.
- `main()` now loads the records at start and stops with a message on `None`, so it never overwrites a damaged file.
- Added `save(sales)` in `main.py`: runs after each new sale, release, reference change, and delete. Catches `OSError` (for example, a read-only file) and prints a message instead of crashing.
- Created `sample_sales.json` by running the program with 6 sales (2026-11-14: 3 sales, 2026-11-15: 3 sales; total 75,900.00).

**Errors / fixes**
- AI-assisted run: while scripting the 6 sample sales, the first attempt saved only 5. Cause: an input mistake, not a program bug. For Paolo Lim's CASH sale, the script had an extra blank line for a reference number, but CASH skips that question. The blank went to Remarks, "promo price" went to "Save this sale? (y/n)", and the program cancelled the sale (anything other than "y" cancels). Fixed the script; second run saved 6.
- *(add any error you hit yourself, or "none observed")*

**Test runs** *(paste what the terminal shows)*

| # | Scenario | Steps | Expected | Actual (paste) |
|---|---|---|---|---|
| 6.1 | First run, no file | delete `sales.json` if present, run `python main.py`, choose `6` | `Loaded 0 sale record(s) from sales.json.` | |
| 6.2 | Record survives restart | encode test 2.1's sale, choose `6`, run again, view `2026-11-15` to `2026-11-15` | `Saved to sales.json.`, then after restart `Loaded 1 ...` and slip `111526-01` | |
| 6.3 | Update survives restart | `3`, `111526-01`, `1`, `2`, exit, run again, view the day | Follow column shows `0` | |
| 6.4 | Delete survives restart | `4`, `111526-01`, `y`, exit, run again | `Loaded 0 ...`; `sales.json` contains `[]` | |
| 6.5 | Damaged file | open `sales.json` in Notepad, replace everything with `[{"slip_no": "111526-01",`, save, run | `Cannot open sales.json: the file is damaged ...`; file text unchanged | |
| 6.6 | Wrong shape | replace contents with `{}`, run | same message as 6.5 | |
| 6.7 | Missing field | replace contents with `[{"slip_no": "111526-01"}]`, run | same message as 6.5 | |
| 6.8 | Read-only file | replace contents with `[]`, right-click `sales.json` → Properties → tick Read-only, encode a sale, then untick Read-only | `Could not save to sales.json. Check that the file is not read-only.` (no crash) | |
| 6.9 | Sample data | copy `sample_sales.json` to `sales.json`, run, view `2026-11-14` to `2026-11-15` | `Loaded 6 ...`, 6 records, total 75,900.00 | |

**Tip for later tests:** step 6.9 loads 6 sales in one go, so you no longer need to encode setup sales by hand.

---

## Milestone 7 – Error handling review
**Date:** 2026-11-15

**Done**
- Listed every `try`/`except` in the code: `ValueError` in `ask_whole_number`, `ask_amount`, `ask_date`; `FileNotFoundError` and `json.JSONDecodeError` in `load_sales`; `OSError` in `save`.
- Probed inputs no earlier test covered: `nan` and `inf` as amounts, end of input mid-question, and hand-edited `sales.json` records.

**Errors / fixes** *(found in an AI-assisted review run)*

1. **`nan` accepted as a discount.**
   - Symptom: typing `nan` at "Discount per package" gave `Price after discount: nan` and `Amount due: nan`.
   - Cause: `float("nan")` succeeds, and every comparison with `nan` is False. The old check `if amount < 0 or amount > highest:` was False for both parts, so it let `nan` through.
   - Fix: check the good case instead, `if 0 <= amount <= highest: return amount`. `nan` fails this check, so it reaches the error message.
   - Verified: `nan` now prints `Please type an amount from 0 to 10,500.00.`; `inf` and normal amounts behave as before.
2. **Ctrl+Z / end of input crashed with `EOFError`.**
   - Fix: wrapped `main()` in `try` / `except (KeyboardInterrupt, EOFError)`.
   - Verified: ending input mid-question prints `Program stopped. All saved records are in sales.json.`
3. **Record without `"released"` crashed `update_record` with `KeyError: 'released'`.**
   - Fix: added `"released"` to `REQUIRED_FIELDS`.
   - Verified: such a file now gives `Cannot open sales.json ...` at start.
4. **Package `"GOLD"` in `sales.json` crashed the report with `KeyError: 'GOLD'`.**
   - Fix: `load_sales` rejects unknown packages and payment modes, using `ledger.PACKAGES` and `ledger.PAYMENT_MODES`.
   - Verified: such a file gives `Cannot open sales.json ...` at start.
- After the fixes, I loaded `sample_sales.json` and ran view, report and cash count, a bottle release, an encode, and a delete. All still worked.
- *(add any error you hit yourself, or "none observed")*

**Test runs** *(paste what the terminal shows)*

| # | Scenario | Steps | Expected | Actual (paste) |
|---|---|---|---|---|
| 7.1 | `nan` as discount | encode, PLUS, at Discount type `nan` | `Please type an amount from 0 to 10,500.00.` | |
| 7.2 | `inf` as discount | at Discount type `inf` | same message | |
| 7.3 | Ctrl+C mid-question | encode, at Customer name press Ctrl+C | `Program stopped. All saved records are in sales.json.` (no traceback) | |
| 7.4 | Missing field | put this in `sales.json`: `[{"slip_no":"111526-01","date":"2026-11-15","customer":"A","package":"PLUS","quantity":1,"amount":10500.0,"to_follow":3,"payment_mode":"CASH"}]`, run | `Cannot open sales.json ...` | |
| 7.5 | Unknown package | same as 7.4 but `"package":"GOLD"` and add `"released":3` | `Cannot open sales.json ...` | |
| 7.6 | Normal use still works | copy `sample_sales.json` to `sales.json`, run, view `2026-11-14` to `2026-11-15` | `Loaded 6 ...`, total 75,900.00 | |

---

## Milestone 8 – Final test pass and wrap-up
**Date:** 2026-11-15

**Done**
- Ran the 12 Section J tests on the finished code (AI-assisted run). Each expected result matched.
- Wrote Sections J (test table, debugging), K (conclusion), and L (references, acknowledgment).
- Removed the "not built yet" and milestone placeholders from the doc, and the milestone comment from `main.py`.

**Errors / fixes**
- None observed in the final pass.

---

## Before you submit

- [ ] Run every test in milestones 1–7 yourself and paste the output into the "Actual" columns above.
- [ ] Copy your results for T01–T12 into Section J's "Actual result" and "Status" columns. Mark a test Fail if it does not match, and say why.
- [ ] Add any error you hit yourself to Section J's Debugging, or keep the `nan` example marked as AI-assisted.
- [ ] Rewrite the drafted text in your own words where it does not sound like you.
- [ ] Edit the acknowledgment in Section L so it states what happened.
- [ ] Put your name in the doc header and rename the file `CS26_Exam2_Surname_Firstname.md`.
- [ ] Delete the two "*(Student: ...)*" notes in Sections J and L.
- [ ] Open the doc in VS Code, press Ctrl+Shift+V, and check that the tables, flowchart, and code blocks display correctly.
- [ ] Ask your instructor whether to submit the `.py` files too.
