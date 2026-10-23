import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from datetime import date, timedelta
    import requests

    return date, mo, requests, timedelta


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
    3. Function to calculate how much orders were worth: input to function will be total number of pages, items per page, and total number of items that were output from the first function. A variable will be created within the function that uses a for loop to subtract the "freight_dollars" from the "order_total_dollars" from each entry and keep a running total.
    4. Function to determine revenue by country: a similar input will be used as the previous function with total number of pages, items per page, and total number of items. For loops will again iterate through the pages and items on each page to collect the "ship_country" from each order and add the "order_total_dollars" minus "freight_dollars" to whichever country the order was shipped to. The output of the function will be a sorted list of country locations with the total revenue from each of those locations.
    5. Function to determine what was ordered most: the same inputs of total pages, items per page, and total items will be used. The function will again use for loops to iterate through the order information. A list will be created within the function of each type of product, and the total count of a product will be increased by each order that includes an order for that product. The list will be sorted to have the most popular product at the beginning of the list and then returned from the function
    6. Function to determine orders that have not shipped yet: similar inputs of total pages, items per page, and total items used. The function will also use for loops to go through all items and will create a list of the orders with "null" for "shipped_date". The function would return a tuple with the order numbers that have not yet been shipped. A further enhancement could keep a list of how long each succesful order took to ship so that information could also be analyzed.

    I will check the different functions as follows:

    1. I will enter information for same time span directly into API and will confirm the total number of results matches the number of results pulled via my code.
    2. I will confirm that the total number on the API website matches the total number of orders returned by the functiom.
    3. I will use the "sum" command within a line of code in order to add together the "order_total_dollars" and subtract the"freight_total_dollars" for all of the records and will confirm that matches the output from my function.
    4. I will add up the revenues from the individual countries and confirm that number matches the total revenue calculated within the previous function.
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
def _(date, timedelta):
    days = 50
    to_date = date.today()
    from_date = to_date - timedelta(days=days)

    return days, from_date, to_date


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Your functions, and the code that uses them.
    """)
    return


@app.cell
def _(from_date, requests, to_date):
    def pull_pagination(from_date,to_date):
        pagination_info = requests.get(
            "https://oim.zhili.dev/shop/orders?",
            params={"from_date": from_date, "to_date":to_date},
            timeout=10,
        )
        pagination_info_json = pagination_info.json()
        total_pages = pagination_info_json["pagination"]["pages"]
        total_items = pagination_info_json["pagination"]["total"]
        items_per_page = pagination_info_json["pagination"]["per_page"]
        return total_pages, total_items, items_per_page

    total_pages, total_items, items_per_page = pull_pagination(from_date,to_date)

    return total_items, total_pages


@app.function
#function created by AI since dollar fields from API sometimes came back as plain numbers and others as text. 
#The outputs from the API are converted to numbers once they are stored, so future functions can treat them as numbers
# "text/plain+float:457.5", so we only split on ":" if it is text
def to_float(value):
    return float(value.split(":")[-1]) if isinstance(value, str) else float(value)


@app.cell
def _(from_date, pull_order_lines, requests, to_date, total_pages):
    def find_order_info_(total_pages, to_date, from_date):
        orders = []
        for page in range(1, total_pages + 1):
            response = requests.get(
                "https://oim.zhili.dev/shop/orders?",
                params={"from_date": from_date, "to_date": to_date, "page": page},
                timeout=10,
            )
            page_json = response.json()
            for item in page_json["items"]:
                # the list endpoint does not include "lines", so we call
                # pull_order_lines to get each order's line items
                lines = pull_order_lines(item["order_id"])
                order = {
                    "order_id": item["order_id"],
                    "customer_id": item["customer_id"],
                    "customer_name": item["customer_name"],
                    "order_date": item["order_date"],
                    "required_date": item["required_date"],
                    "shipped_date": item["shipped_date"],
                    "shipper": item["shipper"],
                    "ship_city": item["ship_city"],
                    "ship_country": item["ship_country"],
                    "freight_dollars": to_float(item["freight_dollars"]),
                    "line_count": item["line_count"],
                    "order_total_dollars": to_float(item["order_total_dollars"]),
                    "lines": lines,
                }
                orders.append(order)
        return orders

    orders = find_order_info_(total_pages, to_date, from_date)
    len(orders)

    all_lines = []
    for order in orders: 
        all_lines.append(order["lines"])

    orders
    return (orders,)


@app.cell
def _(requests):
    def pull_order_lines(order_id):
        # calls the per-order detail endpoint to get one order's line items
        detail_response = requests.get(
            f"https://oim.zhili.dev/shop/orders/{order_id}",
            timeout=10,
        )
        detail = detail_response.json()
        lines = []
        for line in detail.get("lines", []):
            lines.append({
                "product_id": line["product_id"],
                "product_name": line["product_name"],
                "unit_price_dollars": to_float(line["unit_price_dollars"]),
                "quantity": line["quantity"],
                "discount_fraction": to_float(line["discount_fraction"]),
                "line_total_dollars": to_float(line["line_total_dollars"]),
            })
        return lines

    return (pull_order_lines,)


@app.cell
def _(orders):
    def revenue_calc(orders): 
        total_revenue = 0
        for order in orders:
            total_revenue += order["order_total_dollars"]-order["freight_dollars"]
        return round(total_revenue, 2)

    total_revenue = revenue_calc(orders)
    return (total_revenue,)


@app.cell
def _(orders):
    def revenue_calc_by_country(orders):
        revenue_by_country = {}
        for order in orders:
            country = order["ship_country"]
            amount = order["order_total_dollars"]-order["freight_dollars"]
            if country in revenue_by_country:
                revenue_by_country[country] += amount
            else:
                revenue_by_country[country] = amount

        # sort revenue_by_country from highest to lowest: repeatedly find the
        # largest remaining value and move it into sorted_countries
        remaining_countries = dict(revenue_by_country)
        sorted_countries = []
        while remaining_countries:
            best_country = None
            best_value = None
            for country in remaining_countries:
                if best_value is None or remaining_countries[country] > best_value:
                    best_country = country
                    best_value = remaining_countries[country]
            sorted_countries.append((best_country, best_value))
            del remaining_countries[best_country]
        return sorted_countries

    sorted_countries = revenue_calc_by_country(orders)
    return (sorted_countries,)


@app.cell
def _(orders):
    def top_5_products(orders):
        total_per_product = {}
        for order in orders:
            for line in order["lines"]:
                product = line["product_name"]
                quantity = line["quantity"]
                if product in total_per_product:
                    total_per_product[product] += quantity
                else:
                    total_per_product[product] = quantity

        # keep only the top 5 highest values: repeatedly find the
        # largest remaining value and move it into top_5
        top_5 = {}
        remaining = dict(total_per_product)
        for i in range(5):
            best_key = None
            best_value = None
            for key in remaining:
                if best_value is None or remaining[key] > best_value:
                    best_key = key
                    best_value = remaining[key]
            if best_key is not None:
                top_5[best_key] = best_value
                del remaining[best_key]
        return top_5

    top_5_products_result = top_5_products(orders)
    top_5_products_result
    return (top_5_products_result,)


@app.cell
def _(orders):
    def not_shipped(orders):
        not_shipped_ids = []
        for order in orders:
            if order["shipped_date"] == None:
                not_shipped_ids.append(order['order_id'])
        return not_shipped_ids

    orders_not_shipped = not_shipped(orders)
    orders_not_shipped
    return (orders_not_shipped,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    Your result table, printed with print and f-strings with the columns lined up, and one sentence that answers the question in section 1 with the numbers in it. Print the sentence from code with an f-string, so that it changes when the data does.
    """)
    return


@app.cell
def _(
    days,
    from_date,
    orders_not_shipped,
    sorted_countries,
    to_date,
    top_5_products_result,
    total_items,
    total_revenue,
):
    print(f"ORDER REPORT: {from_date} to {to_date}")
    print(f"Total orders: {total_items}")
    print(f"Total revenue (excluding freight): ${total_revenue:,.2f}")
    print()

    print("Revenue by country:")
    for country, revenue in sorted_countries:
        print(f"  {country:<20} ${revenue:,.2f}")
    print()

    print("Top 5 products by units sold:")
    for product, quantity in top_5_products_result.items():
        print(f"  {product:<30} {quantity:>6} units")
    print()

    print(f"Orders not shipped yet ({len(orders_not_shipped)}):")
    for order_id in orders_not_shipped:
        print(f"  {order_id}")
    print()

    print(f"In the past {days} days, we received {total_items} orders worth ${total_revenue:,.2f} in revenue, and {len(orders_not_shipped)} of those orders have not shipped yet.")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Reach at least one result a second way, in this notebook, and show that the two agree. Write a cell that gets the same number from other fields, or open the raw reply in your browser and find each number of one row of your table there. For instance: an average bill is close to the average value times the tax rate divided by 1,000; an order's total equals the sum of its lines; the number of records you collected equals the total the API reports.
    """)
    return


@app.cell
def _(from_date, to_date, total_items, total_pages):
    #Check for pull_pagination function: 
    print(total_items)
    print(total_pages)
    print(to_date)
    print(from_date)

    #I manually input date range from 2026-10-16 to 2026-10-23 on API website and confirmed the pagination tab matches the total_items and total_pages numbers in the response body- which was 24 and 1, respectively. 

    return


@app.cell
def _(orders):
    #Check for find_order_info, pull_order_lines, and to_float functions. I randomly chose an index from the list of orders, 9, and had the data for that displayed. I confirmed that the data displayed, including the order_info and all of the line items, matched what was in the API. I also confirmed that numbers were matching between this and API to confirm to_float function was converting them correctly. 
    orders[9]
    return


@app.cell
def _(orders, total_revenue):
    #Check for revenue_calc function by using sum functions. The numbers match, but I realized that function was not rounding output. I updated the functions to have the output rounded to two decimal points. 
    sum_order_totals = sum(order["order_total_dollars"] for order in orders)
    sum_freight_totals = sum(order["freight_dollars"] for order in orders)
    check_total_revenue = sum_order_totals - sum_freight_totals

    check_total_revenue, total_revenue
    return


@app.cell
def _(sorted_countries):
    #check for revenue_calc_by_country function- confirm that sum of revenues for all of the countries adds up to values above. The function sums just the revenue half of each (country, revenue) tuple. The total revenue matches the revenues calculated above. 
    sum_country_orders = sum(revenue for country, revenue in sorted_countries)
    sum_country_orders

    return


@app.cell
def _(orders, top_5_products_result):
    #check for top_5_products function
    #I picked two products that showed up in the top 5 and recount their units a different way
    products_to_check = list(top_5_products_result.keys())[:2]

    for product_name in products_to_check:
        manual_count = 0
        for _order in orders:
            for line in _order["lines"]:
                if line["product_name"] == product_name:
                    manual_count += line["quantity"]
        print(f"{product_name}: function says {top_5_products_result[product_name]}, manual count says {manual_count}")
    return


@app.cell
def _(orders, orders_not_shipped):
    #Check for not_shipped function:
    #count shipped and not-shipped orders a different way, with a plain loop
    shipped_count = 0
    not_shipped_count = 0
    for _order in orders:
        if _order["shipped_date"] is None:
            not_shipped_count += 1
        else:
            shipped_count += 1

    print(f"shipped: {shipped_count}, not shipped: {not_shipped_count}, total orders: {len(orders)}")
    print(f"shipped + not shipped == total orders: {shipped_count + not_shipped_count == len(orders)}")
    print(f"manual not-shipped count matches function output: {not_shipped_count == len(orders_not_shipped)}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell. If the agent got it right the first time: What did you do to verify that? Pointing to your check in section 6 is enough.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When I worked with the agent on the "not_shipped" function, it originally suggested the code "if order["shipped"] == False" for evaluating whether the orders had shipped. I saved this original output as commit 7954688. I knew that the key in the dictionary for shipping status was not "shipped", so I looked into the dictionary of orders and confirmed that the shipped status was indicated by "shipped_date" and that my function had saved the ship_date as "None" if it was listed as null on the API. I updated the code accordigly to correct the line of code to "if order["shipped_date"] == None:".

    After I corrected that logic I looked at the output of the not_shipped orders. I saw that the entirety of the information on the orders was included in a dictionary instead of having the specific order IDs listed. I asked the AI how to correct the logic within the function and it pointed out I should use the "append" functionality instead of the "not_shipped[order['id']] = order" line that it had originally suggested in the code. I confirmed that the not_shipped orders only listed the order ids.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    Pick two functions in your notebook that your agent wrote or helped write. For each, write in your own words what goes in, what comes out, and one line you had to ask about. Then choose one change to what the tool does, such as another county, another week or another rule. Changing one value in your Inputs cell is enough. Write what you expect to change in the answer. Commit with the message `mp2: prediction`, make the change, run it, and write what happened and whether it matched.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I had my agent help write the functions for finding the order and line info. Originally the agent had pulled the order info and line info within the same function, which was difficult for me to decipher. I had the agent update the code to separate the functions.
    - what goes in: The total number of pages of results from the API, which was returned from the pagination function, and the to_date and from_date that are evaluated automatically at the beginning of the code. Note: I originally thought I also had to add items per page and total items, but that is not required since items_per_page is a default and the code will automatically end the list once it get to the final "item" on the page.
    - what comes out: A list of dictionaries, with one dictionary per order. The "line" key of the dictionary for each order also contains a list of dictionaries- with one dictionary per product that was included in the order.
    - Line I had to ask about: I had to ask about to_float function that was incorporated into this function. Since data from APIs like this might have different sources, there's potential for them to have different data types. This to_float function ensures all numbers that are pulled are converted to a float type, which allows them to be used in subsequent calculations.
    - Change to what the tool does: I am going to increase time period to 50 days in order to get the tool to return multiple pages of results. I expect the total number of orders/lines to increase since there will be a longer time period for data to pull from.
    - Results: As I expected, total number of orders increased to 170 with the larger timeframe of 50 days.

    I also had my agent help me write the top_5_products function.
    - What goes in: The data set of "orders" that was created from the find_order_info function.
    - What comes out: The 5 products that had the highest quantity sold within the specified number of days.
    - Line I had to ask about: I had to ask about why best_value and best_key were set to "None" within the code that was identifying the top five products. Setting these to "None" ensures that the first item that is read from the list is what all of the subsequent items will be compared to.
    - Change to what the tool does: create a similar function but rank by total revenue instead of total quantity sold to see if most popular products are similar to products creating the most revenue. I predict that there will be a big difference in the "top 5 products" since higher priced items are often sold in lower quantities, but it doesn't take much quantity to drive a higher revenue.
    """)
    return


@app.cell
def _(orders):
    def top_5_products_by_revenue(orders):
        revenue_per_product = {}
        for order in orders:
            for line in order["lines"]:
                product = line["product_name"]
                revenue = line["line_total_dollars"]
                if product in revenue_per_product:
                    revenue_per_product[product] += revenue
                else:
                    revenue_per_product[product] = revenue

        # keep only the top 5 highest values: repeatedly find the
        # largest remaining value and move it into top_5
        top_5 = {}
        remaining = dict(revenue_per_product)
        for i in range(5):
            best_key = None
            best_value = None
            for key in remaining:
                if best_value is None or remaining[key] > best_value:
                    best_key = key
                    best_value = remaining[key]
            if best_key is not None:
                top_5[best_key] = round(best_value, 2)
                del remaining[best_key]
        return top_5

    top_5_products_by_revenue_result = top_5_products_by_revenue(orders)
    top_5_products_by_revenue_result
    return


@app.cell
def _(orders, top_5_products_result):
    #revenue for the top 5 products by quantity (from top_5_products_result)
    revenue_for_top_5_by_quantity = {}
    for _product_name in top_5_products_result:
        _product_revenue = 0
        for _order in orders:
            for _line in _order["lines"]:
                if _line["product_name"] == _product_name:
                    _product_revenue += _line["line_total_dollars"]
        revenue_for_top_5_by_quantity[_product_name] = round(_product_revenue, 2)

    revenue_for_top_5_by_quantity
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
    90 minutes on 18Oct
    60 minutes
    60 min so far on 23Oct
    """)
    return


if __name__ == "__main__":
    app.run()
