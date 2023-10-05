from unittest import TestCase

import eikon
from mock import patch


class Test_Symbology(TestCase):
    def setUp(self):
        eikon.set_app_key("1234")

    def test_get_symbology_wrong_parameters(self):
        """Check ValueError exception is raised when type of symbol isn't a string nor a list"""
        self.assertRaises(ValueError, eikon.get_symbology, 1234)
        self.assertRaises(ValueError, eikon.get_symbology, {"a": 1})
        self.assertRaises(ValueError, eikon.get_symbology, True)

        """Check ValueeError exception is raised when type of from_symbol isn't a string"""
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", 1234)
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", True)
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", ["123"])
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", {"a": 1})

        """Check ValueError exception is raised when type of to_symbol isn't a string"""
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", "RIC", 1234)
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", "RIC", True)
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", "RIC", [123])
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", "RIC", {"a": 1})

        """Check ValueError exception is raised when type of to_symbol isn't a list of string"""
        self.assertRaises(
            ValueError, eikon.get_symbology, "IBM.N", "RIC", ["aaa", 1234]
        )
        self.assertRaises(
            ValueError, eikon.get_symbology, "IBM.N", "RIC", ["aaa", True]
        )
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", "RIC", {"a": 1})

        """Check ValueError exception is raised when from_symbol is unknown symbol type """
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", "RIQ", "ISIN")

        """Check ValueError exception is raised when to_symbol contains unknown symbol type """
        self.assertRaises(
            ValueError, eikon.get_symbology, "IBM.N", "RIC", "WrongSymbolType"
        )
        self.assertRaises(
            ValueError, eikon.get_symbology, "IBM.N", ["RIC", "WrongSymbolType"]
        )

        """Check TypeError exception is raised when bestMatch parameter is set """
        self.assertRaises(TypeError, eikon.get_symbology, "IBM.N", bestMatch=False)

        """Check ValueError exception is raised when best_match parameter is not bool value """
        self.assertRaises(ValueError, eikon.get_symbology, "IBM.N", best_match="test")

    @patch("eikon.json_requests.send_json_request")
    def test_get_symbology_case_insensitive_symbol_parameters(self, send_json_request):
        json_result_get_symbology_for_IBM = {
            "mappedSymbols": [
                {
                    "CUSIPs": ["IBM_CUSIP"],
                    "ISINs": ["IBM_ISIN"],
                    "RICs": ["IBM.N"],
                    "SEDOLs": ["IBM_SEDOL"],
                    "bestMatch": {
                        "CUSIP": "IBM_CUSIP",
                        "ISIN": "IBM_ISIN",
                        "RIC": "IBM.N",
                        "SEDOL": "IBM_SEDOL",
                        "ticker": "IBM",
                    },
                    "symbol": "IBM.N",
                }
            ]
        }

        send_json_request.return_value = json_result_get_symbology_for_IBM

        """Check happy path """
        result = eikon.get_symbology("IBM.N", "RIC", "ISIN", raw_output=True)
        expected = json_result_get_symbology_for_IBM
        self.assertEqual(result, expected)

        """Check rics and symbols arn't case sensitive """
        result = eikon.get_symbology("ibm.n", "Ric", "Isin", raw_output=True)
        self.assertEqual(result, expected)
