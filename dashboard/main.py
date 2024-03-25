"""Streamlit dashboard about T3 transactions."""

from os import environ

from dotenv import load_dotenv
import streamlit as st

from database import get_database_connection, load_transaction_data
from visualisations import get_transaction_bar_chart, get_transaction_line_chart
from visualisations import get_profit_pie_chart, get_weekday_bar_chart, get_revenue_line_chart
from visualisations import get_most_popular_truck, get_least_popular_truck
from visualisations import get_least_popular_truck_total, get_most_popular_truck_total
from filters import filter_by_date, filter_by_truck

if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection(environ)

    transactions = load_transaction_data(conn)

    min_date = transactions['at'].min().date()
    max_date = transactions['at'].max().date()

    date_range = st.sidebar.slider(
        'Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
        )
    selected_trucks = st.sidebar.multiselect("Selected trucks", transactions["name"].unique(),
                                              default=transactions["name"].unique())

    transactions = filter_by_date(transactions, date_range)
    transactions = filter_by_truck(transactions, selected_trucks)

    st.title("🚚 T3 Dashboard")

    st.markdown("---")

    upper_cols = st.columns(3)

    with upper_cols[0]:

        revenue = f"£{round(transactions['amount'].sum(), 2)}"
        st.metric('Total Revenue 💷', revenue)

    with upper_cols[1]:

        most_popular_truck = get_most_popular_truck(transactions)
        mpt_trans_num = get_most_popular_truck_total(transactions)
        st.metric('Most Popular Truck 📈', most_popular_truck, delta=mpt_trans_num)

    with upper_cols[2]:

        least_popular_truck = get_least_popular_truck(transactions)
        lpt_trans_num = get_least_popular_truck_total(transactions)
        st.metric('Least Popular Truck 📉', least_popular_truck, delta=-lpt_trans_num)


    if selected_trucks:

        st.header('Transactions per Hour')
        line_chart = get_transaction_line_chart(transactions)
        st.altair_chart(line_chart, use_container_width=True)

        lower_cols = st.columns(2)

        with lower_cols[0]:

            st.header("Transactions per Truck")
            bar_chart = get_transaction_bar_chart(transactions)
            st.altair_chart(bar_chart, use_container_width=True)

        with lower_cols[1]:
            st.header('Revenue Per Truck')
            pie_chart = get_profit_pie_chart(transactions)
            st.altair_chart(pie_chart, use_container_width=True)

        st.header('Transactions Per Weekday')
        weekday_chart = get_weekday_bar_chart(transactions)
        st.altair_chart(weekday_chart, use_container_width=True)

        st.header('Revenue Per Day')
        revenue_line_chart = get_revenue_line_chart(transactions)
        st.altair_chart(revenue_line_chart, use_container_width=True)
