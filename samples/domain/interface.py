from dynamo.base import DynamoBase
from samples.domain.schema import TABLE_NAME, DOMAIN, URL


class DynamoDomain(DynamoBase):

    def get_params(self, key):
        params = {
            'TableName': TABLE_NAME,
            'Key': {
                DOMAIN: {"S": key}
            }
        }
        return params

    def put_params(self, key, data):
        params = {
            'TableName': TABLE_NAME,
            'Item': {
                DOMAIN: {"S": key},
            }
        }
        params['Item'].update(data)
        return params

    def set_value(self, key, value):
        params = {
            URL: {'S': value}
        }
        self.put(key, params)

    def get_url(self, key):
        data = self.get(key)
        return data['Item'][URL]['S']
