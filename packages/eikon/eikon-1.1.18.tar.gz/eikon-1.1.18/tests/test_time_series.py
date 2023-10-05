from unittest import TestCase

import eikon
from mock import patch

json_result_from_timeseries = {
    "timeseriesData": [
        {
            "dataPoints": [
                [
                    "2016-12-01T00:00:00Z",
                    194.207808,
                    190.375,
                    192.2,
                    191,
                    19059,
                    104508409,
                ],
                [
                    "2016-12-02T00:00:00Z",
                    192.7163,
                    188.85,
                    191.1,
                    191.4,
                    15866,
                    92887431,
                ],
            ],
            "fields": [
                {"name": "TIMESTAMP", "type": "DateTime"},
                {"name": "HIGH", "type": "Double"},
                {"name": "LOW", "type": "Double"},
                {"name": "OPEN", "type": "Double"},
                {"name": "CLOSE", "type": "Double"},
                {"name": "COUNT", "type": "Double"},
                {"name": "VOLUME", "type": "Double"},
            ],
            "ric": "VOD.L",
            "statusCode": "Normal",
        }
    ]
}


class Test_Time_Series(TestCase):
    def setUp(self):
        eikon.set_app_key("1234")

    def test_get_timeseries_wrong_parameters(self):
        # rics must be a string or a list of string
        """Check ValueError exception is raised when type of rics is not string nor list of strings"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            1234,
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            {"a": 1},
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            True,
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            [1234],
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            [{"a": 1}],
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            [True],
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
        )

        """Check ValueError exception is raised when start_date isn't a datetime"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "abcd",
            "2016-02-01T15:04:05",
        )
        self.assertRaises(
            ValueError, eikon.get_timeseries, "IBM.N", None, 1234, "2016-02-01T15:04:05"
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            {"a": 1},
            "2016-02-01T15:04:05",
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            ["a", 1],
            "2016-02-01T15:04:05",
        )

        """Check ValueError exception is raised when end_date isn't a datetime"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "abcd",
        )
        self.assertRaises(
            ValueError, eikon.get_timeseries, "IBM.N", None, "2016-01-01T15:04:05", 1234
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            {"a": 1},
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            [1, 2],
        )

        """Check ValueError exception is raised when start_date = newer then end_date"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2022-04-15T15:04:05",
            "2022-04-14T15:04:05",
        )

        """Check ValueError exception is raised when type of interval is not string"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            1234,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            True,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            ["123"],
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            {"a": 1},
        )

        """Check ValueError exception is raised when fields is not in type list [None, string, list]"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            1234,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            True,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            [123],
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            {"a": 1},
        )

        """Check ValueError exception is raised when count is not an integer"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            True,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            [123],
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            {"a": 1},
        )

        """Check ValueError exception is raised when type of calendar is not string"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            1234,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            True,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            ["123"],
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            {"a": 1},
        )

        """Check ValueError exception is raised when type of calendar is not string"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            1234,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            True,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            ["123"],
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            {"a": 1},
        )

        """Check ValueError exception is raised when type of corax is not string"""
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            None,
            1234,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            None,
            True,
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            None,
            ["123"],
        )
        self.assertRaises(
            ValueError,
            eikon.get_timeseries,
            "IBM.N",
            None,
            "2016-01-01T15:04:05",
            "2016-02-01T15:04:05",
            None,
            None,
            None,
            {"a": 1},
        )

    """Check if lower case parameters are properly set to upper case"""

    @patch("eikon.json_requests.send_json_request")
    def test_get_timeseries_lower_parameters(self, mock_send_json_request):
        mock_send_json_request.return_value = json_result_from_timeseries

        self.assertFalse(
            mock_send_json_request.called, "called not initialized correctly"
        )

        payload = {
            "rics": ["GOOG.O"],
            "interval": "daily",
            "enddate": "2016-01-05T15:04:05-07:00",
            "startdate": "2016-01-01T15:04:05-07:00",
            "fields": ["HIGH", "LOW", "OPEN", "CLOSE", "COUNT", "VOLUME", "TIMESTAMP"],
        }

        result = eikon.get_timeseries(
            "goog.o",
            fields=["high", "low", "open", "close", "count", "volume"],
            start_date="2016-01-01T15:04:05-07:00",
            end_date="2016-01-05T15:04:05-07:00",
            interval="daily",
        )

        # check that json_send_request was called with expected parameters
        mock_send_json_request.assert_called_once_with(
            "TimeSeries", payload, debug=False
        )
