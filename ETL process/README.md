# Designing a Simple Data Pipeline and ETL Process

## Group Members

| Name                  | Student ID    | Role/Notes             |
|----------------------|--------------|-----------------------|
| **Surafel Asfawosen** | DBU1501482   | Team Lead             |
| **Nardos Mola**       | DBU1501397   | Data Cleaning         |
| **Ephrata Yeshaneh**  | DBU1501631   | Data Transformation   |
| **Bethlehem Asres**   | DBU1501062   | Database Integration  |
| **Besufekad Ayalkbet**| DBU1501050   | ETL Implementation    |
| **Beiment Yealmbirhan** | DBU1501024 | Testing & Validation  |
| **Yonatan Kiros**     | DBU1501656   | Documentation         |

---

## Project Overview
This project demonstrates a **data pipeline and ETL process** using Python and PostgreSQL. The dataset is the **UK HM Land Registry Price Paid Data (2021–2025)**, publicly available from the UK government: [Price Paid Data](https://www.gov.uk/guidance/about-the-price-paid-data). It contains over **2 million property transaction records**, including sale price, property type, date of transfer, postcode, town, district, and transaction category.  

We chose this dataset because it provides **real-world insights into the UK property market**. Analyzing these transactions allows businesses, real estate agencies, and policymakers to understand **price trends, property type distributions, and regional variations**, which are critical for strategic decision-making in real estate and investment planning.

---

## ETL Process Description
Our ETL workflow is designed to **extract, clean, transform, and load** this large dataset efficiently:

1. **Extraction**
   - Load multiple CSV files (one per year) and combine them into a single dataset (`combined_ukhm.csv`).  
   - Ensure consistent column naming and formatting.

2. **Transformation**
   - Identify and handle missing values; drop columns or rows based on thresholds.  
   - Remove duplicate rows.  
   - Convert categorical codes into **readable labels**:
     - `property_type`: D, S, T, F, O → Detached, Semi-Detached, Terraced, Flat/Maisonette, Other  
     - `old_new`: Y/N → New Build / Established  
     - `duration`: F/L → Freehold / Leasehold  
     - `ppd_category_type`: A/B → Standard / Additional  
     - `record_status`: A/C/D → Added / Changed / Deleted  
   - Convert numeric and date columns to appropriate types (`price`, `date_of_transfer`).  
   - Save cleaned data as `combined_ukhm_clean.csv` and `combined_ukhm_clean.parquet`.

3. **Loading**
   - Use Python and SQLAlchemy to load the cleaned dataset into **PostgreSQL**.  
   - Database credentials are stored in a `.env` file (kept local and never pushed to GitHub).  
   - Load data efficiently using chunking to handle large volumes.

---

## Tools and Libraries
- **Python 3.x**, **Pandas**, **SQLAlchemy**, **python-dotenv**  
- **PostgreSQL** as the relational database  

---

## How to Run
1. Clone the repository.  
2. Create a `.env` file in the project folder with your database credentials:

```text
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
