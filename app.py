import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date
from db import init_db, add_expense, fetch_expenses
from utils import export_to_excel

st.set_page_config("💰 Expense Tracker", layout="wide")
st.title("💸 Personal Budget & Expense Tracker")

# --- Init DB ---
init_db()

# --- Login (Optional) ---
PASSWORD = "admin123"  # Change this
password = st.text_input("Enter Password to Access:", type="password")
if password != PASSWORD:
    st.warning("Enter correct password to use the app.")
    st.stop()

# --- Input Section ---
with st.expander("➕ Add New Expense"):
    col1, col2 = st.columns(2)
    amount = col1.number_input("Amount (₹)", min_value=0.0, step=0.5)
    category = col2.selectbox("Category", ["Food", "Transport", "Bills", "Shopping", "Health", "Other"])
    date_input = st.date_input("Date", value=date.today())
    description = st.text_input("Description (optional)")
    if st.button("Add Expense"):
        add_expense(str(date_input), category, amount, description)
        st.success("Expense added!")

# --- Fetch Data ---
df = fetch_expenses()
df['date'] = pd.to_datetime(df['date'])

# --- Date Range Filter ---
st.subheader("📆 Filter Expenses")
start_date = st.date_input("Start Date", min(df['date']))
end_date = st.date_input("End Date", max(df['date']))

filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

st.dataframe(filtered_df, use_container_width=True)

# --- Export to Excel ---
if st.button("📁 Export to Excel"):
    file_path = export_to_excel(filtered_df)
    st.success("File exported!")
    with open(file_path, "rb") as f:
        st.download_button("Download Excel File", f, file_name=file_path)

# --- Summary ---
st.subheader("📊 Expense Summary")

if not filtered_df.empty:
    total = filtered_df["amount"].sum()
    st.metric("Total Spent", f"₹ {total:.2f}")

    # Pie chart by category
    pie_data = filtered_df.groupby("category")["amount"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    # Line chart over time
    st.subheader("📈 Expense Over Time")
    line_chart = px.line(filtered_df, x="date", y="amount", color="category", markers=True)
    st.plotly_chart(line_chart, use_container_width=True)
else:
    st.info("No expenses found for the selected date range.")
