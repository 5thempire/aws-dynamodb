import unittest

from dynamo.conf import aws_conf
from samples.domain.interface import DynamoDomain
from samples.domain.schema import SCHEMA, TABLE_NAME


class TestDynamoDomain(unittest.TestCase):

    def setUp(self):
        self.dyn = DynamoDomain(conf=aws_conf)
        self.dyn.create_table(SCHEMA, TABLE_NAME)

    def test_get_url(self):
        self.dyn.set_value('example.com', 'http://example.com/some/other/page')
        data = self.dyn.get_url('example.com')

        self.assertEqual(data, 'http://example.com/some/other/page')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
