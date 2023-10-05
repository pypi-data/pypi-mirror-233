import glob
import os
import tempfile
from unittest import TestCase

from nose.tools import raises


class TestProfile(TestCase):
    tmp_dir = tempfile.gettempdir()
    file_pattern = os.path.join(tmp_dir, "pyeikon*.log")

    # Remove *.log files before each test
    @classmethod
    def setup_class(cls):
        for filename in os.listdir(os.curdir):
            if filename.endswith(".log"):
                os.remove(filename)

    @classmethod
    def tearDownClass(cls):
        for filename in os.listdir(os.curdir):
            if filename.endswith(".log"):
                os.remove(filename)

        for filename in glob.glob(cls.file_pattern):
            os.remove(filename)

    @raises(AttributeError)
    def test_profile_with_wrong_appid_1(self):
        from eikon.Profile import get_profile

        get_profile().set_app_key([])

    @raises(AttributeError)
    def test_profile_with_wrong_appid_2(self):
        from eikon.Profile import get_profile

        get_profile().set_app_key({"a": "b"})

    @raises(AttributeError)
    def test_profile_with_wrong_appid_3(self):
        from eikon.Profile import get_profile

        get_profile().set_app_key(12345)

    def test_log_path(self):
        import logging
        import glob

        # clean old pyeikon.*.log files in TEMP directory
        for filename in glob.glob(self.file_pattern):
            os.remove(filename)

        # check no pyeikon.*.log file is in TEMP directory
        self.assertFalse(glob.glob(self.file_pattern))
        from eikon.Profile import Profile

        profile = Profile()
        profile.set_app_key("123")
        profile.set_log_path(self.tmp_dir)
        profile.set_log_level(logging.INFO)

        # check that a pyeikon.*.log was created
        self.assertTrue(glob.glob(self.file_pattern))

    def test_logger(self):
        import logging

        # clean old pyeikon.*.log files in current directory
        file_pattern = os.path.join(os.curdir, "pyeikon*.log")
        for filename in glob.glob(file_pattern):
            os.remove(filename)

        # check that no pyeikon.*.log is in current directory
        filenames = os.listdir(os.curdir)
        self.assertFalse(any((filename.endswith(".log")) for filename in filenames))

        from eikon.Profile import Profile

        profile = Profile()
        profile.set_app_key("123")
        profile.set_log_path(os.curdir)
        profile.set_log_level(logging.INFO)

        # check that a pyeikon.*.log was created
        filenames = os.listdir(os.curdir)
        self.assertTrue(any((filename.endswith(".log")) for filename in filenames))
