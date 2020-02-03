import sys
from abc import abstractmethod

import boto3


class DynamoBase:

    def __init__(self, conf):
        self.conf = conf

        try:
            self.dynamodb = boto3.client('dynamodb', **conf)
        except Exception as err:
            print("{} - {}".format(__name__, err))
            sys.exit(1)

    def create_table(self, table_schema, table_name):
        self.table_name = table_name
        try:
            self.dynamodb.create_table(**table_schema)
        except Exception as err:
            print("{} - already exists - {}".format(table_name, err))
        finally:
            # Wait for the table to exist before exiting
            waiter = self.dynamodb.get_waiter('table_exists')
            waiter.wait(TableName=table_name)

    def get_table(self, table_name):
        dyndb = boto3.resource('dynamodb', **self.conf)
        return dyndb.Table(table_name)

    def list_all(self):
        """
        For TESTING puposes ONLY, should not be used in
        production
        """
        return self.dynamodb.scan(TableName=self.table_name)

    @abstractmethod
    def get_params(self, key):
        pass

    @abstractmethod
    def put_params(self, key, data):
        pass

    @abstractmethod
    def update_params(self, key, data):
        pass

    def get(self, key):
        """
        Get from DynamoDB
        """
        params = self.get_params(key)
        response = self.dynamodb.get_item(**params)
        return response

    def put(self, key, data):
        """
        Write to DynamoDB
        """
        params = self.put_params(key, data)
        self.dynamodb.put_item(**params)

    def update(self, key, data):
        """
        Update to DynamoDB
        """
        params = self.update_params(key, data)
        self.dynamodb.update_item(**params)

    def exists(self, key):
        """
        Returns a boolean depending
        on the existence of the key
        """
        data = self.get(key)
        return True if 'Item' in data else False
