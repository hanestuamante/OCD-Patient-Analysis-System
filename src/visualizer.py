import matplotlib.pyplot as plt
import seaborn as sns
import os
import networkx as nx

class OCDVisualizer:
    def __init__(self, df, report_dir='reports'):
        self.df = df
        self.report_dir = report_dir
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

    def plot_marital_impact(self):
        plt.figure(figsize=(10, 6))
        sns.pointplot(data=self.df, x='Marital Status', y='Total_Score', capsize=.1, color='#E74C3C')
        plt.title('Xu hướng điểm Y-BOCS theo Tình trạng hôn nhân')
        plt.savefig(f'{self.report_dir}/marital_impact.png')
        plt.close()

    def plot_education_duration(self):
        plt.figure(figsize=(12, 7))
        sns.violinplot(data=self.df, x='Education Level', y='Duration of Symptoms (months)', inner="quartile")
        plt.title('Phân bổ Thời gian mắc bệnh theo Trình độ học vấn')
        plt.savefig(f'{self.report_dir}/education_duration.png')
        plt.close()

    def plot_cluster_profile(self):
        plt.figure(figsize=(12, 8))
        sns.scatterplot(data=self.df, x='Age', y='Total_Score', hue='Cluster', palette='viridis')
        plt.title('Phân cụm bệnh nhân OCD (k=4)')
        plt.savefig(f'{self.report_dir}/cluster_distribution.png')
        plt.close()

    def save_network_graph(self, rules):
        """Tạo và lưu sơ đồ mạng lưới triệu chứng từ kết quả Apriori"""
        G = nx.DiGraph()
        top_rules = rules.sort_values('lift', ascending=False).head(20)
        
        for _, row in top_rules.iterrows():
            ant = list(row['antecedents'])[0]
            con = list(row['consequents'])[0]
            G.add_edge(ant, con, weight=row['lift'])

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=1.5, seed=42)
        nx.draw_networkx(G, pos, node_size=2500, node_color='#AED6F1', font_size=10, alpha=0.8)
        
        plt.title('Sơ đồ Mạng lưới kết hợp Ám ảnh - Cưỡng chế')
        plt.savefig(f'{self.report_dir}/symptom_network.png') # Đây là file app.py đang tìm
        plt.close()