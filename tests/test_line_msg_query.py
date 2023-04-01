from datetime import timedelta
from unittest import TestCase

from app.job_msg.line_msg_query import LineMsgQuery
from app.job_msg.schema import recent_ts
from app.job_msg.tagger.city import City
from app.job_msg.tagger.dept import Dept


class TestLineMsgQuery(TestCase):
    def test_init1(self):
        msg = """範例一
地區：臺北市, 新北市
科別: 內科，一般科
頁數: 1
        """
        q = LineMsgQuery(msg)
        self.assertEqual({City.TAIPEI, City.NEW_TAIPEI}, q.city_tags)
        self.assertEqual({Dept.GENERAL, Dept.GM}, q.dept_tags)
        self.assertEqual(0, q.skip)
        self.assertFalse(q.error_msgs)

    def test_init2(self):
        msg = """
地區： 臺北市
        """
        q = LineMsgQuery(msg)
        self.assertEqual({City.TAIPEI}, q.city_tags)
        self.assertEqual(set(), q.dept_tags)
        self.assertEqual(0, q.skip)
        self.assertFalse(q.error_msgs)

    def test_init3(self):
        msg = """範例三
科別: 內科
頁數: 2
        """
        q = LineMsgQuery(msg)
        self.assertEqual(set(), q.city_tags)
        self.assertEqual({Dept.GM}, q.dept_tags)
        self.assertEqual(5, q.skip)
        self.assertFalse(q.error_msgs)

    def test_init4(self):
        msg = "高雄內科頁數5"
        q = LineMsgQuery(msg)
        self.assertEqual({City.KAOHSIUNG}, q.city_tags)
        self.assertEqual({Dept.GM}, q.dept_tags)
        self.assertEqual(20, q.skip)
        self.assertFalse(q.error_msgs)

    def test_init_error1(self):
        msg = """範例三
頁數: 2
        """
        q = LineMsgQuery(msg)
        self.assertEqual(set(), q.city_tags)
        self.assertEqual(set(), q.dept_tags)
        self.assertEqual(5, q.skip)
        self.assertEqual("查詢條件至少須包含一個地區或科別標籤，可輸入help查看幫助訊息", q.error_msgs[0])

    def test_init_error2(self):
        msg = """範例三
地區：
科別: 內
頁數: 2
        """
        q = LineMsgQuery(msg)
        self.assertEqual(set(), q.city_tags)
        self.assertEqual(set(), q.dept_tags)
        self.assertEqual(5, q.skip)
        self.assertEqual("查詢條件至少須包含一個地區或科別標籤，可輸入help查看幫助訊息", q.error_msgs[0])

    def test_init_error3(self):
        msg = """範例一
地區：臺北市, a
科別: 內科，b
頁數: c
        """
        q = LineMsgQuery(msg)
        self.assertEqual({City.TAIPEI}, q.city_tags)
        self.assertEqual({Dept.GM}, q.dept_tags)
        self.assertEqual(0, q.skip)
        self.assertFalse(q.error_msgs)

    def test_init_error4(self):
        msg = """範例一
地區：臺北市，新北市，桃園市，新竹市，新竹縣，苗栗縣
科別: 內科，外科，一般科，小兒科，神經外科，神經內科
頁數: c
        """
        q = LineMsgQuery(msg)
        self.assertEqual(
            {City.TAIPEI, City.NEW_TAIPEI, City.HSINCHU_CITY, City.HSINCHU_COUNTY, City.TAOYUAN, City.MIAOLI},
            q.city_tags)
        self.assertEqual({Dept.GM, Dept.GS, Dept.GENERAL, Dept.PEDIATRICS, Dept.NEURO, Dept.NS}, q.dept_tags)
        self.assertEqual(0, q.skip)
        self.assertEqual("地區標籤最多5個", q.error_msgs[0])
        self.assertEqual("科別標籤最多5個", q.error_msgs[1])

    def test_to_query_request(self):
        msg = """範例一
        地區：臺北市, 新北市
        科別: 內科，一般科
        頁數: 0
                """
        q = LineMsgQuery(msg).to_query_request()
        start_time_minus_tem_min = recent_ts() - timedelta(minutes=10)
        self.assertEqual({City.TAIPEI, City.NEW_TAIPEI}, q.city_tags)
        self.assertEqual({Dept.GENERAL, Dept.GM}, q.dept_tags)
        self.assertEqual(0, q.skip)
        self.assertEqual(5, q.limit)
        self.assertGreater(q.start_time, start_time_minus_tem_min)
        self.assertIsNone(q.end_time)
