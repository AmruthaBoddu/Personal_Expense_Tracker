import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

BUDGET_LIMIT = 20000  # Set your monthly budget here

def check_budget_alert(df):
    current_month = datetime.datetime.now().strftime("%Y-%m")
    df['Month'] = pd.to_datetime(df['Date']).dt.strftime("%Y-%m")
    month_total = df[df['Month'] == current_month]['Amount'].sum()

    if month_total >= BUDGET_LIMIT:
        return f"🚨 Budget Exceeded! You spent ₹{month_total:.2f} / ₹{BUDGET_LIMIT}."
    elif month_total >= 0.75 * BUDGET_LIMIT:
        return f"⚠️ Warning! Above 75% of budget: ₹{month_total:.2f} / ₹{BUDGET_LIMIT}."
    elif month_total >= 0.5 * BUDGET_LIMIT:
        return f"🔔 Notice! Above 50% of budget: ₹{month_total:.2f} / ₹{BUDGET_LIMIT}."
    else:
        return f"✅ You are within budget. Spent: ₹{month_total:.2f} / ₹{BUDGET_LIMIT}."

st.title("Personal Expense Tracker")

df = pd.read_csv("expenses.csv")

page = st.sidebar.selectbox("Menu", ["Home", "View Expenses", "Add Expense", "Summary"])

# Show Budget Alert on every page
alert = check_budget_alert(df)
if "Within" in alert:
    st.info(alert)
elif "50%" in alert:
    st.warning(alert)
else:
    st.error(alert)

# Pages
if page == "Home":
    st.header("Dashboard Overview")
    st.write("Your monthly budget status is displayed above.")

elif page == "View Expenses":
    st.header("All Expenses")
    st.dataframe(df)

elif page == "Add Expense":
    st.header("Add New Expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food","Transport","Bills","Entertainment","Groceries","Shopping","Other"])
    amount = st.number_input("Amount", min_value=1)
    if st.button("Add"):
        new = pd.DataFrame([[str(date),category,amount]], columns=df.columns)
        df2 = pd.concat([df,new], ignore_index=True)
        df2.to_csv("expenses.csv", index=False)
        st.success("Expense added successfully!")

elif page == "Summary":
    st.header("Summary Charts")
    cat_sum = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    ax.pie(cat_sum, labels=cat_sum.index, autopct="%1.1f%%")
    st.pyplot(fig)
