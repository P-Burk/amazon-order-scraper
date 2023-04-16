import os
import pprint
import typing

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())

MONGO_USERNAME = os.getenv("MONGODB_USERNAME")
MONGO_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGO_CONNECTION_STRING = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}" \
                          f"@scraper0.cipyr9d.mongodb.net/?retryWrites=true&w=majority"

class DBHandler:
    def __init__(self):
        self.__connect()
        self.db = self.client["amazon_scraper"]

    # attempts to connect to the MongoDB database
    def __connect(self):
        try:
            self.client = MongoClient(MONGO_CONNECTION_STRING)
        except Exception as error_msg:
            print(error_msg)
            print("Failed to connect to MongoDB instance.")

    # close the connection when done
    def __disconnect(self):
        self.client.close()

    def __find_document(self, query: dict) -> None | object:
        """
        Private method to check collection for documents and return cursor object if documents are found
        :param query: Dict
        :return: None or pymongo cursor
        """
        document_count = self.db.orders.count_documents(query)
        if document_count == 0:
            return None
        return self.db.orders.find(query)

    def read_all(self, query):
        output = self.__find_document(query)
        if output is None:
            print("No matching document(s) found.")
            return None
        return output

    def insert_order(self, query: dict):
        """
        Inserts a single document into the orders collection.
        :param query: dictionary of content to add to the database.
        """
        try:
            self.db.orders.insert_one(query)
        except Exception as error:
            print(error)
            print("Failed to add order to database.")
