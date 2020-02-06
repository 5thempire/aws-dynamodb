TABLE_NAME = 'Domain'
DOMAIN = 'domain'
URL = 'url'
SCHEMA = {
    'TableName': TABLE_NAME,
    'AttributeDefinitions': [
        {
            'AttributeName': URL,
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': URL,
            'KeyType': 'HASH'
        }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
}
