# load_to_postgres.py
import os
import sys
import time
import urllib.parse

import pandas as pd
from sqlalchemy import create_engine

# Optional: load a local .env file in development (install python-dotenv)
from dotenv import load_dotenv
load_dotenv()  # loads variables from .env into os.environ

# ---------- Config ----------
# File to read (set this to the actual file you have)
input_file = 'combined_ukhm_clean.csv'  # or .parquet if you have parquet

# Table name
table_name = 'price_paied'

# ---------- Read DB credentials from env ----------
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME')

# Helpful error if required env var is missing:
missing = [k for k, v in {
    'DB_USER': DB_USER,
    'DB_PASSWORD': DB_PASSWORD,
    'DB_NAME': DB_NAME
}.items() if not v]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    print("Set them locally (or use a .env file in development). Exiting.")
    sys.exit(1)

# ---------- Load file ----------
print(f"Reading clean data from '{input_file}'...")
try:
    if input_file.lower().endswith('.parquet'):
        df = pd.read_parquet(input_file)
    else:
        df = pd.read_csv(input_file)
    print("Clean data loaded into DataFrame successfully.")
except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
    print("Please ensure that the ETL script has generated it.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# ---------- Build DB URL safely (quote password) ----------
# Use psycopg2 driver; make sure it's installed in your environment.
quoted_password = urllib.parse.quote_plus(DB_PASSWORD)
db_url = f"postgresql+psycopg2://{DB_USER}:{quoted_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ---------- Create engine and push ----------
try:
    engine = create_engine(db_url)
    print("Database engine created successfully.")
except Exception as e:
    print(f"Error creating database engine: {e}")
    sys.exit(1)

print(f"Loading data into table '{table_name}'...")
start_time = time.time()
try:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='replace',
        index=False,
        chunksize=50000
    )
    elapsed = time.time() - start_time
    print(f"Successfully loaded {len(df)} rows into PostgreSQL in {elapsed:.2f} seconds.")
except Exception as e:
    print(f"An error occurred during the data loading: {e}")
    sys.exit(1)
