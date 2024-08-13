#!/usr/bin/python3
"""Insert a document in Python"""
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """Insert a document in Python"""
    result = mongo_collection.insert_one(kwargs)
    return str(result.inserted_id)
