import logging
from unittest import TestCase

import httpx
from eikon import EikonError
from mock import patch, Mock, MagicMock


class Mock_Profile(object):
    session = None

    def __init__(self, application_key):
        self.app_key = application_key
        self.port = 3000
        self.url = "http://localhost:{0}/api/v1/data".format(self.port)
        self.session = httpx.AsyncClient()
        self.logger = logging.getLogger("pyeikon")
        setattr(self.logger, "trace", lambda *args: self.logger.log(5, *args))

    def set_app_key(self, app_key):
        self.app_key = app_key

    def get_app_key(self):
        return self.app_key

    def get_url(self):
        return self.url

    def get_session(self):
        return self.session

    def get_timeout(self):
        return 60

    def get_log_level(self):
        return 100


class Mock_Response(object):
    def __init__(self, status_code, response):
        self._status_code = status_code
        self._json = response

    @property
    def status_code(self):
        return self._status_code

    def json(self, **kwargs):
        return str(self._json)

    def text(self):
        return str(self.json())


class TestSend_json_request(TestCase):
    @patch("eikon.Profile.get_profile")
    def test_raise_AttributeError_if_entity_not_string(self, mock_get_profile):
        mock_get_profile.return_value = Mock()
        from eikon.json_requests import send_json_request

        self.assertRaises(ValueError, send_json_request, 1234, {})
        self.assertRaises(ValueError, send_json_request, True, {})
        self.assertRaises(ValueError, send_json_request, {"entity": "test"}, {})
        self.assertRaises(ValueError, send_json_request, ["entity"], {})

    @patch("eikon.Profile.get_profile")
    def test_raise_AttributeError_if_payload_not_dict(self, mock_get_profile):
        mock_get_profile.return_value = Mock()
        from eikon.json_requests import send_json_request

        self.assertRaises(ValueError, send_json_request, "entity", "payload")
        self.assertRaises(ValueError, send_json_request, "entity", True)
        self.assertRaises(ValueError, send_json_request, "entity", ["payload"])
        self.assertRaises(ValueError, send_json_request, "entity", 12345)

    @patch("eikon.Profile.get_profile")
    def test_raise_payload_jsondecode(self, mock_get_profile):
        mock_get_profile.return_value = Mock()
        from eikon.json_requests import send_json_request
        from json import JSONDecodeError

        self.assertRaises(JSONDecodeError, send_json_request, "entity", "x")

    @patch("eikon.Profile.get_profile")
    def test_enter_on_Exception(self, mock_get_profile):
        mock_profile = Mock_Profile("12345")
        setattr(mock_profile, "send_request", MagicMock(side_effect=AttributeError))
        mock_get_profile.return_value = mock_profile

        from eikon.json_requests import send_json_request

        self.assertIsNone(send_json_request("entity", {}))
        mock_profile.send_request.assert_called_once()

    @patch("eikon.Profile.get_profile")
    def test_raise_EikonError_on_ConnectionError(self, mock_get_profile):
        mock_profile = Mock_Profile("12345")
        setattr(
            mock_profile,
            "send_request",
            MagicMock(
                side_effect=httpx.ConnectTimeout("ConnectTimeout", request=MagicMock())
            ),
        )
        mock_get_profile.return_value = mock_profile

        from eikon.json_requests import send_json_request

        with self.assertRaises(EikonError) as ex_info:
            send_json_request("entity", {})
        self.assertEqual(ex_info.exception.code, 408)
        mock_profile.send_request.assert_called_once()

    @patch("eikon.Profile.get_profile")
    def test_raise_EikonError_on_HTTPError(self, mock_get_profile):
        mock_profile = Mock_Profile("12345")
        setattr(
            mock_profile,
            "send_request",
            MagicMock(side_effect=httpx.HTTPError("HTTPError")),
        )
        mock_get_profile.return_value = mock_profile

        from eikon.json_requests import send_json_request

        with self.assertRaises(EikonError) as ex_info:
            send_json_request("entity", {})
        self.assertEqual(ex_info.exception.code, 401)
        mock_profile.send_request.assert_called_once()

    @patch("eikon.Profile.get_profile")
    def test_raise_TimeoutError_on_ConnectionTimeout(self, mock_get_profile):
        mock_profile = Mock_Profile("12345")
        setattr(
            mock_profile,
            "send_request",
            MagicMock(
                side_effect=httpx.TimeoutException(
                    "TimeoutException", request=MagicMock()
                )
            ),
        )
        mock_get_profile.return_value = mock_profile

        from eikon.json_requests import send_json_request

        with self.assertRaises(EikonError) as ex_info:
            send_json_request("entity", {}, debug=True)
        self.assertEqual(ex_info.exception.code, 408)
        mock_profile.send_request.assert_called_once()

    @patch("eikon.Profile.get_profile")
    def test_raise_EikonError_on_DecodingError(self, mock_get_profile):
        mock_profile = Mock_Profile("12345")

        setattr(
            mock_profile,
            "send_request",
            MagicMock(
                side_effect=httpx.DecodingError("DecodingError", request=MagicMock())
            ),
        )
        mock_get_profile.return_value = mock_profile

        from eikon.json_requests import send_json_request

        with self.assertRaises(EikonError) as ex_info:
            send_json_request("entity", {}, debug=True)
        self.assertEqual(ex_info.exception.code, 401)
        mock_profile.send_request.assert_called_once()

    @patch("eikon.Profile.get_profile")
    def test_raise_exception_when_post_status_code_error(self, mock_get_profile):
        mock_profile = Mock_Profile("12345")
        setattr(
            mock_profile,
            "send_request",
            MagicMock(return_value=Mock_Response(400, "error")),
        )
        mock_profile.send_request.return_value.headers = {}
        mock_get_profile.return_value = mock_profile

        from eikon.json_requests import send_json_request

        with self.assertRaises(EikonError) as ex_info:
            send_json_request("entity", {})
        self.assertEqual(ex_info.exception.code, 400)

    @patch("eikon.Profile.get_profile")
    @patch("eikon.Profile.get_url")
    def test_result_when_post_status_code_200(self, mock_get_url, mock_get_profile):
        mock_profile = Mock_Profile("12345")
        setattr(
            mock_profile,
            "send_request",
            MagicMock(return_value=Mock_Response(200, {"key1": "value1"})),
        )
        mock_get_profile.return_value = mock_profile
        mock_get_url.return_value = "http://localhost:3000/api/v1/data"

        from eikon.json_requests import send_json_request

        self.assertEqual("{'key1': 'value1'}", send_json_request("entity", {}))

    @patch("eikon.Profile.get_profile")
    def test_result_when_post_datagrib_async_code_200(self, mock_get_profile):
        mock_profile = Mock_Profile("12345")
        setattr(
            mock_profile,
            "send_request",
            MagicMock(return_value=Mock_Response(200, {"key1": "value1"})),
        )
        mock_get_profile.return_value = mock_profile
        from eikon.json_requests import send_json_request
        from eikon.data_grid import DataGridAsync_UDF_endpoint

        self.assertEqual(
            "{'key1': 'value1'}", send_json_request(DataGridAsync_UDF_endpoint, {})
        )

    @patch("eikon.json_requests._check_ticket_async")
    @patch("eikon.Profile.get_profile")
    def test_result_when_post_datagrib_async_with_ticket(
        self, mock_get_profile, mock_get_ticket
    ):
        mock_profile = Mock_Profile("12345")
        setattr(
            mock_profile,
            "send_request",
            MagicMock(
                side_effect=[
                    Mock_Response(200, "x"),
                    Mock_Response(200, {"key1": "value1"}),
                ]
            ),
        )
        mock_get_profile.return_value = mock_profile
        mock_get_ticket.side_effect = ["test_ticket", ""]

        from eikon.json_requests import send_json_request
        from eikon.data_grid import DataGridAsync_UDF_endpoint

        self.assertEqual(
            "{'key1': 'value1'}", send_json_request(DataGridAsync_UDF_endpoint, {})
        )

    # @patch('eikon.Profile.get_profile')
    # @patch('eikon.Profile.Profile.get_url')
    # @patch('eikon.vendor.requests_async.Session.post')
    # def test_debug_output(self, mock_requests_post, mock_get_url, mock_get_profile):
    #     mock_get_profile.return_value = Mock_Profile('12345')
    #     mock_get_url.return_value = 'http://localhost:3000/api/v1/data'
    #     mock_requests_post.return_value = Mock_Response(200, {"key1": "value1"})
    #     from eikon.json_requests import send_json_request
    #     send_json_request('entity', {}, debug=True)
    #     output = sys.stdout.getvalue().strip() # because stdout is an StringIO instance
    #     output = output.split('\n')
    #     first_output = output[0].split(':', 1)
    #     first_output = {first_output[0]: json.loads(first_output[1])}
    #     self.assertEquals(first_output, {'Request': {'Entity': {'E': 'entity', 'W': {}}}})
    #     result = 'HTTP Response: 200 - <bound method Mock_Response'
    #     self.assertEquals(output[1][:len(result)], result)
