import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# إعدادات الصفحة
st.set_page_config(page_title="Qahwa Corner Dashboard", page_icon="☕", layout="wide")

st.title("☕ Coffee Chain Sales Dashboard")
st.write("Explore sales performance across branches and products.")

# تحميل وتطهير البيانات تلقائياً لمنع أي أخطاء في أسماء الأعمدة
@st.cache_data
def load_data():
    df = pd.read_csv("cafe_sales.csv")
    # توحيد أسماء الأعمدة بحذف المسافات وتحويلها لأحرف صغيرة
    df.columns = df.columns.str.strip().str.lower()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# التأكد من وجود الأعمدة المطلوبة لتجنب الأخطاء
required_cols = ['branch', 'product', 'total_sar', 'quantity']
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"خطأ: الأعمدة التالية غير موجودة في ملف الـ CSV: {missing_cols}")
else:
    # الشريط الجانبي لاختيار الفرع
    st.sidebar.header("Filters")
    branches = df['branch'].unique()
    selected_branch = st.sidebar.selectbox("Select Branch", branches)

    # تصفية البيانات حسب الفرع المختار
    filtered_df = df[df['branch'] == selected_branch]

    # مؤشرات الأداء الرئيسية (Metrics)
    st.subheader(f"Performance Metrics for: {selected_branch}")
    col1, col2 = st.columns(2)

    total_orders = len(filtered_df)
    total_revenue = filtered_df['total_sar'].sum()

    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Total Revenue (SAR)", f"{total_revenue:,.2f} SAR")

    st.markdown("---")

    # الرسم البياني للإيرادات حسب المنتج
    st.subheader("Revenue by Product")
    revenue_by_product = filtered_df.groupby('product')['total_sar'].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    revenue_by_product.plot(kind='bar', ax=ax, color='saddlebrown')
    ax.set_ylabel("Revenue (SAR)")
    ax.set_xlabel("Product")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # عرض جدول البيانات للطلبات الحديثة
    st.subheader("Recent Orders Data")
    st.dataframe(filtered_df.head(20))
