# -*- coding: utf-8 -*-
import datetime
from typing import Optional
import re
import csv

DATE_PATTERN = re.compile(r"\d{4}/\d{2}/\d{2}（[一二三四五六日]）")
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
                self.match_date_header(line)
                # skip lines when there is no matching date
                if not self.cur_date:
                    continue

                if self.match_msg_start(line):
                    continue
                elif self.building_valid_msg():
                    # keep building old msg
                    self.cur_msg += line
        # flush last msg
        if self.building_valid_msg():
            self.flush_cur_msg()

    def match_date_header(self, line: str) -> None:
        matches = re.findall(DATE_PATTERN, line)
        if len(matches) != 1:
            return
        date_str = matches[0][:-3].replace("/", "-")
        self.cur_date = datetime.date.fromisoformat(date_str)

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
        self.cur_msg = self.cur_msg.replace('"', '')
        self.results.append((dt, self.cur_msg_user, self.cur_msg))
        self.cur_msg = None
        self.cur_msg_time = None
        self.cur_msg_user = None


if __name__ == '__main__':
    parser = LineChatParser()
    parser.read_line_chat("LINE______104A....txt")

    with open('line_chat_20220307.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)

        for res in parser.results:
            utc_ts = res[0].replace(tzinfo=datetime.timezone.utc).timestamp()
            writer.writerow((utc_ts, res[1], res[2]))
