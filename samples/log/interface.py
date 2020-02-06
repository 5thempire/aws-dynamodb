from dynamo.base import DynamoBase
from samples.log.schema import TABLE_NAME, TIMESTAMP, STATUS, INDEX_STATUS_KEY


class DynamoLog(DynamoBase):

    def get_params(self, key):
        params = {
            'TableName': TABLE_NAME,
            'Key': {
                TIMESTAMP: {"S": key}
            }
        }
        return params

    def put_params(self, key, data):
        params = {
            'TableName': TABLE_NAME,
            'Item': {
                TIMESTAMP: {"S": key},
            }
        }
        params['Item'].update(data)
        return params

    def update_params(self, timestamp, value):
        params = {
            'ExpressionAttributeNames': {
                '#LU': INDEX_STATUS_KEY,
                '#S': STATUS
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
                TIMESTAMP: {"S": timestamp}
            },
            'ReturnValues': 'UPDATED_NEW',
            'TableName': TABLE_NAME,
            'UpdateExpression': 'SET #LU = :lu, #S = :s'
        }
        return params

    def filter_by_timestamp_status(self, timestamp, status):
        """
        Filters all entries by timestamp and status
        """
        response = self.dynamodb.query(TableName=TABLE_NAME,
                                       KeyConditionExpression=f"{TIMESTAMP} = :updated_at",
                                       FilterExpression="#S = :status",
                                       ExpressionAttributeValues={":status": {"S": status},
                                                                  ":updated_at": {"S": timestamp}},
                                       ExpressionAttributeNames={"#S": STATUS})
        return response

    def filter_by_status(self, status):
        """
        Filters all entries by key two
        """
        response = self.dynamodb.query(TableName=TABLE_NAME,
                                       IndexName=INDEX_STATUS_KEY,
                                       KeyConditionExpression="#S = :status",
                                       ExpressionAttributeValues={":status": {"S": status}},
                                       ExpressionAttributeNames={"#S": STATUS})
        return response

    def update(self, timestamp, status):
        """
        Update to DynamoDB
        """
        params = self.update_params(timestamp, status)

        self.dynamodb.update_item(**params)
