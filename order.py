#
# duplicate order id  error
orders = orders.sort_values(by="order_date")
orders = orders.drop_duplicates(subset="order_id", keep="last")
# Why it’s dangerous:
# Inflates revenue → classic “oops CFO is yelling” scenario.

# Fix:

# Treat as re-export duplicates
# Keep latest or most complete row


# Issue 2: Mixed / Dirty Numeric Fields (price, quantity)
# $49.99, 49,99, N/A
# Negative quantities

# Fix:

products['list_price'] = (
    products['list_price']
    .replace({'\$': '', ',': '.'}, regex=True)
    .replace('N/A', np.nan)
    .astype(float)
)

orders['quantity'] = pd.to_numeric(orders['quantity'], errors='coerce')

# Handle negatives (assume returns → exclude or flag)
orders = orders[orders['quantity'] > 0]



# Issue 3: Inconsistent Dates

# Multiple formats + Excel serials (because Excel refuses to die)

# Fix:

orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce', dayfirst=True)
shipments['ship_date'] = pd.to_datetime(shipments['ship_date'], errors='coerce')