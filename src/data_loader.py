import pandas as pd
from sqlalchemy import create_engine

class OCDDataLoader:
    def __init__(self, db_url="mysql+pymysql://root:@127.0.0.1/ocd_analysis"):
        self.engine = create_engine(db_url)
        
    def load_raw_data(self):
        query = "SELECT * FROM ocd_patient_dataset"
        return pd.read_sql(query, self.engine)
    
    def preprocess(self, df):
        # Tạo Total_Score và Severity
        df['Total_Score'] = df['Y-BOCS Score (Obsessions)'] + df['Y-BOCS Score (Compulsions)']
        
        def classify_severity(score):
            if score <= 15: return 'Mild'
            if score <= 23: return 'Moderate'
            if score <= 31: return 'Severe'
            return 'Extreme'
        
        df['Severity'] = df['Total_Score'].apply(classify_severity)
        df.columns = df.columns.str.strip()
        df['Family_History_Bin'] = df['Family History of OCD'].map({'Yes': 1, 'No': 0})
        return df