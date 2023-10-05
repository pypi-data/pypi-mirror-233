import os

import eikon as ek
import pytest
from eikon.eikonError import EikonError

APP_KEY = os.getenv("DESKTOP_APP_KEY")
payload = (
    '{ "Analysis": [ "OHLCV"], '
    '"EndDate": "2015-10-01T10:00:00","StartDate": "2015-09-01T10:00:00", "Tickers": [ "EUR="]}'
)


class TestApplicationKey:
    def test_not_set_app_key(self):
        ek.set_app_key("")
        with pytest.raises(EikonError) as e:
            ek.send_json_request("TATimeSeries", payload)
        assert e.value is not None, "No exception raised, but the exception expected."
        assert isinstance(
            e.value, EikonError
        ), f"Invalid exception type received: {type(e)}"
        # timeout returns in CI
        # assert (
        #     "Application key  is not valid!" in e.value.message
        # ), f"Invalid exception message received"

    def test_set_app_key_and_send_a_request(self):
        ek.set_app_key(APP_KEY)
        payload = (
            '{ "Analysis": [ "OHLCV"], '
            '"EndDate": "2015-10-01T10:00:00","StartDate": "2015-09-01T10:00:00", "Tickers": [ "EUR="]}'
        )
        response = ek.send_json_request("TATimeSeries", payload)
        assert response is not None
        assert response != ""
