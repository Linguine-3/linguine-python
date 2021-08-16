"""
Database adapter.
Concerned with selecting the correct database, port, etc.

author: peter mikitsh
"""

from pymongo import MongoClient


class DatabaseAdapter:

    def __init__(self, database):
        self.database = database

    def get_db(self):
        return MongoClient()[self.database]
