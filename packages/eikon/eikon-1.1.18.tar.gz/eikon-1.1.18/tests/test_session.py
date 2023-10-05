import os
import sys
from unittest.mock import patch

import pytest
from httpx import Response

if sys.version_info >= (3, 8):
    from unittest.mock import AsyncMock

import eikon as eik


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8 or higher.")
@pytest.mark.asyncio
async def test_desktop_session_add_headers_and_cookies_properly():
    response = Response(status_code=200, text="Response text")

    with patch.dict(
        os.environ, {"DP_PROXY_APP_VERSION": "1", "REFINITIV_AAA_USER_ID": "2"}
    ):
        session = eik.DesktopSession(app_key="foo")
        session._http_session.request = AsyncMock(return_value=response)
        await session.http_request_async(url="http://localhost:9001/api/status")
        session._http_session.request.assert_called_once_with(
            "GET",
            "http://localhost:9001/api/status",
            headers={"app-version": "1", "x-tr-applicationid": "foo"},
            cookies={"user-uuid": "2"},
            data=None,
            params=None,
            json=None,
            follow_redirects=True,
        )
