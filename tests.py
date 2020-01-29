import unittest
from datetime import datetime
from uuid import uuid4

from botocore.exceptions import ClientError, EndpointConnectionError

from dyn_complex import ComplexTableClass, GREEN, RED
from dyn_simple import SimpleTableClass
from schema import (SIMPLE_SCHEMA, SIMPLE_SCHEMA_TABLE_NAME, SIMPLE_SCHEMA_VALUE, SIMPLE_SCHEMA_KEY, COMPLEX_SCHEMA,
                    COMPLEX_SCHEMA_TABLE_NAME, COMPLEX_SCHEMA_KEY_ONE, COMPLEX_SCHEMA_KEY_TWO, COMPLEX_SCHEMA_KEY_THREE)

DYNAMO_VALID_ENDPOINT_URL = 'http://localhost:8000'
DYNAMO_INVALID_ENDPOINT_URL = 'http://invalid:9000'

aws_conf = {
    'aws_access_key_id': 'dummy_key',
    'aws_secret_access_key': 'dummy_secret',
    'region_name': 'dummy_region'}


class TestDynamoSimpleClass(unittest.TestCase):

    def setUp(self):
        aws_conf['endpoint_url'] = DYNAMO_VALID_ENDPOINT_URL
        self.dyn = SimpleTableClass(conf=aws_conf)
        self.dyn.create_table(SIMPLE_SCHEMA, SIMPLE_SCHEMA_TABLE_NAME)

    def test_valid(self):
        self.dyn.set_value('sample_key', 'dummy_value')
        data = self.dyn.get('sample_key')
        self.assertEqual(data['Item'][SIMPLE_SCHEMA_VALUE]['S'], 'dummy_value')


class TestDynamoComplexClass(unittest.TestCase):

    def setUp(self):
        aws_conf['endpoint_url'] = DYNAMO_VALID_ENDPOINT_URL
        self.dyn = ComplexTableClass(conf=aws_conf)
        self.dyn.create_table(COMPLEX_SCHEMA, COMPLEX_SCHEMA_TABLE_NAME)
        self.table = self.dyn.get_table(COMPLEX_SCHEMA_TABLE_NAME)
        self.key = '2020-01-01-01-5'

        last_update = datetime.utcnow().strftime('%Y-%m-%d-%H-%M')

        self.sample = {
            COMPLEX_SCHEMA_KEY_ONE: {'S': self.key},
        }

        self.sample_data = {
            'field_number': {'N': '22485'},
            'field_string': {'S': 'sample_bucket'},
            'field_path': {'S': 'some/path'},
            'field_date': {'S': '2020-01-01-01-5'},
            COMPLEX_SCHEMA_KEY_THREE: {'S': last_update},
            COMPLEX_SCHEMA_KEY_TWO: {'S': GREEN}
            }

        self.complete_sample = {}
        self.complete_sample.update(self.sample)
        self.complete_sample.update(self.sample_data)

    def test_valid(self):
        self.dyn.put(self.key, self.sample_data)

        data = self.dyn.get(self.key)

        self.assertEqual(self.complete_sample, data['Item'])

    def test_update(self):
        self.dyn.put(self.key, self.sample_data)
        self.dyn.update(self.key, RED)

        self.complete_sample.update({COMPLEX_SCHEMA_KEY_TWO: {'S': RED}})

        data = self.dyn.get(self.key)

        self.assertEqual(self.complete_sample, data['Item'])

    def test_filters(self):
        TOTAL_ITEMS = 50

        with self.table.batch_writer() as batch:
            for i in range(TOTAL_ITEMS):
                batch.put_item(
                    Item={
                        COMPLEX_SCHEMA_KEY_ONE: '2020-01-01-01-{}'.format(str(i)),
                        COMPLEX_SCHEMA_KEY_TWO: RED,
                        COMPLEX_SCHEMA_KEY_THREE: datetime.utcnow().strftime('%Y-%m-%d-%H-%M')
                    }
                )

        response = self.dyn.filter_by_key_one(self.key, RED)
        self.assertEqual(len(response['Items']), 1)

        response = self.dyn.filter_by_key_two(RED)
        self.assertEqual(len(response['Items']), TOTAL_ITEMS)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
