import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Qahwa Corner Dashboard", page_icon="☕")
st.title("☕ Qahwa Corner Sales Dashboard")
st.write("Explore sales performance across branches and products for Qahwa Corner.")

@st.cache_data
def load_data():
    df = pd.read_csv("cafe_sales.csv")
    df.columns = df.columns.str.strip()
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar branch selector
st.sidebar.header("Filters")
branches = df['branch'].unique()
selected_branch = st.sidebar.selectbox("Select Branch", branches)

# Filter data
filtered_df = df[df['branch'] == selected_branch]

# Key metrics
c1, c2 = st.columns(2)
c1.metric("Total Orders", len(filtered_df))
total_revenue = filtered_df['total_sar'].sum()
c2.metric("Total Revenue", f"{total_revenue:,.2f} SAR")

# Bar chart of revenue by product
st.subheader(f"Revenue by Product for {seproduct_revenue = filtered_df.groupby("product")["total_sar"].sum()lected_branch}")
product_revenue = filtered_df.groupby('product_name')['total_sar'].sum()

fig, ax = plt.subplots()
product_revenue.plot(kind='bar', ax=ax, color='saddlebrown')
ax.set_ylabel("Revenue (SAR)")
ax.set_xlabel("Product")
st.pyplot(fig)

# Data table
st.subheader("Recent Orders")
st.dataframe(filtered_df.head(20))
