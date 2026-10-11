"""this section describe the test of the transformation function"""
import pytest
from pyspark.sql import SparkSession
from analytics_pipeline.transforms import enrich_date_dimenstion, clean_products, build_fact_sales

@pytest.fixture(scope= "module")
def spark():
    return SparkSession.builder.appName("test").getOrCreate()


def test_enrich_date_dimension_adds_calendar_columns(spark):
    df = spark.sql("SELECT to_date(2025-03-15) as date")
    results = enrich_date_dimenstion(df)
    row results.collect()[0]
    assert row["year"] == 2025
    assert row["quarter"] ==  1
    assert row["month"] == 3
    assert row["day"] == 15
    assert row ["day_name"] == "Saturday"

def test_clean_products_drop_non_positive_proices(spark):
    df = spark.CreateDataFrame([
        (1, "Widget", "Tools", 9.99),
        (2, "Broken", "Tools", -5.00),
        (3, "Free Sample", "Tools", 0.0),
    ], ["product_id", "product_name", "category", "unit_price"])

    results = clean_products(df)
    assert results.count() == 1

def test_clean_products_drops_duplicate_product_id(saprk):
    df = spark.CreateDataFrame([
        (1, "Widget", "Tools", 9.99),
        (1, "Widget", "Tools", 9.99),
    ], ["product_id", "product_name", "category", "unit_price"])
    results = clean_products(df)
    assert results.count() == 1

def test_build_facttest_build_fact_sales_resolves_surrogate_keys(spark):
    orders = spark.createDataFrame([
        (1, 100, 200, "2025-01-01", 2, 19.98),
    ], ["order_id", "customer_id", "product_id", "order_date", "quantity", "amount"])

    dim_customer = spark.createDataFrame([
        (100, 1, "Jane Doe"),
    ], ["customer_id", "customer_key", "name"])

    dim_product = spark.createDataFrame([
        (200, 1, "Widget"),
    ], ["product_id", "product_key", "product_name"])

    result = build_fact_sales(orders, dim_customer, dim_product)
    assert result.count() == 1
    row = result.collect()[0]
    assert row["customer_key"] == 1
    assert row["product_key"] == 1

def test_build_fact_sales_drops_orders_with_unknown_customer(spark):
    orders = spark.createDataFrame([
        (1, 999, 200, "2025-01-01", 2, 19.98),  # customer_id 999 doesn't exist in dim
    ], ["order_id", "customer_id", "product_id", "order_date", "quantity", "amount"])

    dim_customer = spark.createDataFrame([
        (100, 1, "Jane Doe"),
    ], ["customer_id", "customer_key", "name"])

    dim_product = spark.createDataFrame([
        (200, 1, "Widget"),
    ], ["product_id", "product_key", "product_name"])

    result = build_fact_sales(orders, dim_customer, dim_product)
    assert result.count() == 0

