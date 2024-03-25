"""Functions for creating data visualisations."""

import altair as alt
import pandas as pd

TRUCK_COLOURS = ['#2A9D8F', '#FFD670', '#E0BAD7', '#E76F51', '#B8336A', '#51A0F5']
PAYMENT_COLOURS = ['#ED7B84', '#D6FFB7']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_transaction_bar_chart(data: pd.DataFrame) -> alt.Chart:
    """Returns a bar chart showing total transactions per truck, split by payment type."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X('name', title="Truck Name", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('count(amount)', title='Transactions'),
        color=alt.Color('type', title='Payment Type', scale=alt.Scale(range=PAYMENT_COLOURS)),
        xOffset='type',
        )


def get_transaction_line_chart(data: pd.DataFrame) -> alt.Chart:
    """Returns a line chart showing total transactions per hour of the day per truck."""

    hour_data = data.copy()
    hour_data['at'] = pd.to_datetime(hour_data['at']).dt.hour

    return alt.Chart(hour_data).mark_line().encode(
        x=alt.X('at:O', title='Hour of Day'),
        y=alt.Y('count(amount)', title='Transactions'),
        color=alt.Color('name', title='Truck Name', scale=alt.Scale(range=TRUCK_COLOURS))
    )

def get_profit_pie_chart(data: pd.DataFrame) -> alt.Chart:
    """Returns a pie chart showing profit per truck."""

    return alt.Chart(data).mark_arc().encode(
        theta=alt.Theta('sum(amount)', title='Profit', ),
        color=alt.Color('name', title='Truck', scale=alt.Scale(range=TRUCK_COLOURS)),
        tooltip=alt.Tooltip(['sum(amount):Q'],format=',.2f', title="Profit")
    )


def get_weekday_bar_chart(data: pd.DataFrame) -> alt.Chart:
    """Returns a bar chart of transactions per weekday per truck."""

    weekday_data = data.copy()
    weekday_data['at'] = pd.to_datetime(weekday_data['at']).dt.day_name()
    return alt.Chart(weekday_data).mark_bar().encode(
        x=alt.X('at', title='Weekday', sort=WEEKDAYS),
        y=alt.Y('count(amount)', title='Transactions'),
        color=alt.Color('name', title='Truck Name', scale=alt.Scale(range=TRUCK_COLOURS)),
        xOffset='name'
    )

def get_revenue_line_chart(data: pd.DataFrame) -> alt.Chart:
    """Returns a line chart of revenue per truck per day."""

    date_data = data.copy()
    date_data['at'] = pd.to_datetime(date_data['at']).dt.date

    return alt.Chart(data).mark_line().encode(
        x=alt.X('at', title='Date', timeUnit='yearmonthdate'),
        y=alt.Y('sum(amount)', title='Revenue'),
        color=alt.Color('name', title='Truck Name', scale=alt.Scale(range=TRUCK_COLOURS))
    )


def get_most_popular_truck(data: pd.DataFrame):
    """Returns the truck with the most transactions."""

    new_data = data.copy()

    top_data = new_data.groupby('name').amount.agg('count').sort_values(ascending=False).head(1).to_dict()

    return list(top_data.keys())[0]

def get_least_popular_truck(data: pd.DataFrame) -> alt.Chart:
    """Returns the truck with the most transactions."""

    new_data = data.copy()

    bottom_data = new_data.groupby('name').amount.agg('count').sort_values(ascending=True).head(1).to_dict()

    return list(bottom_data.keys())[0]
        

def get_most_popular_truck_total(data: pd.DataFrame):
    """Returns the truck with the most transactions."""

    new_data = data.copy()

    top_data = new_data.groupby('name').amount.agg('count').sort_values(ascending=False).head(1).to_dict()

    return list(top_data.values())[0]

def get_least_popular_truck_total(data: pd.DataFrame) -> alt.Chart:
    """Returns the truck with the most transactions."""

    new_data = data.copy()

    bottom_data = new_data.groupby('name').amount.agg('count').sort_values(ascending=True).head(1).to_dict()

    return list(bottom_data.values())[0]