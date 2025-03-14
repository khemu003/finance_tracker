import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_handler import fetch_transactions, add_transaction, delete_transaction, change_transaction

# Streamlit UI
st.set_page_config(page_title="Finance Tracker", layout="wide")

if "user_id" not in st.session_state or st.session_state["user_id"] is None:
    st.warning("You need to log in to access this page.")
    st.stop()

# Title
st.title("📊 Personal Finance Dashboard")


# Fetch Data
df = fetch_transactions()


# Sidebar: Add new transaction
st.sidebar.header("➕ Add New Transaction")
date = st.sidebar.date_input("Date")
category = st.sidebar.text_input("Category")
amount = st.sidebar.number_input("Amount", min_value=0.0)
txn_type = st.sidebar.selectbox("Type", ["income", "expense"])
description = st.sidebar.text_area("Description")

if st.sidebar.button("Add Transaction"):
    add_transaction(date, category, amount, txn_type, description)
    st.sidebar.success("Transaction Added Successfully!")


# Sidebar: Delete transaction
st.sidebar.header("❌ Delete Transaction")
delete_id = st.sidebar.number_input("Delete Transaction ID", min_value=1, step=1)

if st.sidebar.button("Delete Transaction"):
    delete_transaction(delete_id)
    st.sidebar.success("Transaction Deleted Successfully!")


# Sidebar: change transaction
st.sidebar.header("❌ Change Transaction")
change_id = st.sidebar.number_input("Change Transaction ID", min_value=1, step=1)
date = st.sidebar.date_input("Change Date")
category = st.sidebar.text_input("Change Category")
amount = st.sidebar.number_input("Change Amount", min_value=0.0)
txn_type = st.sidebar.selectbox("Change Type", ["income", "expense"])
description = st.sidebar.text_area("Change Description")

if st.sidebar.button("Change Transaction"):
    change_transaction(date, category, amount, txn_type, description, change_id)
    st.sidebar.success("Transaction change Successfully!")


# Show Data
st.subheader("📌 Transactions")
if df is None:
    st.error("Error fetching transactions!")
else:
    st.dataframe(df)


# Summary Metrics
income = df[df['type'] == 'income']['amount'].sum()
expense = df[df['type'] == 'expense']['amount'].sum()
balance = income - expense


# Display summary metrics
st.metric("Total Income", f"₹{income:,.2f}", "green")
st.metric("Total Expenses", f"₹{expense:,.2f}", "red")
st.metric("Balance", f"₹{balance:,.2f}", "blue")


income_df = df[df["type"] == "income"]
expense_df = df[df["type"] == "expense"]


# Visualization options
option = st.selectbox("Select Analysis", [
    "Expense Overview", "Income Overview", "Income vs. Expense", "Account Analysis"
])

# Expense Overview
if option == "Expense Overview" and not expense_df.empty:
    df_expense = expense_df.groupby("category")["amount"].sum()
    if not df_expense.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = sns.color_palette("husl", len(df_expense))
        wedges, texts, autotexts = ax.pie(
            df_expense, labels=df_expense.index, autopct='%1.1f%%', startangle=90,
            colors=colors, wedgeprops={'edgecolor': 'black'}, pctdistance=0.85,
            textprops={'fontsize': 10}
        )
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plt.gca().add_artist(centre_circle)
        
        plt.text(0, 0, 'Expenses', ha='center', va='center', fontsize=14, fontweight='bold', color='black')
        
        plt.legend(wedges, df_expense.index, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.axis('equal')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("No expense data available to plot.")

# Income Overview
elif option == "Income Overview" and not income_df.empty:
    fig, ax = plt.subplots(figsize=(6, 6))
    income_summary = income_df.groupby("category")["amount"].sum()
    if not income_summary.empty:
        ax.pie(income_summary, labels=income_summary.index, autopct='%1.1f%%', colors=['green', 'blue'], textprops={'fontsize': 10})
        ax.set_title("Income Overview")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("No income data available.")

# Income vs Expense
elif option == "Income vs. Expense":
    fig, ax = plt.subplots()
    ax.bar(["Income", "Expense"], [income, expense], color=["green", "red"])
    ax.set_title("Income vs. Expense")
    plt.tight_layout()
    st.pyplot(fig)

# Account Analysis Placeholder
elif option == "Account Analysis":
    st.write("Feature coming soon!")

st.write("\n\n")