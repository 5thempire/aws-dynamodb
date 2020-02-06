from dynamo.base import DynamoBase
from samples.domain.schema import TABLE_NAME, DOMAIN, URL


class DynamoDomain(DynamoBase):

    def get_params(self, key):
        params = {
            'TableName': TABLE_NAME,
            'Key': {
                URL: {"S": key}
            }
        }
        return params

    def put_params(self, key, data):
        params = {
            'TableName': TABLE_NAME,
            'Item': {
                URL: {"S": key},
            }
        }
        params['Item'].update(data)
        return params

    def remove_params(self, key):
        params = {
            'TableName': TABLE_NAME,
            'Key': {
                URL: {"S": key}
            }
        }
        return params

    def set_value(self, key, value):
        params = {
            DOMAIN: {'S': value}
        }
        self.put(key, params)

    def get_domain(self, key):
        data = self.get(key)
        return data['Item'][URL]['S']
