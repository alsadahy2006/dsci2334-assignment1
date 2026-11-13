import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# إعدادات الصفحة
st.set_page_config(page_title="Qahwa Corner Dashboard", page_icon="☕", layout="wide")

# العنوان الرئيسي
st.title("☕ Coffee Chain Sales Dashboard")
st.write("Explore sales performance across branches and products.")

# تحميل وتطهير البيانات
@st.cache_data
def load_data():
    df = pd.read_csv("cafe_sales.csv")
    df.columns = df.columns.str.strip().str.lower()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# --- القائمة المنسدلة ومحدد الفروع في الواجهة الرئيسية معاً ---
st.markdown("### Select Branch to Filter Data")
branches = df['branch'].unique()
selected_branch = st.selectbox("Choose a branch:", branches, key="branch_selector")

# تصفية البيانات حسب الفرع المختار
filtered_df = df[df['branch'] == selected_branch]

st.markdown("---")

# عرض المؤشرات المرتبطة بالفرع المختار
st.subheader(f"Performance Metrics for: {selected_branch}")
col1, col2 = st.columns(2)

total_orders = len(filtered_df)
total_revenue = filtered_df['total_sar'].sum()

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue (SAR)", f"{total_revenue:,.2f} SAR")

st.markdown("---")

# الرسم البياني للإيرادات حسب المنتج للفرع المحدد
st.subheader(f"Revenue by Product for {selected_branch}")
revenue_by_product = filtered_df.groupby('product')['total_sar'].sum()

fig, ax = plt.subplots(figsize=(10, 5))
revenue_by_product.plot(kind='bar', ax=ax, color='saddlebrown')
ax.set_ylabel("Revenue (SAR)")
ax.set_xlabel("Product")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# عرض جدول البيانات للطلبات الحديثة التابعة للفرع
st.subheader("Recent Orders Data")
st.dataframe(filtered_df.head(20))
