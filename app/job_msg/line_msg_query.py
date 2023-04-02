from typing import List

from app.job_msg.schema import JobMsgQueryRequest
from app.job_msg.tagger.city_tagger import city_tagger
from app.job_msg.tagger.department_tagger import dept_tagger
from app.validator_util import find_first_num


class LineMsgQuery:

    def __init__(self, msg: str):
        self.city_tags = city_tagger.tags_from_msg(msg)
        self.dept_tags = dept_tagger.tags_from_msg(msg)
        self.skip: int = 0
        self.error_msgs: List[str] = []
        i = msg.find("頁數")
        if i != -1:
            page = find_first_num(msg[i + 2:], 1)
            self.skip = max(0, (int(page) - 1) * 5)
        if not self.city_tags and not self.dept_tags:
            self.error_msgs.append(f"查詢條件至少須包含一個地區或科別標籤，可輸入help查看幫助訊息")
        if len(self.city_tags) > 5:
            self.error_msgs.append(f"地區標籤最多5個")
        if len(self.dept_tags) > 5:
            self.error_msgs.append(f"科別標籤最多5個")

    def pretty_error_msgs(self) -> str:
        return "\n".join(self.error_msgs)

    def to_query_request(self) -> JobMsgQueryRequest:
        return JobMsgQueryRequest(
            city_tags=self.city_tags,
            dept_tags=self.dept_tags,
            limit=5,
            skip=self.skip
        )
