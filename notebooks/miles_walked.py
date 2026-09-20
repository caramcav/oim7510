import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import matplotlib.pyplot as plt

    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question: How many miles did I walk in the last week?
    """)
    return


@app.cell
def _():
    miles_walked = [3.2, "n/a", 4.5, 5.0, 2.75, 6.1, 3.8]
    day_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return day_labels, miles_walked


@app.cell
def _(mo):
    mo.md(r"""
    The number `4.5` in `miles_walked` (paired with `"Wednesday"` in `day_labels`) means I walked 4.5 miles on Wednesday.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    The last line of the error said `TypeError: unsupported operand type(s) for +: 'float' and 'str'`.

    In my own words: The above error means that I can't do addition with the data types in the array since float and string are different types

    The rule I'm choosing: skip any value that isn't a real number (like `"n/a"`) instead of guessing a replacement value. I'll build a clean list with a `for` loop and an `if` that only keeps values which are `int` or `float`.
    """)
    return


@app.cell
def _(miles_walked):
    clean_miles = []
    for _miles in miles_walked:
        if isinstance(_miles, (int, float)):
            clean_miles.append(_miles)
    clean_miles
    return (clean_miles,)


@app.cell
def _(clean_miles):
    total_miles = sum(clean_miles)
    average_miles = total_miles/len(clean_miles)
    print(f"I walked a total of {total_miles:.2f} miles in the last week and an average of {average_miles:.2f} miles per day.")
    return


@app.cell
def _(miles_walked):
    total = miles_walked[0]+miles_walked[2]+miles_walked[3]+miles_walked[4]+miles_walked[5]+miles_walked[6]
    print(f"{total:.2f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    How I know these numbers are right: I added up each of the values that were known for miles walked per day this past week with the line of code above and got the same answer of 29.05 miles.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All of the calculated values update when I switched the miles walked on Sunday from "7.5" to "3.8." Those include values such as total_miles, clean_miles, and the check of the calculation using addition of the different indexes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The agent had created a manual calculation where it wrote down all of the miles_walked values as the numbers themselves. However, this strategy made it so that the manual check would not function after I changed one of the number values. I created a different line of code to manually check that the different values in the array had the same sum as the clean_miles function.
    """)
    return


@app.cell
def _(clean_miles, day_labels, miles_walked, plt):
    clean_labels = []
    for _miles, _day in zip(miles_walked, day_labels):
        if isinstance(_miles, (int, float)):
            clean_labels.append(_day)

    plt.figure(figsize=(8, 5))
    plt.bar(clean_labels, clean_miles, color="steelblue")
    plt.xlabel("Day")
    plt.ylabel("Miles Walked")
    plt.title("Miles Walked per Day (Last Week)")
    plt.gca()
    return


if __name__ == "__main__":
    app.run()
