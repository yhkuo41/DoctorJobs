import asyncio
import time
from pprint import pprint

from analysis_scripts.line_chat_analyzer import read_msg_from_file, MAN_CSV
from app.db.database import get_db
from app.job_msg import service
from app.job_msg.schema import recent_ts, JobMsgPutRequest
from app.job_msg.tagger.city import City

USER_ID = "U138383ec9583e853cb6859090b5e6745"
RECENT = int(recent_ts().timestamp())

if __name__ == '__main__':
    man_msgs = read_msg_from_file(MAN_CSV)
    man_msgs = [m for m in man_msgs if m.is_recruitment and m.utc_ts >= RECENT]
    db = next(get_db())

    total = len(man_msgs)
    i = 0

    for m in man_msgs:
        job_msg = JobMsgPutRequest(raw_msg=m.content, auto_tag=True)
        if "博田國際醫院誠徵兼任內視鏡檢查操作醫師兼任時段" in job_msg.raw_msg:
            job_msg.city_tags = {City.KAOHSIUNG}
            job_msg.auto_tag = False
        asyncio.run(service.tag_if_needed(job_msg))

        time.sleep(1)

        duplicates = asyncio.run(service.find_duplicate_job_msgs(job_msg, db.job_msg))
        if len(duplicates) > 1:
            raise ValueError(
                f"duplicate msg ids: {[m.job_msg_id for m in duplicates]}"
            )
        if len(duplicates) == 1:  # update
            job_msg.job_msg_id = duplicates[0].job_msg_id
            job_msg_id = asyncio.run(service.update_job_msg(job_msg, USER_ID, db.job_msg))
        else:
            job_msg_id = asyncio.run(service.insert_job_msg(job_msg, USER_ID, db.job_msg))
        job_msg.job_msg_id = job_msg_id

        i += 1
        print(f"{i}/{total}")
        pprint(vars(job_msg))
