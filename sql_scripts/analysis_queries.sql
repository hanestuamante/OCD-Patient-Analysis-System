-- Tỉ lệ phần trăm nhóm nữ / nam mắc bệnh obsession
SELECT 
    Gender,
    COUNT(`Patient ID`) AS patient_count,
    ROUND(AVG(`Y-BOCS Score (Obsessions)`), 2) AS avg_obs_score,
    ROUND(COUNT(`Patient ID`) * 100.0 / SUM(COUNT(`Patient ID`)) OVER(), 2) AS percentage
FROM ocd_patient_dataset
GROUP BY Gender;

-- 
SELECT 
    Ethnicity,
    COUNT(`Patient ID`) AS eth_patient_count,
    ROUND(AVG(`Y-BOCS Score (Obsessions)`), 2) AS avg_obs_score
FROM ocd_patient_dataset
GROUP BY Ethnicity
ORDER BY eth_patient_count DESC;
							
SELECT
    DATE_FORMAT(`OCD Diagnosis Date`, '%Y-%m-01 00:00:00') AS month,
    COUNT(`Patient ID`) AS diagnosis_count
FROM ocd_patient_dataset
GROUP BY month
ORDER BY month;

SELECT 
    `Obsession Type`,
    COUNT(`Patient ID`) AS obsession_count,
    ROUND(AVG(`Y-BOCS Score (Obsessions)`), 2) AS avg_obs_score
FROM ocd_patient_dataset
GROUP BY 1
ORDER BY obsession_count DESC;

SELECT 
    `Compulsion Type`,
    COUNT(`Patient ID`) AS compulsion_count,
    ROUND(AVG(`Y-BOCS Score (Compulsions)`), 2) AS avg_com_score
FROM ocd_patient_dataset
GROUP BY 1
ORDER BY compulsion_count DESC;


SELECT 
	Age,
	COUNT(`Patient ID`) AS patient_count
FROM ocd_patient_dataset
GROUP BY Age;

SELECT 
    `Patient ID`,
    Age,
    Gender,
    `Y-BOCS Score (Obsessions)`,
    `Y-BOCS Score (Compulsions)`,
    (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) AS Total_YBOCS,
    CASE 
        WHEN (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) <= 7 THEN 'Subclinical'
        WHEN (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) <= 15 THEN 'Mild'
        WHEN (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) <= 23 THEN 'Moderate'
        WHEN (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) <= 31 THEN 'Severe'
        ELSE 'Extreme'
    END AS Severity_Level
FROM ocd_patient_dataset 
ORDER BY Total_YBOCS DESC;

SELECT 
    CASE 
        WHEN (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) <= 7 THEN 'Subclinical'
        WHEN (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) <= 15 THEN 'Mild'
        WHEN (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) <= 23 THEN 'Moderate'
        WHEN (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) <= 31 THEN 'Severe'
        ELSE 'Extreme'
    END AS Severity_Level,
    COUNT(*) AS Patient_Count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS Percentage
FROM ocd_patient_dataset
GROUP BY Severity_Level
ORDER BY Patient_Count DESC;

SELECT 
    CASE 
        WHEN Age < 12 THEN 'Child'
        WHEN Age BETWEEN 12 AND 17 THEN 'Teenager'
        WHEN Age BETWEEN 18 AND 30 THEN 'Young Adult'
        WHEN Age BETWEEN 31 AND 55 THEN 'Middle-aged'
        ELSE 'Senior'
    END AS Age_Group,
    COUNT(*) AS Patient_Count,
    ROUND(AVG(`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`), 2) AS Avg_Total_YBOCS
FROM ocd_patient_dataset
GROUP BY Age_Group
ORDER BY 1 DESC;

SELECT 
    COUNT(*) AS Total_Extreme_Patients,
    SUM(CASE WHEN `Family History of OCD` = 'Yes' THEN 1 ELSE 0 END) AS Has_Family_History,
    ROUND(
        SUM(CASE WHEN `Family History of OCD` = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        2
    ) AS Percentage_Family_History
FROM ocd_patient_dataset
WHERE (`Y-BOCS Score (Obsessions)` + `Y-BOCS Score (Compulsions)`) > 31;