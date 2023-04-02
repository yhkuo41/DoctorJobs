from datetime import datetime
from unittest import TestCase

from pydantic import ValidationError

from app.job_msg.schema import JobMsgPutRequest, ContactInfo, JobMsgQueryRequest, JobMsg
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

    def test_valid_tags(self):
        query = JobMsgQueryRequest(city_tags={City.TAIPEI})

        self.assertEqual({City.TAIPEI}, query.city_tags)


class TestJobMsg(TestCase):
    def test_pretty_msg1(self):
        job_msg = JobMsg(
            job_msg_id="642724b05e7966237f8883d9",
            raw_msg="""* 誠徵［專任醫師］*
1. 新北市下新莊 診所 ，近丹鳳/泰山貴和站，交通便利、有停車位。

2.  誠徵  小兒科、家醫科、內科，急診， ENT、腸胃科 醫師


3.  每周6-7診、 節次可議、 需上假日班、亦可先報備支援兼診

4.  薪資優渥，執照費+診費+PPF，面洽

5. 院長會親自分享開業、看診經驗、歡迎有志開業的醫師加入

6. 詳情請洽  02-29066999林醫師""",
            city_tags={City.NEW_TAIPEI, City.TAIPEI},
            dept_tags={Dept.FM, Dept.ER, Dept.GM, Dept.PEDIATRICS},
            contact_info=ContactInfo(
                telephone="02-29066999",
                contact_person="林醫師"
            ),
            working_hours="每周6-7診、 節次可議",
            create_ts=datetime.utcnow(),
            update_ts=datetime.utcnow(),
            is_delete=False,
        )

        expect = """*訊息id*
642724b05e7966237f8883d9
*原始訊息*

* 誠徵［專任醫師］*
1. 新北市下新莊 診所 ，近丹鳳/泰山貴和站，交通便利、有停車位。

2.  誠徵  小兒科、家醫科、內科，急診， ENT、腸胃科 醫師


3.  每周6-7診、 節次可議、 需上假日班、亦可先報備支援兼診

4.  薪資優渥，執照費+診費+PPF，面洽

5. 院長會親自分享開業、看診經驗、歡迎有志開業的醫師加入

6. 詳情請洽  02-29066999林醫師

*地區*
新北市 臺北市
*科別*
內科 家庭醫學科 小兒科 急診醫學科
*工作時間*
每周6-7診、 節次可議
*手機*
02-29066999
*聯絡人*
林醫師"""
        self.assertEqual(expect, job_msg.pretty_msg())
