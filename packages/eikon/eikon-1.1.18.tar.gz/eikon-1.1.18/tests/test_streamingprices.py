import eikon as ek
import pytest

from conftest import check_pricing_data, APP_KEY


class TestStreamingPrices:
    @pytest.mark.skip(reason="hangs in CI")
    @pytest.mark.parametrize(
        "instruments,fields",
        [
            (
                ["FXFX", "EUR=", "GBP=", "JPY=", "CAD="],
                ["DSPLY_NAME", "BID", "ASK", "ROW64_1", "ROW64_2"],
            )
        ],
    )
    def test_open_streaming_pricing_and_getting_snapshot(self, instruments, fields):
        ek.set_app_key(APP_KEY)

        streaming_prices = ek.StreamingPrices(
            instruments=instruments,
            fields=fields,
            on_refresh=lambda streaming_price, instrument_name, fields: print(
                f"REFRESH {instrument_name}: {fields}"
            ),
            on_update=lambda streaming_price, instrument_name, fields: print(
                f"UPDATE {instrument_name}: {fields}"
            ),
            on_status=lambda streaming_price, instrument_name, status: print(
                f"STATUS {instrument_name}: {status}"
            ),
            on_complete=lambda streaming_prices: print(
                f"COMPLETE {streaming_prices.get_snapshot()}"
            ),
        )
        streaming_prices.open()
        snap = streaming_prices.get_snapshot()
        streaming_prices.close()

        check_pricing_data(snap, instruments, fields)
