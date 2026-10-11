" the transformation functions"

from pyspark.sql import DataFrame
from pyspark.sql.functions import year, month, quarter, dayofmonth, col, date_format

def enrich_date_dimenstion(date_df: DataFrame) -> DataFrame:
    """Add date calendar to a dataframe with a single column  'date' """
    return (date_df
            .WithColumn("year", year("date"))
            .WithColumn("quarter", quarter("date"))
            .WithColumn("month", month("date"))
            .WithColumn("day", dayofmonth("date"))
            .WithColumn("date_name", date_format("date", "EEEE"))


def clean_products(df: DataFrame) -> DataFrame:
    """Removes invalid product rows (non-positive price) and dedupes on product_id."""
    return (df
        .dropDuplicates(["product_id"])
        .filter(col("unit_price") > 0))

def build_fact_sales(order_df: DataFrame, dim_customer_current: DataFrame, dim_product: DataFrame) -> DataFrame:
    """
    Joins staged orders to the CURRENT version of each dimension to resolve
    surrogate keys, producing the fact table. Uses inner joins deliberately —
    an order referencing a customer_id/product_id that doesn't exist in the
    dimension is a data quality problem, not something to silently keep with
    a null key.
    """
    return (order_df
            .join(dim_customer_current.select("customer_id", "customer_key"), "customer_id", "inner")
            .join(dim_product.select("product_id", "product_key"), "product_id", "inner")
            .filter("order_id", "customer_key", "product_key", "order_date", "quantity", "amount")
        )
    





