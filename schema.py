SIMPLE_SCHEMA_TABLE_NAME = 'SimpleSchemaTableName'
SIMPLE_SCHEMA_KEY = 'IndexKey'
SIMPLE_SCHEMA_VALUE = 'Value'
SIMPLE_SCHEMA = {
    'TableName': SIMPLE_SCHEMA_TABLE_NAME,
    'AttributeDefinitions': [
        {
            'AttributeName': SIMPLE_SCHEMA_KEY,
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': SIMPLE_SCHEMA_KEY,
            'KeyType': 'HASH'
        }
    ],
    'ProvisionedThroughput':{
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
}

COMPLEX_SCHEMA_TABLE_NAME = 'ComplexSchemaTableName'
COMPLEX_SCHEMA_KEY_ONE = 'AttributeOneKey'
COMPLEX_SCHEMA_KEY_TWO = 'AttributeTwoKey'
COMPLEX_SCHEMA_KEY_THREE = 'AttributeThreeKey'
COMPLEX_SCHEMA_INDEX_TWO = 'AttributeTwoIndexName'
COMPLEX_SCHEMA = {
    'TableName': COMPLEX_SCHEMA_TABLE_NAME,
    'AttributeDefinitions': [
        {
            'AttributeName': COMPLEX_SCHEMA_KEY_ONE,
            'AttributeType': 'S'
        },
        {
            'AttributeName': COMPLEX_SCHEMA_KEY_TWO,
            'AttributeType': 'S'
        }
        ],
    'KeySchema': [
        {
            'AttributeName': COMPLEX_SCHEMA_KEY_ONE,
            'KeyType': 'HASH'
        }
    ],
    'ProvisionedThroughput':{
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
    'GlobalSecondaryIndexes' : [{
      'IndexName' : COMPLEX_SCHEMA_INDEX_TWO,
      'KeySchema' : [
        {
          'AttributeName' : COMPLEX_SCHEMA_KEY_TWO,
          'KeyType' : 'HASH'
        }
      ],
      'Projection' : {
        'ProjectionType' : 'ALL'
      },
      'ProvisionedThroughput' : {
        'ReadCapacityUnits' : 10,
        'WriteCapacityUnits' : 10
      }
    }],
}