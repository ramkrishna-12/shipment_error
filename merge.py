# Cleaning & Standardization Strategy
# Key transformations:
# Normalize category:
products['category'] = products['category'].str.lower().str.strip()



# Missing customer_id (~1.8%)
# Drop or flag (depends on business)
orders = orders.dropna(subset=['customer_id'])


# Ensure keys are clean:
assert orders['order_id'].notnull().all()
assert products['product_id'].is_unique




# Merge Logic (THIS is where most people fail)
# Relationships:

#  `orders.product_id → products.product_id (many-to-one)`
#  'orders.order_id → shipments.order_id (one-to-many)`


# Aggregate shipments FIRST


ship_agg = shipments.groupby('order_id').agg({
    'shipment_id': 'count',
    'ship_date': 'max',
    'status': 'last'
}).rename(columns={'shipment_id': 'shipment_count'}).reset_index()


# Merge 
df = orders.merge(products, on='product_id', how='left', validate='many_to_one')

df = df.merge(ship_agg, on='order_id', how='left', validate='one_to_one')