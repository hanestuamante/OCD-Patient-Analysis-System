from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

class OCDAnalysis:
    @staticmethod
    def perform_clustering(df, n_clusters=4):
        # Sử dụng các đặc trưng như trong ảnh
        X = df[['Age', 'Total_Score', 'Family_History_Bin']]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['Cluster'] = model.fit_predict(X_scaled)
        return df, model

    @staticmethod
    def run_anova(df, group_col, value_col):
        # Kiểm định cho sự khác biệt hôn nhân
        groups = [group[value_col].values for name, group in df.groupby(group_col)]
        f_stat, p_val = stats.f_oneway(*groups)
        return f_stat, p_val
    
    @staticmethod
    def get_association_rules(df):
        """Tính toán luật kết hợp giữa Ám ảnh và Cưỡng chế"""
        # 1. Chuẩn bị dữ liệu One-hot encoding cho 2 cột triệu chứng
        df_rules = pd.get_dummies(df[['Obsession Type', 'Compulsion Type']])
        
        # 2. Tìm tập mục phổ biến với support >= 5%
        frequent_itemsets = apriori(df_rules, min_support=0.05, use_colnames=True)
        
        # 3. Trích xuất các luật kết hợp với Lift > 1.0
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
        return rules