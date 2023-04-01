from unittest import TestCase

from app.validator_util import remove_all_whitespaces


class Test(TestCase):
    def test_remove_all_whitespaces(self):
        msg = """範例一
地區: 臺北市, 新北市
科別: 內科, 一般科
頁數: 1
        """

        removed = remove_all_whitespaces(msg)
        self.assertEqual("範例一地區:臺北市,新北市科別:內科,一般科頁數:1", removed)
