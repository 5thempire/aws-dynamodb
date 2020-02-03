import unittest
from datetime import datetime

from dynamo.conf import aws_conf
from samples.log.interface import DynamoLog
from samples.log.schema import SCHEMA, STATUS, TABLE_NAME, TIMESTAMP


class TestDynamoLog(unittest.TestCase):

    def setUp(self):
        self.dyn = DynamoLog(conf=aws_conf)
        self.dyn.create_table(SCHEMA, TABLE_NAME)
        self.table = self.dyn.get_table(TABLE_NAME)
        self.key = '2020-01-01-01-5'

        self.sample_data = {
            STATUS: {'S': 'INFO'},
            'message': {'S': 'sample log message'}
        }

    def test_get(self):
        self.dyn.put(self.key, self.sample_data)

        data = self.dyn.get(self.key)

        self.assertEqual(data['Item']['status']['S'], 'INFO')

    def test_update(self):
        self.dyn.put(self.key, self.sample_data)
        self.dyn.update(self.key, 'WARNING')

        data = self.dyn.get(self.key)
        self.assertEqual(data['Item']['status']['S'], 'WARNING')

    def test_filters(self):
        TOTAL_ITEMS = 50

        with self.table.batch_writer() as batch:
            for i in range(TOTAL_ITEMS):
                batch.put_item(
                    Item={
                        TIMESTAMP: '2020-01-01-01-{}'.format(str(i)),
                        STATUS: 'ERROR',
                        'message': f'#{i} log message'
                    }
                )

        response = self.dyn.filter_by_timestamp_status(self.key, 'ERROR')
        self.assertEqual(len(response['Items']), 1)

        response = self.dyn.filter_by_status('ERROR')
        self.assertEqual(len(response['Items']), TOTAL_ITEMS)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
