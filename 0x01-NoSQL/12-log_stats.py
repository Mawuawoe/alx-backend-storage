#!/usr/bin/env python3
'''
a Python script that
provides some stats about Nginx logs stored in MongoDB:
'''
from pymongo import MongoClient

def print_nginx_request_logs(nginx_collection):
    '''
    Prints stats about Nginx request logs.
    '''
    print(f"{nginx_collection.count_documents({})} logs")
    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print(f"\tmethod {method}: {req_count}")
    
    status_checks_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_checks_count} status check")

def run():
    '''
    Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)

if __name__ == '__main__':
    run()
