from datetime import datetime

from dyn_base import DynamoGeneralClass
from schema import (COMPLEX_SCHEMA, COMPLEX_SCHEMA_INDEX_TWO, COMPLEX_SCHEMA_KEY_ONE, COMPLEX_SCHEMA_KEY_THREE,
                    COMPLEX_SCHEMA_KEY_TWO, COMPLEX_SCHEMA_TABLE_NAME)

GREEN = 'green'
RED = 'red'


class ComplexTableClass(DynamoGeneralClass):

    def get_params(self, key):
        params = {
            'TableName': COMPLEX_SCHEMA_TABLE_NAME,
            'Key': {
                COMPLEX_SCHEMA_KEY_ONE: {"S": key}
            }
        }
        return params

    def put_params(self, key, data):
        params = {
            'TableName': COMPLEX_SCHEMA_TABLE_NAME,
            'Item': {
                COMPLEX_SCHEMA_KEY_ONE: {"S": key},
            }
        }
        params['Item'].update(data)
        return params

    def update_params(self, key, value, timestamp):
        params = {
            'ExpressionAttributeNames': {
                '#LU': COMPLEX_SCHEMA_KEY_THREE,
                '#S': COMPLEX_SCHEMA_KEY_TWO
            },
            'ExpressionAttributeValues': {
                ':lu': {
                    'S': timestamp
                },
                ':s': {
                    'S': value
                }
            },
            'Key': {
                COMPLEX_SCHEMA_KEY_ONE: {"S": key}
            },
            'ReturnValues': 'UPDATED_NEW',
            'TableName': COMPLEX_SCHEMA_TABLE_NAME,
            'UpdateExpression': 'SET #LU = :lu, #S = :s'
        }
        return params

    def filter_by_key_one(self, key, status):
        """
        Filters all entries by key one and key two
        """
        response = self.dynamodb.query(TableName=COMPLEX_SCHEMA_TABLE_NAME,
                                       KeyConditionExpression="{} = :key".format(COMPLEX_SCHEMA_KEY_ONE),
                                       FilterExpression="#S = :status",
                                       ExpressionAttributeValues={":status": {"S": status},
                                                                  ":key": {"S": key}},
                                       ExpressionAttributeNames={"#S": COMPLEX_SCHEMA_KEY_TWO})
        return response

    def filter_by_key_two(self, status):
        """
        Filters all entries by key two
        """
        response = self.dynamodb.query(TableName=COMPLEX_SCHEMA_TABLE_NAME,
                                       IndexName=COMPLEX_SCHEMA_INDEX_TWO,
                                       KeyConditionExpression="#S = :status",
                                       ExpressionAttributeValues={":status": {"S": status}},
                                       ExpressionAttributeNames={"#S": COMPLEX_SCHEMA_KEY_TWO})
        return response

    def update(self, key, status):
        """
        Update to DynamoDB
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M')
        params = self.update_params(key, status, timestamp)

        self.dynamodb.update_item(**params)
