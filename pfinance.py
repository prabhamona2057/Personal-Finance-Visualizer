import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Personal Finance Visualizer", layout="wide")

# --- DATA GENERATOR (For testing) ---
def generate_sample_data():
    categories = ['Rent', 'Groceries', 'Utilities', 'Entertainment', 'Dining Out', 'Transport']
    data = {
        'Date': [datetime.now() - timedelta(days=x) for x in range(100)],
        'Category': [np.random.choice(categories) for _ in range(100)],
        'Amount': [round(np.random.uniform(10, 500), 2) for _ in range(100)],
        'Note': ['Sample transaction' for _ in range(100)]
    }
    return pd.DataFrame(data)

# --- APP UI ---
st.title("💰 Personal Finance Visualizer")
st.markdown("Upload your bank statement (CSV) or use sample data to analyze your spending.")

uploaded_file = st.file_uploader("Upload CSV (Required columns: Date, Category, Amount)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
else:
    if st.checkbox("Use Sample Data"):
        df = generate_sample_data()
    else:
        st.info("Please upload a file or check the sample data box.")
        st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Settings")
date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
filtered_df = df[(df['Date'] >= pd.to_datetime(date_range[0])) &
                 (df['Date'] <= pd.to_datetime(date_range[1]))]

# --- KEY METRICS ---
total_spent = filtered_df['Amount'].sum()
avg_transaction = filtered_df['Amount'].mean()

m1, m2, m3 = st.columns(3)
m1.metric("Total Spending", f"₹{total_spent:,.2f}")
m2.metric("Avg. Transaction", f"₹{avg_transaction:,.2f}")
m3.metric("Transactions", len(filtered_df))

# --- VISUALIZATIONS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spending by Category")
    fig_pie = px.pie(filtered_df, values='Amount', names='Category', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Spending Over Time")
    daily_spend = filtered_df.groupby('Date')['Amount'].sum().reset_index()
    fig_line = px.line(daily_spend, x='Date', y='Amount', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

st.subheader("Transaction Breakdown")
st.dataframe(filtered_df.sort_values(by='Date', ascending=False), use_container_width=True)
