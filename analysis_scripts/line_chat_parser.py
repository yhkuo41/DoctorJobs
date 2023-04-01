# -*- coding: utf-8 -*-
import csv
import datetime
import re
from typing import Optional

from analysis_scripts import msg_filter
from analysis_scripts.line_chat_msg import LineChatMsg, csv_header
from app.job_msg.tagger.city_tagger import city_tagger
from app.job_msg.tagger.department_tagger import dept_tagger

SOURCE_TXT = "data/LINE______104A....txt"
RESULT_CSV = "data/line_chat_20220307_algo.csv"

DATE_PATTERN = re.compile(r"(\d{4}/\d{2}/\d{2})(（[一二三四五六日]）)")
MSG_PATTERN = re.compile(r"^([上下]午)(\d{2}):(\d{2})[ \t]([^\t\n]+)\t?(.*)")
"""
for normal message, like

下午10:36	社群副管理員	"徵《內/外/家醫科》專科醫師，歡迎介紹：

* 服務地點：
1.台南市東區裕東診所
2.台中市大里區元里診所
...

"""
SYS_MSG_PATTERN = re.compile(r"^([上下]午)(\d{2}):(\d{2})[ \t](\s.+)")
"""
for system message, like

上午08:36		社群副管理員已收回訊息

"""
TIME_ZONE = datetime.timezone(datetime.timedelta(hours=8))


class LineChatParser:
    """Parse history messages to message objects"""

    def __init__(self):
        self.results: list[tuple[datetime.datetime, str, str]] = []
        """
        parsing results [(msg datetime, user, msg content)]
        """
        self.cur_date: Optional[datetime.date] = None
        self.cur_msg: Optional[str] = None
        self.cur_msg_time: Optional[datetime.time] = None
        self.cur_msg_user: Optional[str] = None

    def read_line_chat(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='UTF-8') as txt:
            for line in txt:
                line = line.strip()
                if self.match_date_header(line):
                    continue
                # skip lines when there is no matching date
                if not self.cur_date:
                    continue

                if self.match_msg_start(line):
                    continue
                elif self.building_valid_msg():
                    # keep building old msg
                    self.cur_msg += line
                    self.cur_msg += "\n"
        # flush last msg
        if self.building_valid_msg():
            self.flush_cur_msg()

    def match_date_header(self, line: str) -> bool:
        matches = re.findall(DATE_PATTERN, line)
        if len(matches) != 1:
            return False
        date_str = matches[0][0].replace("/", "-")
        self.cur_date = datetime.date.fromisoformat(date_str)
        return True

    def match_msg_start(self, line: str) -> bool:
        # match system msg
        if re.findall(SYS_MSG_PATTERN, line) and self.building_valid_msg():
            self.flush_cur_msg()
            return True

        matches = re.findall(MSG_PATTERN, line)
        if not matches:
            return False
        matches = matches[0]
        # finish old msg at first
        if self.building_valid_msg():
            self.flush_cur_msg()
        hours = int(matches[1])
        if matches[0] == "下午":
            hours = (hours + 12) % 24  # 下午12:01 is 00:01 (24 hours format)
        minutes = int(matches[2])
        self.cur_msg_time = datetime.time(hours, minutes)
        self.cur_msg_user = matches[3]
        self.cur_msg = matches[4]
        return True

    def building_valid_msg(self) -> bool:
        return self.cur_date is not None \
            and self.cur_msg_time is not None \
            and self.cur_msg_user is not None \
            and self.cur_msg is not None

    def flush_cur_msg(self) -> None:
        dt = datetime.datetime.combine(self.cur_date, self.cur_msg_time, TIME_ZONE)
        self.cur_msg = self.cur_msg.replace('"', '').replace("\t", " ")
        self.results.append((dt, self.cur_msg_user, self.cur_msg))
        self.cur_msg = None
        self.cur_msg_time = None
        self.cur_msg_user = None


if __name__ == '__main__':
    """Parse history messages from txt then write to csv"""
    parser = LineChatParser()
    parser.read_line_chat(SOURCE_TXT)

    # 加上地區及科別標籤，並依照filters判斷是否為職缺訊息
    msg_list = []
    for res in parser.results:
        utc_ts = int(res[0].replace(tzinfo=datetime.timezone.utc).timestamp())
        msg = LineChatMsg(utc_ts, res[1], res[2])
        msg.city_tags = [e.value for e in city_tagger.tags_from_msg(msg.content)]
        msg.dept_tags = [e.value for e in dept_tagger.tags_from_msg(msg.content)]
        msg.is_recruitment = all(f.apply(msg) for f in msg_filter.filters)
        msg_list.append(msg)

    with open(RESULT_CSV, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header())
        for msg in msg_list:
            writer.writerow(msg.to_csv_row())
