# shipment_error
# Shipment Error Detection & ETL Pipeline

# Project Structure

```bash
shipment_error/
│
├── .github/
│   └── workflows/
│       └── pipeline.yml
│
├── data/
│   ├── orders.csv
│   ├── products.csv
│   └── shipments.csv
│
├── output/
│
├── order.py
├── merge.py
├── pipeline.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

# error log :
update order.py and merge.py --> pipeline.py workflow failed

fix: 

replace this 
``` 
orders = pd.read_csv(
    "data/orders.csv",
     engine="python",
     on_bad_lines="warn"
)

```
with this : 
```
orders = pd.read_csv(
    "data/orders.csv",
    engine="python",
    on_bad_lines="skip"
)
```