#!/usr/bin/env python3
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    name = "Holberton school"
    topics = ['Sys admin', 'AI', 'Algorithm']
    mongo_collection.update_Many(name, topics)
