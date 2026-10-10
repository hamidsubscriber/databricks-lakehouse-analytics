"""
Central configuration for the Lakehouse Analytics pipeline (Project 3).
"""

CATALOG = "dev"
STAGING_SCHEMA = "staging"
CURATED_SCHEMA = "curated"

# source files
CUSTOMERS_INITIAL_PATH = "/Volumes/dev/staging/raw_files/customers_initial.csv"
CUSTOMERS_UPDATES_PATH = "/Volumes/dev/staging/raw_files/customers_updates.csv"
PRODUCTS_PATH = "/Volumes/dev/staging/raw_files/products.csv"
ORDERS_PATH = "/Volumes/dev/staging/raw_files/orders.csv"

# Staging tables

STG_CUSTOMERS_INITIAL = f"{CATALOG}.{STAGING_SCHEMA}.customers_initial"
STG_CUSTOMERS_UPDATES = f"{CATALOG}.{STAGING_SCHEMA}.customers_updates"
STG_PRODUCTS = f"{CATALOG}.{STAGING_SCHEMA}.products"
STG_ORDERS = f"{CATALOG}.{STAGING_SCHEMA}.orders"

# curated Star Schema

DIM_DATE = f"{CATALOG}.{CURATED_SCHEMA}.dim_date"
DIM_CUSTOMER = f"{CATALOG}.{CURATED_SCHEMA}.dim_customer"
DIM_PRODUCT = f"{CATALOG}.{CURATED_SCHEMA}.dim_product"
FACT_SALES = f"{CATALOG}.{CURATED_SCHEMA}.fact_sales"

# Masked view for PII protection (Part 6)
DIM_CUSTOMER_MASKED = f"{CATALOG}.{CURATED_SCHEMA}.dim_customer_masked"

DATE_RANGE_START = "2024-01-01"
DATE_RANGE_END = "2025-12-31"




