from datetime import datetime
from unittest import TestCase

from pydantic import ValidationError

from app.job_msg.schema import JobMsgPutRequest, ContactInfo, JobMsgQueryRequest
from app.job_msg.tagger.city import City
from app.job_msg.tagger.dept import Dept


class TestJobMsgPostRequest(TestCase):

    def test_create_job_msg(self):
        job_msg = JobMsgPutRequest(
            raw_msg="   this should be at least 20 characters   ",
            city_tags={City.TAIPEI, City.NEW_TAIPEI},
            dept_tags={Dept.GM, Dept.GS},
            contact_info=ContactInfo(
                telephone=" 0912345678 ",
                email=" a@gmail.com",
                contact_person="陳主任 "
            ),
            company=" 臺大醫院",
            job_desc=" 工作內容描述",
            salary_desc="每診10k ",
            working_hours=" 一週6-8節(必定需要:週二、週五、週日夜診) "
        )

        self.assertEqual("this should be at least 20 characters", job_msg.raw_msg)
        self.assertEqual({City.TAIPEI, City.NEW_TAIPEI}, job_msg.city_tags)
        self.assertEqual({Dept.GM, Dept.GS}, job_msg.dept_tags)
        self.assertEqual("0912345678", job_msg.contact_info.telephone)
        self.assertEqual("a@gmail.com", job_msg.contact_info.email)
        self.assertEqual("陳主任", job_msg.contact_info.contact_person)
        self.assertEqual("臺大醫院", job_msg.company)
        self.assertEqual("工作內容描述", job_msg.job_desc)
        self.assertEqual("每診10k", job_msg.salary_desc)
        self.assertEqual("一週6-8節(必定需要:週二、週五、週日夜診)", job_msg.working_hours)


class TestJobMsgQueryRequest(TestCase):
    def test_invalid_time_range(self):
        with self.assertRaises(ValidationError) as cm:
            time = datetime.utcnow()
            JobMsgQueryRequest(start_time=time, end_time=time, city_tags={City.TAIPEI})
        msg = str(cm.exception)
        self.assertIn("end_time can not before or equals to start_time", msg)

    def test_invalid_tags(self):
        with self.assertRaises(ValidationError) as cm:
            JobMsgQueryRequest(city_tags=set(), dept_tags=set())
        msg = str(cm.exception)
        self.assertIn("city_tags and dept_tags can not be both empty", msg)

    def test_too_many_tags(self):
        with self.assertRaises(KeyError) as cm:
            JobMsgQueryRequest(
                city_tags={City.TAIPEI,
                           City.NEW_TAIPEI,
                           City.CHIAYI_CITY,
                           City.HSINCHU_CITY,
                           City.TAINAN,
                           City.KAOHSIUNG})
        msg = str(cm.exception)
        self.assertIn("city_tags", msg)  # 太多items會移除此Key

    def test_valid_tags(self):
        query = JobMsgQueryRequest(city_tags={City.TAIPEI})

        self.assertEqual({City.TAIPEI}, query.city_tags)
