TABLE_NAME = 'Log'
TIMESTAMP = 'updated_at'
STATUS = 'status'
INDEX_STATUS_KEY = 'Status'
SCHEMA = {
    'TableName': TABLE_NAME,
    'AttributeDefinitions': [
        {
            'AttributeName': TIMESTAMP,
            'AttributeType': 'S'
        },
        {
            'AttributeName': STATUS,
            'AttributeType': 'S'
        }
        ],
    'KeySchema': [
        {
            'AttributeName': TIMESTAMP,
            'KeyType': 'HASH'
        }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
    'GlobalSecondaryIndexes': [{
      'IndexName': INDEX_STATUS_KEY,
      'KeySchema': [
        {
          'AttributeName': STATUS,
          'KeyType': 'HASH'
        }
      ],
      'Projection': {
        'ProjectionType': 'ALL'
      },
      'ProvisionedThroughput': {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
      }
    }],
}
