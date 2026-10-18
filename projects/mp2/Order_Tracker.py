import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. The Question

    Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool is to track orders from the past 7 days and report some key statistics from those orders including how many orders came in, how much they were worth, where they went, what sold most, and which orders have not shipped yet. A tool that generates and summarizes this information can be used by companies to understand and improve their business performance. For example, they can use this tool to track their performance over time by comparing their weekly total number of orders/revenue, can use insights from what products sold best/worst to modify their strategy, and keep an eye on which orders have not yet shipped.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    Before you ask your agent anything, open the API's address in your browser and read what comes back. Then write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these:

    - Which functions will your tool need? For each, what goes in and what comes out?
    - Which addresses will they request?
    - How will you know you have every record?
    - Which check will you use in section 6, and which two numbers should agree?

    Commit with the message `mp2: plan before AI`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My tool will need the following functions:
    1. Determine pagination: Function to determine the total number of results/pages from the API for orders in the past 7 days by pulling the json file and calling the "pagination" result from that json file. The inputs to that function will be the start date and end date. That function will return the number of items per page (per_page), total number of items(total), and total number of pages(pages).
    2. How many orders came in will be the same as the total number of items returned("total") from the first function. Those can be assigned to a variable for total orders outside of that function.
    3. Function to calculate how much orders were worth: input to function will be total number of pages, items per page, and total number of items that were output from the first function. A variable will be created within the function that uses a for loop to pull the "order_total_dollars" from each entry and keep a running total.
    4. Function to determine where orders went: a similar input will be used as the previous function with total number of pages, items per page, and total number of items. For loops will again iterate through the pages and items on each page to collect the "ship_city" and "ship_country" from each order and keep a tally of the number of total orders going to each city. The tricky part for this one will be to ensure that if cities are in different countries they will be added to separate tallies. I will attempt to account for this my combining the city and country so they can be counted together as a ship location. The output of the function will be a sorted list of appended city/country locations with the total number of orders from those locations.
    5. Function to determine what was ordered most: the same inputs of total pages, items per page, and total items will be used. The function will again use for loops to iterate through the order information. A list will be created within the function of each type of product, and the total count of a product will be increased by each order that includes an order for that product. The list will be sorted to have the most popular product at the beginning of the list and then returned from the function
    6. Function to determine orders that have not shipped yet: similar inputs of total pages, items per page, and total items used. The function will also use for loops to go through all items and will create a list of the orders with "null" for "shipped_date". The function would return a tuple with the order numbers that have not yet been shipped. A further enhancement could keep a list of how long each succesful order took to ship so that information could also be analyzed.

    I will check the different functions as follows:

    1. I will enter information for same time span directly into API and will confirm the total number of results matches the number of results pulled via my code.
    2. I will confirm that the total number on the API website matches the total number of orders returned by the functiom.
    3. I will use the "sum" command within a line of code in order to add together the order_total_dollars for all of the records and wil confirm that matches the output from my function.
    4. I will look through the list of ship locations to make sure they make sense (i.e. include city and country information, don't have duplicates where the same city/country are listed with different punctuation, etc.). I will also add up the number of orders from all of the locations and will confirm that number matches the total number of orders.
    5. I will create a separate piece of code that looks for a few specific products to ensure the numbers for those match the output from the function.
    6. I will add a counter within the function to confirm that the total number of orders evaluated matches the total number of items shipped in the past 7 days
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every input in one cell.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Your functions, and the code that uses them.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    Your result table, printed with print and f-strings with the columns lined up, and one sentence that answers the question in section 1 with the numbers in it. Print the sentence from code with an f-string, so that it changes when the data does.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Reach at least one result a second way, in this notebook, and show that the two agree. Write a cell that gets the same number from other fields, or open the raw reply in your browser and find each number of one row of your table there. For instance: an average bill is close to the average value times the tax rate divided by 1,000; an order's total equals the sum of its lines; the number of records you collected equals the total the API reports.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell. If the agent got it right the first time: What did you do to verify that? Pointing to your check in section 6 is enough.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    Pick two functions in your notebook that your agent wrote or helped write. For each, write in your own words what goes in, what comes out, and one line you had to ask about. Then choose one change to what the tool does, such as another county, another week or another rule. Changing one value in your Inputs cell is enough. Write what you expect to change in the answer. Commit with the message `mp2: prediction`, make the change, run it, and write what happened and whether it matched.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    What you tried past the main task, what you found, and where it is in the notebook.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    About how many hours this project took you outside class, as one number. It is not graded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    30 minutes total on 17Oct
    """)
    return


if __name__ == "__main__":
    app.run()
