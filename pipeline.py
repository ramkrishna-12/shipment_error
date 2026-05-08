# versin 2: latest
# pulling all the code together in a single pipeline file to run the entire process in one go. This is a common pattern for simple ETL pipelines, but as complexity grows, it’s often better to modularize into separate scripts (like order.py and merge.py) for maintainability and clarity.

import subprocess

print("Running order cleaning...")
subprocess.run(
    ["python", "order.py"],
    check=True
)

print("Running merge pipeline...")
subprocess.run(
    ["python", "merge.py"],
    check=True
)

print("ETL Pipeline completed successfully")

## ------------------------------------------------------------------------------------------------------------##
# pipeline define but singular pipeline for merging datasets and feature engineering

# version 1 


# import pandas as pd
# import numpy as np
# import os

# def build_dataset(orders, products, shipments):
    
#     # --- Clean products ---
#     products['list_price'] = (
#         products['list_price']
#         .replace({'\$': '', ',': '.'}, regex=True)
#         .replace('N/A', np.nan)
#         .astype(float)
#     )
#     products['category'] = products['category'].str.lower().str.strip()

#     # --- Clean orders ---
#     orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce', dayfirst=True)
#     orders['quantity'] = pd.to_numeric(orders['quantity'], errors='coerce')
#     orders = orders[orders['quantity'] > 0]
#     orders = orders.dropna(subset=['customer_id'])
#     orders = orders.sort_values('order_date').drop_duplicates('order_id', keep='last')

#     # --- Clean shipments ---
#     shipments['ship_date'] = pd.to_datetime(shipments['ship_date'], errors='coerce')

#     ship_agg = shipments.groupby('order_id').agg({
#         'shipment_id': 'count',
#         'ship_date': 'max'
#     }).reset_index()

#     # --- Merge ---
#     df = orders.merge(products, on='product_id', how='left', validate='many_to_one')
#     df = df.merge(ship_agg, on='order_id', how='left', validate='one_to_one')

#     # --- Feature ---
#     df['revenue'] = df['quantity'] * df['unit_price_paid']

#     return df