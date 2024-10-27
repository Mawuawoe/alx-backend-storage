#!/usr/bin/env python3
'''
a Python script that
provides some stats about Nginx logs stored in MongoDB:
'''
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient()
db = client.logs
collection = db.nginx

# Total number of logs
total_logs = collection.count_documents({})
print(f"{total_logs} logs")

# Count methods
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
print("Methods:")
for method in methods:
    count = collection.count_documents({"method": method})
    print(f"\tmethod {method}: {count}")

# Count status check for GET requests with path "/status"
status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
print(f"{status_check_count} status check")
