# Loan Amortization Calculator

**INSY 8212: Programming with C**. **Due Wednesday 07 October 2026, 23:59 (Africa/Kigali time).**

## Overview

In this assignment you will create e C-program that calculates and displays a month-by-month payment schedule (an amortization table) for a loan.

When you borrow money, each monthly payment  is split into two portion; 1. interest  -> The fee paid to the lender for borrowing the remaining balance. 2. principal -> The amount that goes directly towards reducing the balance you owe.

Your program will accept user input for the principal amount, annual interest rate and monthly payment, validate that the monthly payment is sufficient to reduce the loan, and output a breakdown of monthly payments until the balance reaches $0.0

## Background: what is amortization?

The word **amortize** comes from the Old French *amortir*, "to deaden or kill," built from the Latin *ad* ("to") + *mors, mortis* ("death"). To amortize a loan is, quite literally, to *kill it off* gradually, one payment at a time, until nothing is left. (Its cousin **mortgage** comes from the Old French for a "dead pledge": a pledge that dies once the debt is paid.)

An **amortization schedule** is the month-by-month story of that loan dying: for each payment, how much went to the bank as interest, how much actually reduced the debt (a.k.a the principal), and what is still owed (a.k.a the balance).

## How each monthly payment is split

Every month, the payment does two jobs:

1. **Pay the interest** that built up on what you still owe that month.
2. **Everything left over repays the principal** (the borrowed amount).

With a monthly interest rate of *r* = annual rate ÷ 12 ÷ 100:

| Step | Formula |
|---|---|
| Interest this month | `interest = balance × r` |
| Principal repaid | `principal = payment − interest` |
| New balance | `balance = balance − principal` |

Because the balance shrinks each month, the interest shrinks too, so **more and more of the same payment goes to the principal over time**. Early payments are mostly interest; late payments are mostly principal.

### A worked example

Borrow **1000.00** at **12%** per year (so *r* = 1% per month), paying **300.00** per month:

| Month | Payment | Interest | Principal | Balance |
|---:|---:|---:|---:|---:|
| 1 | 300.00 | 10.00 | 290.00 | 710.00 |
| 2 | 300.00 | 7.10 | 292.90 | 417.10 |
| 3 | 300.00 | 4.17 | 295.83 | 121.27 |
| 4 | 122.48 | 1.21 | 121.27 | 0.00 |

Notice month 4: the full 300.00 isn't needed, so the **last payment is smaller**. It is just the remaining balance plus that month's interest. In total the borrower pays 1022.48, of which 22.48 is interest.

## Constraints your program must handle

- **The payment must be larger than the first month's interest.** If
  `payment <= principal × r`, the balance never goes down and the loan is
  never paid off: your program would loop forever. Detect this *before*
  printing the schedule. (Use the error message in **Example 2** below.)
- **Never print a negative balance.** Handle the final, smaller payment as
  shown above.

## Input

```
Enter principal amount ($) -> 1000.00
Enter annual interest rate (%) -> 12.0
Enter monthly payment ($) -> 300.00
```

## Output

```
Month -> 1; Payment -> $300.00; Interest -> $10.00; Principal -> $290.00; Balance -> $710.00
Month -> 2; Payment -> $300.00; Interest -> $7.10; Principal -> $292.90; Balance -> $417.10
Month -> 3; Payment -> $300.00; Interest -> $4.17; Principal -> $295.83; Balance -> $121.27
Month -> 4; Payment -> $122.48; Interest -> $1.21; Principal -> $121.27; Balance -> $0.00
```

## Examples

**Example 1:** Short-term loan with multiple full payment and a partial final payment.

*Input:*

```
Enter principal amount ($) -> 1000.00
Enter annual interest rate (%) -> 12.0
Enter monthly payment ($) -> 300.00
```

*Expected output:*

```
Month -> 1; Payment -> $300.00; Interest -> $10.00; Principal -> $290.00; Balance -> $710.00
Month -> 2; Payment -> $300.00; Interest -> $7.10; Principal -> $292.90; Balance -> $417.10
Month -> 3; Payment -> $300.00; Interest -> $4.17; Principal -> $295.83; Balance -> $121.27
Month -> 4; Payment -> $122.48; Interest -> $1.21; Principal -> $121.27; Balance -> $0.00
```

**Example 2:** Monthly payment is equivalent to the first month's interest preventing the deduction of the principal.

*Input:*

```
Enter principal amount ($) -> 1000.00
Enter annual interest rate (%) -> 12.0
Enter monthly payment ($) -> 10.00
```

*Expected output:*

```
Error: Monthly payment of 10.00 is too low!
Minimum monthly payment must be greater than 10.00 to cover interest
```

**Example 3:** Monthly payment is less than the monthly interest.

*Input:*

```
Enter principal amount ($) -> 5000.00
Enter annual interest rate (%) -> 12.0
Enter monthly payment ($) -> 40.00
```

*Expected output:*

```
Error: Monthly payment of 40.00 is too low!
Minimum monthly payment must be greater than 50.00 to cover interest
```

## What you may and may not use

**Allowed:**

- `stdio.h`

**Not allowed:**

- `math.h`

## Getting started

1. Open the template repository (https://github.com/Kabera192/hw1-template) and click **Use this template > Create a new repository**. Make it **private** (a public repo lets anyone copy your work).
2. Clone your new repository to your computer and work there. Commit and push as often as you like; this is for your own version control and is **not** your submission.
3. Write your code in `hw1.c`.

## Compiling

Your code is graded with exactly this command (gcc on Linux):

```
gcc -std=c11 -Wall -Wextra -Werror hw1.c -o hw1
```

Or just type `make`. **Warnings count as errors:** if gcc prints any warning, your program does not compile and every test scores 0. Fix every warning before you submit.

## Testing your work

Run the visible tests with `make test` (or `python3 tests/run_tests.py`). They show exactly how your output differs from what is expected, with invisible characters marked. The visible tests are:

- `standard_short_term_loan`: Short-term loan with multiple full payment and a partial final payment.
- `long_term_loan`: Multi-year loan ~3years testing long term iteration and balance tracking.
- `large_principal`: Tests a large principal and multi-year payment schedule.
- `shorter_term_loan`: A short 2 month amortization schedule.
- `small_emergency_loan`: A small emergency loan that should pay off in 4 months.
- `monthly_payment_equals_interest`: Monthly payment is equivalent to the first month's interest preventing the deduction of the principal.
- `monthly_payment_lessthan_interest`: Monthly payment is less than the monthly interest.
- `interest_far_exceed_payment`: Interest expected on the loan is far greater than the monthly payment.
- `payment_is_zero`: Monthly payment is zero.
- `one_cent_below`: Payment is 1 cent below the monthly interest expected.
- `edge_1`: Tests for floating point precision that might cause infinite loops
- `edge_2`: Payment is exactly one cent above the monthly charge.
- `edge_4`: Fractional interest rates to test the use of doubles or floats.
- `edge_9`: Final month payment leaves a fractional principal under $1.00

Grading also uses **14 hidden tests** that check edge cases. Passing every visible test does not guarantee full marks: test unusual inputs yourself.

`tests/run_tests.py` needs Python 3. On Windows, use WSL (recommended) or MSYS2 so that `gcc` and `make` are available.

## Submitting

**Only the Google Form counts.** Pushing to GitHub is not a submission.

1. Make a zip file named `hw1_STUDENTID.zip`, replacing STUDENTID with your numeric student ID, containing `hw1.c`. The easiest way: `make zip ID=12345` or `python3 tests/make_zip.py 12345` (with your ID). This also checks that your code compiles.
2. To zip by hand instead: Windows: select the file(s), right-click > Send to > Compressed (zipped) folder. macOS: select the file(s), right-click > Compress. Linux/WSL: `zip hw1_STUDENTID.zip hw1.c`. Zip the files themselves, not a folder around them (a folder is tolerated, but not required).
3. Do not include compiled programs, and do not use .rar or .7z.
4. Open the submission form (https://docs.google.com/forms/d/e/1FAIpQLSelQUKjV2yDZ6rVfttxN1gXg9SNtE3HLpOQ0XcE2y08Dz2u1w/viewform?usp=header), sign in with your Google account, enter your full name and numeric student ID exactly, and upload the zip.
5. You may submit again as many times as you like (see the late policy below for how we choose which one to grade).

## How your grade is computed

| Category | Points | How it is graded |
|---|---|---|
| Compiles cleanly (no warnings) | 10 | Compiles with the command above with no warnings |
| Basic correctness (visible tests) | 50 | 19 10 visible + 9 hidden test(s); partial credit per test |
| Edge cases (hidden tests) | 30 | 9 4 visible + 5 hidden test(s); partial credit per test |
| Code quality (graded by hand) | 10 | Graded by hand by the instructor |
| Total | 100 |  |

If your program does not compile, all test-based categories score 0. Within a category, tests can carry different weights. The final score is rounded to the nearest 0.5. You will receive a feedback report by email listing every test, what went wrong, and your points per category.

## Deadline and late submissions

Deadline: Wednesday 07 October 2026, 23:59 Africa/Kigali time (UTC+02:00; = 2026-10-07 21:59 UTC).

Grace period: submissions up to 15 minutes after the deadline count as on time. After that, lateness is measured from the deadline itself.

Late penalty: 10% of the score you earned per day late. Any part of a day counts as a full day.

Submissions more than 3 day(s) late receive 0.

You may submit as many times as you like. We grade your latest on-time submission AND your latest submission overall (with its late penalty), and you receive whichever final score is higher.

| Submitted after the deadline by | Penalty |
|---|---|
| 10 minutes | 0 (on time) |
| 3 hours | -10% |
| 1 day 1 hour | -20% |
| 2.5 days | -30% |
| 4 days | score = 0 |

If you need an extension, ask the instructor before the deadline.

## Academic integrity

This is an individual assignment. You may discuss ideas with classmates, but the code you submit must be written by YOU. All submissions are compared with each other by software, and unusually similar pairs are reviewed by the instructor. Similar code alone is never treated as proof of copying; you will always be asked to explain your work first.
It is my sincere hope that you will take this assignment as a challenge to yourself to produce work that you can fully explain.
