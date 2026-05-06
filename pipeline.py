import pandas as pd
import numpy as np
import os

def build_dataset(orders, products, shipments):
    
    # --- Clean products ---
    products['list_price'] = (
        products['list_price']
        .replace({'\$': '', ',': '.'}, regex=True)
        .replace('N/A', np.nan)
        .astype(float)
    )
    products['category'] = products['category'].str.lower().str.strip()

    # --- Clean orders ---
    orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce', dayfirst=True)
    orders['quantity'] = pd.to_numeric(orders['quantity'], errors='coerce')
    orders = orders[orders['quantity'] > 0]
    orders = orders.dropna(subset=['customer_id'])
    orders = orders.sort_values('order_date').drop_duplicates('order_id', keep='last')

    # --- Clean shipments ---
    shipments['ship_date'] = pd.to_datetime(shipments['ship_date'], errors='coerce')

    ship_agg = shipments.groupby('order_id').agg({
        'shipment_id': 'count',
        'ship_date': 'max'
    }).reset_index()

    # --- Merge ---
    df = orders.merge(products, on='product_id', how='left', validate='many_to_one')
    df = df.merge(ship_agg, on='order_id', how='left', validate='one_to_one')

    # --- Feature ---
    df['revenue'] = df['quantity'] * df['unit_price_paid']

    return df