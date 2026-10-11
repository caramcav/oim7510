# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Someone who was planning on buying a house would use this tool to quickly calculate their estimated monthly mortgage payment with varied factors such as interest rates, loan terms, and starting loan amounts in order to guide their decision on which mortgage to choose. Additionally, it helps estimate total time/payments required for loan if additional monthly payments were made to the loan.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. I would first define the main input variables for the loan by creating a variable, loan_amount, and a dictionary that hold the two main pieces of information for each loan: interest rate and loan term.
    2. I would define a function that calculates the monthly payment and total payment for those give loan inputs (loan_amount,interest_rate, and loan_term).
    3. At the beginning of the function I'd print the headings for the table that I'll create the lines for using the for loop. I'd also initialize total_payments, total_principal_payments, and total_interest_payments variables with a value of "0" so each calculated monthly/principal/interest payments can be added to that.
    4. After printing the table headers I would use the range function to step through each monthly payment using the calculation [loan_amount * r / (1 - (1 + r) ** -n)].
    5. After the monthly payments are calculated I'd print the month, monthly payments, and the running totals in table format.
    6. I'd call this function for both the 15 year and 30 year loan, then add a print statement that compares the outputted results of each.

    What does your loop carry from one step to the next, the way a running total carries its sum?
    - My loop carries three values from one step to the next: how much has been paid towards the loan in total (principal + interest) and how much has been paid towards principal specifically and interest specifically.

    Which check will you use in section 6, and which two numbers should agree?
    - I will check that the variable that keeps track of principal paid in the two loans matches the loan amount.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    # Your inputs.
    return annual_rates, loan_amount


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.function
def loan_calculator(loan_amount, interest_rate, loan_term): 
    total_payments = 0
    total_interest_payments = 0
    principal_balance = loan_amount
    total_months = loan_term * 12
    r = interest_rate/12
    payment = round(loan_amount * r / (1 - (1 + r) ** -total_months), 2)
    print(f"\n{loan_term}-Year Loan at {interest_rate:.2%}")
    print(f"{'Month':>6} {'Payment':>12} {'Interest':>12} {'Total Interest':>16} {'Balance':>14}")
    print(f"{0:>6} {'--':>12} {'--':>12} {'--':>16} {principal_balance:>14,.2f}")

    for n in range(1,total_months+1):
        interest = principal_balance * r
        total_interest_payments += interest
        if n == total_months:
            payment = principal_balance + interest
        total_payments += payment
        principal_balance = principal_balance-payment+interest
        print(f"{n:>6} {payment:>12,.2f} {interest:>12,.2f} {total_interest_payments:>16,.2f} {principal_balance:>14,.2f}")
    
    return total_interest_payments


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    interest_30 = loan_calculator(loan_amount, annual_rates[30], 30)
    interest_15 = loan_calculator(loan_amount, annual_rates[15], 15)

    print(f"\nThe 30-year loan costs ${interest_30 - interest_15:,.2f} more in total interest than the 15-year loan (${interest_30:,.2f} vs ${interest_15:,.2f}).")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I confirmed that the last line for both tables output by the function has the principal balance calculated to "0." This means that the total payments aligned with the calculated repayment period.
    """)
    return


@app.cell
def _(annual_rates):
    #verifying with the calculation that the interest payment in month 100 algined with interest calculation by multiplying principal in month 99 with monthly interest rate

    interest_100_15 = 227398.63 * annual_rates[15]/12

    interest_100_30 = 356438.13 *annual_rates[30]/12

    interest_100_15, interest_100_30
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I used AI to help me write the print function that displayed the monthly payments in table format. These included the print statements in rows 8 and 9 and later row 10 of the loan_calculator function. I verified that the numbers were correct by going through each column that was outputted to confirm they made sense. For the months row, I confirmed they went from 1 to 12 times total number of years(360 for 30 year and 180 for 15 year). I then confirmed the payment was the same for each month for both of the functions, except for the last month which should have the remaining principal balance plus the interest payment. I confirmed the interest payments were going down over time, and the total interest paid was going up over time. Finally, I confirmed that the balance started at $400,000, went down over time and eventually ended up at $0. After confirming those values, I decided I also wanted a row that printed balance at month "0"- so I had AI create the code for printing a row at month "0" that showed the starting balance. After it created the code I confirmed the table output that information correctly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
