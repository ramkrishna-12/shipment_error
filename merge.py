# version 3 : latest version 

import pandas as pd
import os

os.makedirs("output", exist_ok=True)

# -----------------------------
# Load Datasets
# -----------------------------

orders = pd.read_csv(
    "output/clean_orders.csv"
)

products = pd.read_csv(
    "data/products.csv"
)

shipments = pd.read_csv(
    "data/shipments.csv"
)

# -----------------------------
# Clean Products
# -----------------------------

products["category"] = (
    products["category"]
    .astype(str)
    .str.lower()
    .str.strip()
)

products["list_price"] = (
    products["list_price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", ".", regex=False)
)

products["list_price"] = pd.to_numeric(
    products["list_price"],
    errors="coerce"
)

# -----------------------------
# Clean Shipments
# -----------------------------

shipments["ship_date"] = pd.to_datetime(
    shipments["ship_date"],
    errors="coerce"
)

# -----------------------------
# Aggregate Shipments
# -----------------------------

ship_agg = (
    shipments.groupby("order_id")
    .agg({
        "shipment_id": "count",
        "ship_date": "max",
        "status": "last"
    })
    .rename(columns={
        "shipment_id": "shipment_count"
    })
    .reset_index()
)

# -----------------------------
# Merge Datasets
# -----------------------------

df = orders.merge(
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
)

df = df.merge(
    ship_agg,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# -----------------------------
# Feature Engineering
# -----------------------------

df["revenue"] = (
    df["quantity"] *
    df["unit_price_paid"]
)

# -----------------------------
# Save Final Dataset
# -----------------------------

df.to_csv(
    "output/final_dataset.csv",
    index=False
)

print("Merge pipeline completed successfully")

# version 2: 


# import pandas as pd
# import os

# os.makedirs("output", exist_ok=True)

# # Load datasets
# orders = pd.read_csv("output/clean_orders.csv")

# products = pd.read_csv("data/products.csv")

# shipments = pd.read_csv("data/shipments.csv")

# # -----------------------------
# # Cleaning & Standardization
# # -----------------------------

# # Normalize category
# products["category"] = (
#     products["category"]
#     .astype(str)
#     .str.lower()
#     .str.strip()
# )

# # Remove missing customer_id
# orders = orders.dropna(subset=["customer_id"])

# # Ensure keys are valid
# assert orders["order_id"].notnull().all()
# assert products["product_id"].is_unique

# # -----------------------------
# # Clean shipments
# # -----------------------------

# shipments["ship_date"] = pd.to_datetime(
#     shipments["ship_date"],
#     errors="coerce"
# )

# # Aggregate shipments FIRST
# ship_agg = (
#     shipments.groupby("order_id")
#     .agg({
#         "shipment_id": "count",
#         "ship_date": "max",
#         "status": "last"
#     })
#     .rename(columns={"shipment_id": "shipment_count"})
#     .reset_index()
# )

# # -----------------------------
# # Merge datasets
# # -----------------------------

# df = orders.merge(
#     products,
#     on="product_id",
#     how="left",
#     validate="many_to_one"
# )

# df = df.merge(
#     ship_agg,
#     on="order_id",
#     how="left",
#     validate="one_to_one"
# )

# # -----------------------------
# # Revenue Calculation
# # -----------------------------

# df["unit_price_paid"] = (
#     df["unit_price_paid"]
#     .astype(str)
#     .str.replace("$", "", regex=False)
#     .str.replace(",", ".", regex=False)
# )

# df["unit_price_paid"] = pd.to_numeric(
#     df["unit_price_paid"],
#     errors="coerce"
# )

# df["revenue"] = (
#     df["quantity"] * df["unit_price_paid"]
# )

# # Save final merged dataset
# df.to_csv("output/final_dataset.csv", index=False)

# print("Merge pipeline completed successfully")

## 

# version 1 : basic merge without cleaning

# # Cleaning & Standardization Strategy
# # Key transformations:
# # Normalize category:
# products['category'] = products['category'].str.lower().str.strip()



# # Missing customer_id (~1.8%)
# # Drop or flag (depends on business)
# orders = orders.dropna(subset=['customer_id'])


# # Ensure keys are clean:
# assert orders['order_id'].notnull().all()
# assert products['product_id'].is_unique




# # Merge Logic (THIS is where most people fail)
# # Relationships:

# #  `orders.product_id → products.product_id (many-to-one)`
# #  'orders.order_id → shipments.order_id (one-to-many)`


# # Aggregate shipments FIRST


# ship_agg = shipments.groupby('order_id').agg({
#     'shipment_id': 'count',
#     'ship_date': 'max',
#     'status': 'last'
# }).rename(columns={'shipment_id': 'shipment_count'}).reset_index()


# # Merge 
# df = orders.merge(products, on='product_id', how='left', validate='many_to_one')

# df = df.merge(ship_agg, on='order_id', how='left', validate='one_to_one')