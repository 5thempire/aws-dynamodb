from dyn_base import DynamoGeneralClass
from schema import SIMPLE_SCHEMA,SIMPLE_SCHEMA_TABLE_NAME, SIMPLE_SCHEMA_KEY, SIMPLE_SCHEMA_VALUE


class SimpleTableClass(DynamoGeneralClass):

    def get_params(self, key):
        params = {
            'TableName': SIMPLE_SCHEMA_TABLE_NAME,
            'Key': {
                SIMPLE_SCHEMA_KEY: {"S": key}
            }
        }
        return params

    def put_params(self, key, data):
        params = {
            'TableName': SIMPLE_SCHEMA_TABLE_NAME,
            'Item': {
                SIMPLE_SCHEMA_KEY: {"S": key},
            }
        }
        params['Item'].update(data)
        return params

    def set_value(self, key, value):
        params = {
            SIMPLE_SCHEMA_VALUE: {'S': value}
        }
        self.put(key, params)
