import streamlit as st
import pandas as pd
from src.data_loader import OCDDataLoader
from src.analysis import OCDAnalysis
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập giao diện
st.set_page_config(page_title="OCD Patient Insights", layout="wide")

st.title("🏥 Hệ thống Phân tích & Phân cụm Bệnh nhân OCD")
st.markdown("Dự án nghiên cứu hành vi bệnh nhân dựa trên dữ liệu lâm sàng")

# 1. Load dữ liệu (Sử dụng Cache để tối ưu tốc độ trên Mac M1)
@st.cache_data
def get_data():
    loader = OCDDataLoader()
    df = loader.preprocess(loader.load_raw_data())
    df, _ = OCDAnalysis.perform_clustering(df)
    return df

df = get_data()

# 2. Sidebar - Bộ lọc dữ liệu
st.sidebar.header("Bộ lọc tìm kiếm")
selected_cluster = st.sidebar.multiselect("Chọn Cụm (Cluster):", 
                                         options=df['Cluster'].unique(), 
                                         default=df['Cluster'].unique())

filtered_df = df[df['Cluster'].isin(selected_cluster)]

# 3. Hiển thị các chỉ số chính (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tổng số bệnh nhân", len(filtered_df))
with col2:
    st.metric("Điểm Y-BOCS Trung bình", round(filtered_df['Total_Score'].mean(), 2))
with col3:
    st.metric("Tỷ lệ Di truyền (%)", f"{round(filtered_df['Family_History_Bin'].mean()*100, 1)}%")

# ... (giữ nguyên phần load dữ liệu phía trên)

# 4. Trực quan hóa tương tác
st.subheader("📊 Phân tích Xu hướng & Phân cụm")
tab1, tab2, tab3 = st.tabs(["Phân cụm AI", "Kiểm định Thống kê", "Mạng lưới Triệu chứng"])

with tab1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x='Age', y='Total_Score', hue='Cluster', palette='viridis', ax=ax)
    st.pyplot(fig) # Hiển thị phân cụm

with tab2:
    st.write("### Kiểm định ANOVA: Tác động của Hôn nhân")
    f_stat, p_val = OCDAnalysis.run_anova(df, 'Marital Status', 'Total_Score') # Chạy kiểm định
    
    col_a, col_b = st.columns(2)
    col_a.metric("F-Statistic", round(f_stat, 2))
    col_b.metric("P-Value", round(p_val, 4))
    
    if p_val < 0.05:
        st.success(f"Kết quả có ý nghĩa thống kê ($p < 0.05$). Tình trạng hôn nhân thực sự ảnh hưởng đến mức độ nghiêm trọng của bệnh.")
    else:
        st.warning("Chưa đủ bằng chứng thống kê để khẳng định sự khác biệt.")
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.pointplot(data=df, x='Marital Status', y='Total_Score', capsize=.1, color='#E74C3C', ax=ax2)
    st.pyplot(fig2) # Biểu đồ xu hướng hôn nhân

with tab3:
    st.write("### Mạng lưới kết hợp Ám ảnh - Cưỡng chế")
    st.info("Phần này hiển thị các 'luật hành vi' mạnh nhất được tìm thấy bằng thuật toán Apriori.")
    # Bạn có thể gọi hàm vẽ sơ đồ mạng lưới từ src/visualizer.py tại đây
    st.image("reports/symptom_network.png", caption="Sơ đồ mạng lưới triệu chứng (Đã xuất từ main.py)")