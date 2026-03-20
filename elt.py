import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
df = pd.read_csv('data/restaurant_orders.csv')

#data cleaning
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df['Order Time'] = pd.to_datetime(df['Order Time'])


engine = create_engine(
    "postgresql+psycopg2://postgres:12345@localhost:5432/order"
)


#customer insert
customers = df[['Customer Name']].drop_duplicates()
customers.columns = ['customer_name']

existing_customers = pd.read_sql("SELECT customer_name FROM customers", engine)
new_customers = customers[~customers['customer_name'].isin(existing_customers['customer_name'])]

if not new_customers.empty:
    new_customers.to_sql('customers', engine, if_exists='append', index=False)
    print(f"{len(new_customers)} new customers")
else:
    print("No new customers")

#product insert
products = df[['Food Item', 'Category', 'Price']].drop_duplicates()
products.columns = ['food_item', 'category', 'price']

existing_products = pd.read_sql("SELECT food_item FROM products", engine)
new_products = products[~products['food_item'].isin(existing_products['food_item'])]

if not new_products.empty:
    new_products.to_sql('products', engine, if_exists='append', index=False)
    print(f"{len(new_products)} new products")
else:
    print("No new products")

#order insert
orders = df[['Order ID', 'Customer Name', 'Order Time', 'Payment Method']].drop_duplicates(subset=['Order ID'])
orders.columns = ['order_id', 'customer_name', 'order_time', 'payment_method']

#customer id maping
customer_map = pd.read_sql("SELECT * FROM customers", engine)
orders = orders.merge(customer_map, on='customer_name')
orders = orders[['order_id', 'customer_id', 'order_time', 'payment_method']]

existing_orders = pd.read_sql("SELECT order_id FROM orders", engine)
new_orders = orders[~orders['order_id'].isin(existing_orders['order_id'])]

if not new_orders.empty:
    new_orders.to_sql('orders', engine, if_exists='append', index=False)
    print(f"{len(new_orders)} new orders")
else:
    print("No new orders")

#order details
products_map = pd.read_sql("SELECT * FROM products", engine)
order_details = df.merge(products_map, left_on='Food Item', right_on='food_item')
order_details = order_details[['Order ID', 'product_id', 'Quantity']]
order_details.columns = ['order_id', 'product_id', 'quantity']
existing_order_details = pd.read_sql("SELECT order_id, product_id FROM order_details", engine)

#new order details
new_order_details = order_details.merge(existing_order_details, on=['order_id', 'product_id'], how='left', indicator=True)
new_order_details = new_order_details[new_order_details['_merge'] == 'left_only'].drop(columns=['_merge'])

if not new_order_details.empty:
    new_order_details.to_sql('order_details', engine, if_exists='append', index=False)
    print(f"{len(new_order_details)} new order details")
else:
    print("No new order details")

#mongodb
client = MongoClient("mongodb://localhost:27017/")
db = client["order"]
collection = db["orders_raw"]

existing_count = collection.count_documents({})
if existing_count == 0:
    collection.insert_many(df.to_dict(orient="records"))
    print("Data inserted in mongodb")
else:
    print("Data already exists")

#print("output")