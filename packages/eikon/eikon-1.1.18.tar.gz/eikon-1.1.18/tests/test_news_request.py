import logging
import unittest

import eikon

# from nose.tools import with_setup, assert_raises
from mock import patch

json_result_get_news_headlines_for_IBM = {
    "headlines": [
        {
            "firstCreated": "2016-01-01T15:04:05",
            "versionCreated": "2016-01-01T15:04:05",
            "storyId": "storyId",
            "text": "IBM news headline",
        }
    ]
}

json_result_get_story_for_IBM = {
    "story": {"headlineHtml": "headline content", "storyHtml": "story content"}
}

headline_IBM = (
    "2016-07-20 15:47:17",
    {
        "versionCreated": "2016-07-20 15:47:34",
        "text": "AP Top News at 11:44 a.m. EDT<IBM.N><M.N>",
        "storyId": "urn:newsml:reuters.com:20160720:nNRA2a4sam:1",
        "sourceCode": "NS:ASSOPR",
        "Name": "2016-07-20 15:47:17",
        "dtype": "object",
    },
)

result_get_story_for_IBM = "story content"


class Mock_Profile(object):
    def __init__(self, app_key):
        self.app_key = app_key
        self.port = 3000
        self.url = "http://localhost:{0}/api/v1/data".format(self.port)
        self.logger = logging.getLogger("pyeikon")

    def get_app_key(self):
        return self.app_key

    def get_url(self):
        return self.url


class TestNewsHeadlineRequest(unittest.TestCase):
    def setUp(self):
        eikon.set_app_key("1234")

    @patch("eikon.Profile.get_profile")
    def test_raise_AttributeError(self, mock_get_profile):
        from eikon import get_news_headlines

        mock_get_profile.return_value = Mock_Profile("12345")

        # test get_news_headlines
        # check error on query parameter
        self.assertRaises(ValueError, get_news_headlines, 1234, raw_output=True)
        self.assertRaises(ValueError, get_news_headlines, {"a": 1}, raw_output=True)
        self.assertRaises(ValueError, get_news_headlines, ["a", 1], raw_output=True)

        # check error on headline_count parameter
        self.assertRaises(
            ValueError, get_news_headlines, "query", "abcd", raw_output=True
        )
        self.assertRaises(
            ValueError, get_news_headlines, "query", {"a": 1}, raw_output=True
        )
        self.assertRaises(ValueError, get_news_headlines, "query", [1], raw_output=True)
        self.assertRaises(ValueError, get_news_headlines, "query", -5, raw_output=True)

        # check error on date_from parameter
        self.assertRaises(
            ValueError, get_news_headlines, "query", 10, "abcd", raw_output=True
        )
        self.assertRaises(
            ValueError, get_news_headlines, "query", 10, 1234, raw_output=True
        )
        self.assertRaises(
            ValueError, get_news_headlines, "query", 10, {"a": 1}, raw_output=True
        )
        self.assertRaises(
            ValueError, get_news_headlines, "query", 10, ["a", 1], raw_output=True
        )

        # check error on date_to parameter
        self.assertRaises(
            ValueError,
            get_news_headlines,
            "query",
            10,
            "2016-01-01T15:04:05",
            "abcd",
            raw_output=True,
        )
        self.assertRaises(
            ValueError,
            get_news_headlines,
            "query",
            10,
            "2016-01-01T15:04:05",
            1234,
            raw_output=True,
        )
        self.assertRaises(
            ValueError,
            get_news_headlines,
            "query",
            10,
            "2016-01-01T15:04:05",
            {"a": 1},
            raw_output=True,
        )
        self.assertRaises(
            ValueError,
            get_news_headlines,
            "query",
            10,
            "2016-01-01T15:04:05",
            [1, 2],
            raw_output=True,
        )

    @patch("eikon.json_requests.send_json_request")
    @patch("eikon.Profile.get_profile")
    def test_get_headlines(self, get_profile, send_json_request):
        from eikon import get_news_headlines

        get_profile.return_value = Mock_Profile("12345")
        send_json_request.return_value = json_result_get_news_headlines_for_IBM
        self.assertEqual(
            json_result_get_news_headlines_for_IBM,
            get_news_headlines("IBM", raw_output=True),
        )

    @patch("eikon.json_requests.send_json_request")
    @patch("eikon.Profile.get_profile")
    def test_get_story(self, mock_get_profile, send_json_request):
        from eikon import get_news_story

        mock_get_profile.return_value = Mock_Profile("12345")
        send_json_request.return_value = json_result_get_story_for_IBM
        self.assertEqual(
            json_result_get_story_for_IBM, get_news_story(headline_IBM, raw_output=True)
        )
