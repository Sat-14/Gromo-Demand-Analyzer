# sample_data_generator.py

import random
from datetime import datetime, timedelta
from faker import Faker
from pymongo import MongoClient

# Initialize Faker and MongoDB
fake = Faker()
client = MongoClient("mongodb://localhost:27017/")
db = client["gromo"]
collection = db["sales_data"]

# Product types and channels
product_types = ["loan", "credit_card", "insurance"]
channels = ["online", "offline"]

def random_date():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date=fake.date_between(start_date=start_date, end_date=end_date)
    # Ensure the date is not a weekend
    return datetime.combine(random_date,datetime.min.time())

def generate_record():
    return {
        "date": random_date(),
        "pincode": fake.postcode(),
        "city": fake.city(),
        "product": random.choice(product_types),
        "channel": random.choice(channels),
        "agent_id": fake.uuid4(),
        "customer_age": random.randint(21, 60),
        "customer_income": random.randint(20000, 100000)
    }

def insert_sample_data(n=1000):
    records = [generate_record() for _ in range(n)]
    collection.delete_many({})  # Optional: clear old data
    result = collection.insert_many(records)
    print(f"Inserted {len(result.inserted_ids)} records into MongoDB.")

if __name__ == "__main__":
    insert_sample_data(1000)
