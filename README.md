OCD Patient Analysis Project
Dự án này tập trung vào việc phân tích dữ liệu lâm sàng của bệnh nhân OCD để khám phá các "kiểu hình" (phenotypes) bệnh lý thông qua Machine Learning và Thống kê học. Thay vì dựa trên các nhãn mức độ bệnh truyền thống, dự án sử dụng thuật toán phân cụm để tìm ra các nhóm bệnh nhân có đặc điểm tương đồng về nhân khẩu học và hành vi.


Kiến trúc dự án (Modular Architecture)
Dự án được tổ chức theo cấu trúc module hóa chuyên nghiệp để đảm bảo tính mở rộng và tái sử dụng:

src/data_loader.py: Quản lý kết nối MySQL và thực hiện Feature Engineering (tính toán Total_Score, mã hóa biến định danh).

src/analysis.py: Chúa các lớp xử lý thuật toán như K-Means Clustering và các phép kiểm định thống kê ANOVA.

src/visualizer.py: Đóng gói các hàm trực quan hóa dữ liệu nâng cao, tự động xuất báo cáo ra thư mục /reports.

main.py: File điều phối trung tâm (Orchestrator) thực thi toàn bộ quy trình từ dữ liệu thô đến kết quả phân tích.

Phương pháp nghiên cứu & Kết quả (Methodology)
1. Phân cụm học máy (Unsupervised Learning)Sử dụng Phương pháp Khuỷu tay (Elbow Method) để xác định số lượng cụm tối ưu dựa trên chỉ số WCSS (Within-Cluster Sum of Squares):
2. Insight: Thuật toán nhận diện được Cluster 0 (Người trẻ, không di truyền) là nhóm có mức độ bệnh nặng nhất với điểm trung bình ~43.1.
3. Kiểm định Thống kê (Statistical Inference)Phân tích ảnh hưởng của các yếu tố nhân khẩu học tới mức độ nghiêm trọng của bệnh:Tình trạng hôn nhân: Phép thử ANOVA cho thấy giá trị $P < 0.05$, khẳng định sự khác biệt có ý nghĩa thống kê. Nhóm Single có xu hướng bị nặng hơn nhóm Married.Trình độ học vấn: Biểu đồ Violin Plot chỉ ra trình độ học vấn ảnh hưởng đến hình thái phân bổ thời gian mắc bệnh, đặc biệt là nhóm Some College có sự phân tán rộng hơn về thời gian chịu đựng triệu chứng.
4. Khai phá Luật kết hợp (Association Rules)Sử dụng thuật toán Apriori và sơ đồ mạng lưới (Network Graph) để tìm mối liên hệ giữa các loại ám ảnh và cưỡng chế. Việc này giúp dự báo các triệu chứng cưỡng chế đi kèm dựa trên loại ám ảnh của bệnh nhân.

Công nghệ sử dụng
Database: MySQL

Language: Python 3.14

Libraries: pandas, scikit-learn, scipy, seaborn, matplotlib, mlxtend, networkx, sqlalchemy
