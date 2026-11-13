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

st.sidebar.header("Filters")
branches = df['branch'].unique()
selected_branch = st.sidebar.selectbox("Select Branch", branches)

filtered_df = df[df['branch'] == selected_branch]

c1, c2 = st.columns(2)
c1.metric("Total Orders", len(filtered_df))
total_revenue = filtered_df['total_sar'].sum()
c2.metric("Total Revenue", f"{total_revenue:,.2f} SAR")

st.subheader(f"Revenue by Product for {selected_branch}")
revenue_by_product = filtered_df.groupby('product')['total_sar'].sum()

fig, ax = plt.subplots(figsize=(8, 4))
revenue_by_product.plot(kind='bar', ax=ax, color='saddlebrown')
ax.set_ylabel("Revenue (SAR)")
ax.set_xlabel("Product")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

st.subheader("Recent Orders")
st.dataframe(filtered_df.head(20))
