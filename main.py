# File main.py hoàn chỉnh
from src.data_loader import OCDDataLoader
from src.analysis import OCDAnalysis
from src.visualizer import OCDVisualizer

def main():
    print("--- BẮT ĐẦU QUY TRÌNH PHÂN TÍCH OCD ---")
    
    # 1. Tải và tiền xử lý dữ liệu
    loader = OCDDataLoader()
    df = loader.preprocess(loader.load_raw_data())
    
    # 2. Thực hiện các phân tích logic
    # Phân cụm
    df, model = OCDAnalysis.perform_clustering(df)
    # Kiểm định ANOVA
    f_stat, p_val = OCDAnalysis.run_anova(df, 'Marital Status', 'Total_Score')
    # TÍNH TOÁN RULES Ở ĐÂY (Sửa lỗi undefined variable)
    rules = OCDAnalysis.get_association_rules(df)
    
    # 3. Xuất kết quả ra file ảnh
    viz = OCDVisualizer(df)
    viz.plot_cluster_profile()
    viz.plot_marital_impact()
    viz.plot_education_duration() #
    viz.save_network_graph(rules) # Giờ rules đã có giá trị hợp lệ
    
    print(f"✓ Hoàn tất. ANOVA P-value: {p_val:.4f}")
    print("--- DỰ ÁN HOÀN TẤT ---")

if __name__ == "__main__":
    main()