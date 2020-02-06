import unittest

from dynamo.conf import aws_conf
from samples.domain.interface import DynamoDomain
from samples.domain.schema import SCHEMA, TABLE_NAME


class TestDynamoDomain(unittest.TestCase):

    def setUp(self):
        self.dyn = DynamoDomain(conf=aws_conf)
        self.dyn.create_table(SCHEMA, TABLE_NAME)
        self.dyn.set_value('http://example.com/video', 'example.com')
        self.dyn.set_value('http://example.com/article', 'example.com')

    def test_get_video(self):
        data = self.dyn.get_domain('http://example.com/video')

        self.assertEqual(data, 'http://example.com/video')

    def test_get_article(self):
        data = self.dyn.get_domain('http://example.com/article')

        self.assertEqual(data, 'http://example.com/article')

    def test_exists(self):
        url_one = self.dyn.exists('http://example.com/video')
        url_two = self.dyn.exists('http://example.com/article')
        url_three = self.dyn.exists('http://example.com/post')

        self.assertTrue(url_one)
        self.assertTrue(url_two)
        self.assertFalse(url_three)

    def test_remove(self):
        url_key = 'http://example.com/image'
        self.dyn.set_value(url_key, 'example.com')

        self.dyn.remove(url_key)

    def test_scan(self):
        data = self.dyn.list_all()
        self.assertEqual(data['Count'], 2)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
