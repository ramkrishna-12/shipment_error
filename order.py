# version 3 : latest version with better date parsing and price cleaning


import pandas as pd
import numpy as np
import os

os.makedirs("output", exist_ok=True)

# -----------------------------
# Load Orders Dataset
# -----------------------------

orders = pd.read_csv(
    "data/orders.csv",
    engine="python",
    on_bad_lines="skip"
)
# -----------------------------
# Mixed Date Parser
# -----------------------------

def parse_mixed_dates(x):
    try:
        if str(x).isdigit():
            return pd.to_datetime("1899-12-30") + pd.to_timedelta(int(x), unit="D")

        return pd.to_datetime(
            x,
            errors="coerce",
            dayfirst=True
        )

    except:
        return pd.NaT

# -----------------------------
# Data Cleaning
# -----------------------------

orders["order_date"] = orders["order_date"].apply(parse_mixed_dates)

orders["quantity"] = pd.to_numeric(
    orders["quantity"],
    errors="coerce"
)

# Clean pricing column
orders["unit_price_paid"] = (
    orders["unit_price_paid"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", ".", regex=False)
)

orders["unit_price_paid"] = pd.to_numeric(
    orders["unit_price_paid"],
    errors="coerce"
)

# Remove invalid rows
orders = orders[orders["quantity"] > 0]

orders = orders.dropna(
    subset=["customer_id"]
)

# Remove duplicates
orders = (
    orders
    .sort_values(by="order_date")
    .drop_duplicates(
        subset="order_id",
        keep="last"
    )
)

# -----------------------------
# Save Cleaned Data
# -----------------------------

orders.to_csv(
    "output/clean_orders.csv",
    index=False
)

print("Orders cleaned successfully")




## 

# verasion 2 : 

# import pandas as pd
# import numpy as np
# import os

# os.makedirs("output", exist_ok=True)

# orders = pd.read_csv(
#     "data/orders.csv",
#     engine="python",
#     on_bad_lines="warn"
# )

# def parse_mixed_dates(x):
#     try:
#         if str(x).isdigit():
#             return pd.to_datetime("1899-12-30") + pd.to_timedelta(int(x), unit="D")
#         return pd.to_datetime(x, errors="coerce", dayfirst=True)
#     except:
#         return pd.NaT

# orders["order_date"] = orders["order_date"].apply(parse_mixed_dates)

# orders["quantity"] = pd.to_numeric(
#     orders["quantity"],
#     errors="coerce"
# )

# orders = orders[orders["quantity"] > 0]

# orders = orders.dropna(subset=["customer_id"])

# orders = (
#     orders.sort_values(by="order_date")
#           .drop_duplicates(subset="order_id", keep="last")
# )

# orders.to_csv("output/clean_orders.csv", index=False)

# print("Orders cleaned successfully")





##
# version 1 

# import pandas as pd
# import numpy as np
# import os

# # Create output folder
# os.makedirs("output", exist_ok=True)

# # Load CSV
# orders = pd.read_csv("orders.csv")

# # Convert date column
# orders["order_date"] = pd.to_datetime(
#     orders["order_date"],
#     errors="coerce",
#     dayfirst=True
# )

# # Convert quantity
# orders["quantity"] = pd.to_numeric(
#     orders["quantity"],
#     errors="coerce"
# )

# # Remove invalid quantities
# orders = orders[orders["quantity"] > 0]

# # Remove missing customer_id
# orders = orders.dropna(subset=["customer_id"])

# # Remove duplicate orders
# orders = (
#     orders.sort_values(by="order_date")
#           .drop_duplicates(subset="order_id", keep="last")
# )

# # Save cleaned file
# orders.to_csv("output/clean_orders.csv", index=False)

# print("Orders cleaned successfully")



# #
# # duplicate order id  error
# orders = orders.sort_values(by="order_date")
# orders = orders.drop_duplicates(subset="order_id", keep="last")
# # Why it’s dangerous:
# # Inflates revenue → classic “oops CFO is yelling” scenario.

# # Fix:

# # Treat as re-export duplicates
# # Keep latest or most complete row


# # Issue 2: Mixed / Dirty Numeric Fields (price, quantity)
# # $49.99, 49,99, N/A
# # Negative quantities

# # Fix:

# products['list_price'] = (
#     products['list_price']
#     .replace({'\$': '', ',': '.'}, regex=True)
#     .replace('N/A', np.nan)
#     .astype(float)
# )

# orders['quantity'] = pd.to_numeric(orders['quantity'], errors='coerce')

# # Handle negatives (assume returns → exclude or flag)
# orders = orders[orders['quantity'] > 0]



# # Issue 3: Inconsistent Dates

# # Multiple formats + Excel serials (because Excel refuses to die)

# # Fix:

# orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce', dayfirst=True)
# shipments['ship_date'] = pd.to_datetime(shipments['ship_date'], errors='coerce')