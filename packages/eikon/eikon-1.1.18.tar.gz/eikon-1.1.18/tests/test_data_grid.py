from unittest import TestCase

import eikon
from mock import patch

payload = {
    "requests": [
        {
            "instruments": ["GOOG.O"],
            "fields": [{"name": "TR.PriceOpen"}, {"name": "TR.PriceClose"}],
        }
    ]
}


json_result_from_datagrid = {
    "rowHeadersCount": 1,
    "data": [["googl.o", 992, 993.27]],
    "totalRowsCount": 2,
    "headers": [
        [
            {"displayName": "Instrument"},
            {"displayName": "Price Open", "field": "TR.PRICEOPEN"},
            {"displayName": "Price Close", "field": "TR.PRICECLOSE"},
        ]
    ],
    "columnHeadersCount": 1,
    "totalColumnsCount": 3,
    "headerOrientation": "horizontal",
}


class Test_DataGrid(TestCase):
    def setUp(self):
        eikon.set_app_key("1234")

    def test_get_data_wrong_parameters(self):
        ## get_data(instruments, fields, parameters=None, field_name=False, raw_output=False, debug=False)

        # rics must be a string or a list of string
        """Check ValueError exception is raised when type of rics is not string nor list of strings"""
        self.assertRaises(ValueError, eikon.get_data, "IBM.N", 1234)
        # self.assertRaises(ValueError, eikon.get_data, 'IBM.N', {'a': 1})
        self.assertRaises(ValueError, eikon.get_data, "IBM.N", True)
        self.assertRaises(ValueError, eikon.get_data, "IBM.N", [1234])
        # self.assertRaises(ValueError, eikon.get_data, 'IBM.N', [{'a': 1}])
        self.assertRaises(ValueError, eikon.get_data, "IBM.N", [True])

        """Check ValueError exception is raised when type of fields is not string nor list of strings"""
        self.assertRaises(ValueError, eikon.get_data, 1234, "TR.Close")
        self.assertRaises(ValueError, eikon.get_data, {"a": 1}, "TR.Close")
        self.assertRaises(ValueError, eikon.get_data, True, "TR.Close")
        self.assertRaises(ValueError, eikon.get_data, [1234], "TR.Close")
        self.assertRaises(ValueError, eikon.get_data, [{"a": 1}], "TR.Close")
        self.assertRaises(ValueError, eikon.get_data, [True], "TR.Close")

    """Check if lower case parameters are properly set to upper case"""

    @patch("eikon.json_requests.send_json_request")
    def test_get_data_lower_parameters(self, mock_send_json_request):
        mock_send_json_request.return_value = json_result_from_datagrid

        result = eikon.get_data(
            "goog.o",
            fields=["high", "low", "open", "close", "count", "volume"],
            raw_output=True,
        )
        # expected = [call('DataGrid', payload, False)]

    # check that json_send_request was called with expected parameters
    @patch("eikon.json_requests.send_json_request")
    def test_get_data_result(self, mock_send_json_request):
        mock_send_json_request.return_value = json_result_from_datagrid
        self.assertFalse(
            mock_send_json_request.called, "called not initialized correctly"
        )
        result = eikon.get_data("goog.o", ["TR.PriceOpen", "TR.PriceClose"])
        # check that json_send_request was called with expected parameters
        expected = payload
        mock_send_json_request.assert_called_once_with(
            "DataGrid_StandardAsync", expected, debug=False
        )

    @patch("eikon.json_requests.send_json_request")
    def test_get_data_result_without_headers(self, mock_send_json_request):
        mock_send_json_request.return_value = {
            "rowHeadersCount": 1,
            "data": [["googl.o", 992, 993.27]],
            "totalRowsCount": 2,
            "columnHeadersCount": 1,
            "totalColumnsCount": 3,
            "headerOrientation": "horizontal",
        }
        self.assertFalse(
            mock_send_json_request.called, "called not initialized correctly"
        )

        # 1) test field name
        result, err = eikon.get_data(
            "goog.o", ["TR.PriceOpen", "TR.PriceClose"], field_name=True
        )
        self.assertIsNone(result)
        self.assertIsNone(err)

        # 2) test without field name
        result, err = eikon.get_data(
            "goog.o", ["TR.PriceOpen", "TR.PriceClose"], field_name=False
        )
        self.assertIsNone(result)
        self.assertIsNone(err)

    # check that get_data returns DataFrame with expected headers
    @patch("eikon.json_requests.send_json_request")
    def test_get_data_headers(self, mock_send_json_request):
        mock_send_json_request.return_value = json_result_from_datagrid
        self.assertFalse(
            mock_send_json_request.called, "called not initialized correctly"
        )

        # test if result contains field names as column headers

        # 1) test field name
        result, err = eikon.get_data(
            "goog.o", ["TR.PriceOpen", "TR.PriceClose"], field_name=True
        )
        column_headers = list(result.columns.values)
        self.assertIn("Instrument", column_headers)
        self.assertIn("TR.PRICEOPEN", column_headers)
        self.assertIn("TR.PRICECLOSE", column_headers)
        self.assertNotIn("Price Open", column_headers)

        # 2) test displayt name
        result, err = eikon.get_data(
            "goog.o", ["TR.PriceOpen", "TR.PriceClose"], field_name=False
        )
        column_headers = list(result.columns.values)
        self.assertIn("Instrument", column_headers)
        self.assertIn("Price Open", column_headers)
        self.assertIn("Price Close", column_headers)
        self.assertNotIn("TR.PRICEOPEN", column_headers)

    def test_TR_Field(self):
        # rics must be a string or a list of string
        """Check ValueError exception is raised when type of rics is not string nor list of strings"""

        # test wrong values for params
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", 1234)
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", "nothing")
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", True)
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", {})

        # test wrong values for sort_dir
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", None, 1234)
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", None, "nothing")
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", None, True)
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", None, {})

        # test result for sort_dir
        field = eikon.TR_Field("Field_Name_1")
        self.assertEqual(field, {"Field_Name_1": {}})
        field = eikon.TR_Field("Field_Name_1", sort_dir="desc")
        self.assertEqual(field, {"Field_Name_1": {"sort_dir": "desc"}})

        # test wrong values for sort_priority
        self.assertRaises(
            ValueError, eikon.TR_Field, "Field_Name_1", None, "asc", "nothing"
        )
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", None, "asc", True)
        self.assertRaises(ValueError, eikon.TR_Field, "Field_Name_1", None, "asc", {})

        # test result for sort_priority
        field = eikon.TR_Field("Field_Name_1", sort_priority=1)
        self.assertEqual(field, {"Field_Name_1": {"sort_priority": 1}})

        field = eikon.TR_Field("Field_Name_1", sort_priority=None)
        self.assertEqual(field, {"Field_Name_1": {}})
