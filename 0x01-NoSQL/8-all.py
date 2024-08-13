#!/usr/bin/python3
"""List all documents in Python"""


def list_all(mongo_collection):
    """List all documents in Python"""
    return mongo_collection.find()
