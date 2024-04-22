import unittest
from dateutil import tz
from loxone_listener import parse_log_data


class ParsingTestCase(unittest.TestCase):

    def test_parsing_simple(self):
        result = parse_log_data('2020-09-10 19:46:20;Bedroom temperature;23.0'.encode(), tz.tzutc(), tz.tzutc())
        self.assertEqual({
            'time': '2020-09-10T19:46:20Z',
            'measurement': 'Bedroom temperature',
            'fields': {'value': 23.0},
            'tags': {'Source': 'Loxone', 'Tag_1': '', 'Tag_2': '', 'Tag_3': ''},
        }, result[0])

    def test_parsing_values__notags_vs_tags(self):
        result = parse_log_data('2020-09-10 19:46:20;TEMP;-3.8'.encode(), tz.tzutc(), tz.tzutc())
        self.assertEqual(-3.8, result[0]['fields']['value'])
        result = parse_log_data('2020-09-10 19:46:20;TEMP;-3.35;MyTag'.encode(), tz.tzutc(), tz.tzutc())
        self.assertEqual(-3.35, result[0]['fields']['value'])

    def test_parsing_different_values(self):
        result = parse_log_data('2020-09-10 19:46:20;Bedroom temperature;22'.encode(), tz.tzutc(), tz.tzutc())
        self.assertEqual(22, result[0]['fields']['value'])


if __name__ == '__main__':
    unittest.main()
