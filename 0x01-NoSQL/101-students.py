#!/usr/bin/env python3
""" Top students"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """ Top students"""
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
