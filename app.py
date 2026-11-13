import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    return pd.read_csv('cafe_sales.csv')

df = load_data()

st.title("Coffee Chain Sales Dashboard")

branches = df['branch'].unique()
selected_branch = st.selectbox("Select Branch", branches)

filtered_df = df[df['branch'] == selected_branch]

total_rev = filtered_df['total_sar'].sum()
st.metric(label=f"Total Revenue (SAR) for {selected_branch}", value=f"{total_rev:,.2f} SAR")

st.subheader("Revenue by Product")
revenue_by_product = filtered_df.groupby('product')['total_sar'].sum()
st.bar_chart(revenue_by_product)
