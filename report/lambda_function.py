"""Script which defines a lambda function."""

import json
from os import environ
from datetime import datetime, timedelta

from dotenv import load_dotenv
import pandas as pd

from database import get_database_connection, load_transaction_data
from queries import get_trucks_by_count, get_trucks_by_value, get_total_transaction_value
from queries import get_trucks_by_avg_amount, get_best_hour_trucks


def get_total_revenue_html(data: pd.DataFrame) -> str:
    """Returns the html string for the total revenue."""

    total_revenue = str(get_total_transaction_value(data))
    
    return f"""<h2>Total Revenue</h2><ul><li><h3>£{total_revenue}</h3></li></ul>"""

def get_revenues_html(data: pd.DataFrame) -> str:
    """Returns the html string for the revenues per truck."""

    revenues_string = "<h2>Revenue per Truck</h2>"
    revenues_string += "<ul>"

    values = get_trucks_by_value(data)

    for (name, revenue) in values.items():
        revenues_string += f"""<li><b>{name}</b> - £{revenue}</li>"""
    revenues_string += "</ul>"

    return revenues_string

def get_transactions_html(data: pd.DataFrame) -> str:
    """Returns the html string for the transactions per truck."""

    transactions_string = "<h2>Transactions per Truck</h2>"
    transactions_string += "<ul>"

    counts = get_trucks_by_count(data)

    for (name, count) in counts.items():
        transactions_string += f"""<li><b>{name}</b> - {count}</li>"""
    transactions_string += "</ul>"

    return transactions_string

def get_averages_html(data: pd.DataFrame) -> str:
    """Returns the html for the average transaction per truck."""

    averages_string = "<h2>Average Transaction per Truck</h2>"
    averages_string += "<ul>"

    averages = get_trucks_by_avg_amount(data)

    for (name, avg) in averages.items():
        averages_string += f"""<li><b>{name}</b> - £{avg}</li>"""
    averages_string += "</ul>"

    return averages_string

def get_popular_times_html(data: pd.DataFrame) -> str:
    """Returns the html for the most popular times per truck."""

    popular_times_string = "<h2>Most Popular Times</h2>"
    popular_times_string += "<ul>"

    best_hours = get_best_hour_trucks(data)

    for (name, data) in best_hours.items():
        popular_times_string += f"""<li><b>{name}</b> - {data['hour']}:00 ({data['transactions']} transactions)</li>"""
    popular_times_string += "</ul>"

    return popular_times_string


def handler(event=None, context=None) -> dict:
    """Lambda function."""

    YESTERDAYS_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    load_dotenv()

    db_conn = get_database_connection(environ)

    data = load_transaction_data(db_conn)

    html_string = f"""<h1>T3 Data Report - {YESTERDAYS_DATE}</h1>"""

    html_string += get_total_revenue_html(data)
    html_string += get_revenues_html(data)
    html_string += get_transactions_html(data)
    html_string += get_averages_html(data)
    html_string += get_popular_times_html(data)

    report = {"report": html_string}

    return report
