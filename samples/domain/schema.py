TABLE_NAME = 'SimpleSchemaTableName'
DOMAIN = 'domain'
URL = 'url'
SCHEMA = {
    'TableName': TABLE_NAME,
    'AttributeDefinitions': [
        {
            'AttributeName': DOMAIN,
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': DOMAIN,
            'KeyType': 'HASH'
        }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
}
