# coding: utf-8

from datetime import datetime, timedelta
from unittest import TestCase

from dateutil.tz import tzlocal
from httpx import HTTPError


class TestTools(TestCase):
    def test_isStringType(self):
        from eikon.tools import is_string_type

        self.assertTrue(is_string_type("string"))
        self.assertTrue(is_string_type("string"))
        self.assertFalse(is_string_type(1234))
        self.assertFalse(is_string_type(["string"]))
        self.assertFalse(is_string_type({"string"}))

    def test_check_for_string(self):
        from eikon.tools import check_for_string

        self.assertIsNone(check_for_string("string", "test"))
        self.assertIsNone(check_for_string("string", "test"))
        self.assertRaises(ValueError, check_for_string, 1234, "test")
        self.assertRaises(ValueError, check_for_string, ["string"], "test")
        self.assertRaises(ValueError, check_for_string, {"key": "value"}, "test")

    def test_check_for_string_or_list_of_strings(self):
        from eikon.tools import check_for_string_or_list_of_strings

        self.assertIsNone(check_for_string_or_list_of_strings("string", "test"))
        self.assertIsNone(check_for_string_or_list_of_strings("string", "test"))
        self.assertIsNone(
            check_for_string_or_list_of_strings(["string1", "string2"], "test")
        )
        self.assertIsNone(check_for_string_or_list_of_strings(["string"], "test"))
        self.assertRaises(ValueError, check_for_string_or_list_of_strings, 1234, "test")
        self.assertRaises(
            ValueError, check_for_string_or_list_of_strings, ["string1", 123], "test"
        )
        self.assertRaises(
            ValueError, check_for_string_or_list_of_strings, {"string"}, "test"
        )

    def test_get_json_value(self):
        from eikon.tools import get_json_value

        self.assertEqual("value", get_json_value({"name": "value"}, "name"))
        self.assertEqual(None, get_json_value({"name2": "value"}, "name1"))

    def test_check_server_error(self):
        from eikon.json_requests import _check_server_error
        from eikon import EikonError

        class Response:
            ErrorCode = "403"
            ErrorMessage = "Forbidden"

        self.assertRaises(HTTPError, _check_server_error, Response())
        self.assertRaises(HTTPError, _check_server_error, "<HTTP error>")
        self.assertRaises(
            EikonError,
            _check_server_error,
            {"ErrorCode": 500, "ErrorMessage": "error message"},
        )
        self.assertIsNone(_check_server_error("normal response"))

    def test_to_datetime(self):
        from eikon.tools import to_datetime

        self.assertEqual(
            to_datetime("2016-01-01T15:04:05"), datetime(2016, 1, 1, 15, 4, 5)
        )
        self.assertEqual(
            to_datetime("2016-01-01 15:04:05"), datetime(2016, 1, 1, 15, 4, 5)
        )
        self.assertEqual(to_datetime("2016-01-01"), datetime(2016, 1, 1))
        self.assertRaises(ValueError, to_datetime, "everything but a date")

        # check date and time are correctly computed
        #  (ignore milliseconds with timetuple() function)
        dt1 = datetime.now(tzlocal()) + timedelta(-10)
        dt2 = to_datetime(timedelta(-10))
        tt1 = dt1.timetuple()
        tt2 = dt2.timetuple()
        self.assertEqual(tt1, tt2)

    def test_get_date_from_today(self):
        from eikon.tools import get_date_from_today, to_datetime

        self.assertRaises(ValueError, to_datetime, "everything but a date")

        date_value = datetime.date(to_datetime(timedelta(-10)))
        self.assertEqual(datetime.date(get_date_from_today(10)), date_value)
