import pymongo
import pymongo.errors

from classes import global_constants


class MongoWrapper:

    def __init__(self, dbname=None):
        self.constants = global_constants.GlobalConstants().Mongo()
        try:
            if dbname:
                self.mongo_client = pymongo.MongoClient(
                    self.constants.MONGO_URL, serverSelectionTimeoutMS=self.constants.MONGO_SERVER_TIMEOUT)\
                    .get_database(dbname)
            else:
                self.mongo_client = pymongo.MongoClient(
                    self.constants.MONGO_URL, serverSelectionTimeoutMS=self.constants.MONGO_SERVER_TIMEOUT)\
                    .get_database(self.constants.DB_NAME)
        except pymongo.errors.ConnectionFailure as e:
            print("Connection Failure:\n{}".format(e))
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Timeout:\n{}".format(e))
        except Exception as e:
            print("Exception has occurred:\n{}".format(e))

    def get_db_connection(self):
        return self.mongo_client

    def find(self, collection_name, query, fields_filter=None):
        """
        Find records in Mongo
        :param collection_name: Collection Name
        :param query: Query in JSON
        :param fields_filter: Filter for the output
        :return:
        """
        try:
            return self.mongo_client[collection_name].find(query, fields_filter)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Timeout:\n{}".format(e))
        except Exception as e:
            print("Exception occurred:\n{}".format(e))

    def save_record(self, collection_name, rec):
        """
        Save record to mongo collection
        :param collection_name: Collection Name
        :param rec: Record to save
        :return: Object Id
        """
        try:
            return self.mongo_client.features[collection_name].update(
                {"imageId": "{}".format(rec.imageId)}, {"$set": rec}, upsert=True)
        except Exception as e:
            print("Exception while saving record:\n{}".format(e))

    def bulk_insert(self, collection, records, parallel=False, threads=4):
        """
        Bulk Insert Records in to Mongo
        :param collection: Collection Name
        :param records: Array of Dicts {}, {}
        :param parallel: Boolean for parallel Execution (Future Development)
        :param threads: Number of threads for parallel Execution (Future Development)
        :return:
        """
        try:
            self.mongo_client[collection].insert_many(records)
        except pymongo.errors.BulkWriteError as e:
            print("Bulk Write Error:\n{}".format(e))
        except TypeError as e:
            print("TypeError:\n{}".format(e))
        except Exception as e:
            print("Exception:\n{}".format(e))

