import os

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient, ReturnDocument

load_dotenv(find_dotenv())

MONGO_USERNAME = os.getenv("MONGODB_USERNAME")
MONGO_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGO_CONNECTION_STRING = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}" \
                          f"@scraper0.cipyr9d.mongodb.net/?retryWrites=true&w=majority"

class DBHandler:
    def __init__(self):
        self.__connect()
        self.db = self.client["amazon_scraper"]

    def __enter__(self):
        self.__connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__disconnect()
        if exc_type:
            raise exc_type(exc_val)
        return self

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

    def read_all(self, query: dict) -> None | object:
        """
        Returns a cursor containing documents that meet the search query criteria.
        :param query: Dictionary containing the search criteria.
        :return: None if no documents are found, otherwise a cursor object.
        """
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

    def update_orders(self, query: dict, update_data: dict, multiple_orders: bool) -> None | object:
        """
        Updates one or many orders.
        :param query: documents to find.
        :param update_data: data that will be updated to the order(s).
        :param multiple_orders: selector for updating a single order or multiple orders.
        :return: No document(s) found - None.
                 Single update - the updated document.
                 Multiple updates - pymongo.returnResult.
        """
        if query is None:
            raise Exception("No data provided for query.")
        if update_data is None:
            raise Exception("No data provided for update.")

        update_data = {"$set": update_data}

        # logic for updating a single order
        if multiple_orders is False:
            return self.db.orders.find_one_and_update(query, update_data, return_document=ReturnDocument.AFTER)

        # logic for updating multiple orders
        result = self.db.orders.update_many(query, update_data)
        if result.modified_count == 0:
            return None
        return result

    def delete(self, query: dict, multiple_orders: bool) -> None | object:
        """
        Deletes one or many orders.
        :param query: documents to find.
        :param multiple_orders: selector for deleting a single order or multiple orders.
        :return: No document(s) found - None.
                 Document(s) deleted - pymongo.deleteResult.
        """
        if query is None:
            raise Exception("No data provided for query.")

        if multiple_orders is False:    # logic for deleting a single order
            result = self.db.orders.delete_one(query)
        else:                           # logic for deleting multiple orders
            result = self.db.orders.delete_many(query)

        if result.deleted_count == 0:
            return None
        return result
