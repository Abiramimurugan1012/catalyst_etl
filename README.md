# Restaurant Orders ETL Pipeline

# Project Overview

This project demonstrates an **End-to-End ETL (Extract, Transform, Load) Pipeline** built using Python.

The pipeline extracts data from a CSV file, transforms it into structured format, and loads it into:

* PostgreSQL (Relational Database)
* MongoDB (NoSQL Database)

---

## Tools & Technologies Used

* Visual Studio Code
* Python
* SQL
* PostgreSQL
* MongoDB
* Pandas

---

##  ETL Process

### Extract

* Data is extracted from a CSV file:

```
restaurant_orders.csv in data file
```

---

### Transform

* Removed null values
* Removed duplicate records
* Converted order time to datetime format
* Structured data into multiple tables

---

### Load

#### PostgreSQL Tables

* customers
* products
* orders
* order_details

####  MongoDB

* Database: `order`
* Collection: `orders_raw`

---

## Database Schema

### Customers

* customer_id (Primary Key)
* customer_name

### Products

* product_id (Primary Key)
* food_item
* category
* price

### Orders

* order_id (Primary Key)
* customer_id (Foreign Key)
* order_time
* payment_method

### Order Details

* id (Primary Key)
* order_id (Foreign Key)
* product_id (Foreign Key)
* quantity

---

## ⚙️ Setup Instructions

### Step 1: Install Libraries

```bash
pip install pandas sqlalchemy psycopg2 pymongo
```

---

### Step 2: Setup PostgreSQL

```sql
CREATE DATABASE order;
```

---

### Step 3: Setup MongoDB

* Run MongoDB server
* Open MongoDB Compass
* Connect to:

```
mongodb://localhost:27017/
```

---

### Step 4: Project Structure

```
etl.py
restaurant_orders.csv
```

---

### Step 5: Clear Old Data

```sql
DELETE FROM order_details;
DELETE FROM orders;
DELETE FROM customers;
DELETE FROM products;
```

---

### Step 6: Run Project

```bash
python etl.py
```

---

## Output

* Data loaded into PostgreSQL tables
* Data stored in MongoDB collection


## Key Features

* End-to-End ETL Pipeline
* Data Cleaning and Transformation
* Relational Database Design
* NoSQL Data Storage
* Handles duplicate records
* Maintains data integrity

---

## Future Enhancements

* Implement UPSERT (ON CONFLICT)
* Add logging and error handling
* Automate using scheduling tools
* Build dashboard for visualization

---

##  Conclusion

This project demonstrates how to build a complete ETL pipeline using Python, SQL, PostgreSQL, and MongoDB for efficient data processing and storage.

---

## Author

Abirami M
