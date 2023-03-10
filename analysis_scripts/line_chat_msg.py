def csv_header() -> list[str]:
    return ["utc_ts", "user", "content", "is_recruitment_man", "is_recruitment_algo", "region_tags", "department_tags"]


class LineChatMsg:
    def __init__(self,
                 utc_ts,
                 user: str,
                 content: str,
                 region_tags=None,
                 department_tags=None,
                 is_recruitment_msg_algo=False,
                 is_recruitment_msg_man=False):
        if not region_tags or region_tags == "[]":
            region_tags = []
        if not department_tags or department_tags == "[]":
            department_tags = []
        self.is_recruitment_algo = bool(is_recruitment_msg_algo)
        self.is_recruitment_man = bool(is_recruitment_msg_man)
        self.department_tags = department_tags
        self.region_tags = region_tags
        self.content = content
        self.utc_ts = int(utc_ts)
        self.user = user

    def to_csv_row(self) -> list:
        return [
            self.utc_ts,
            self.user,
            self.content,
            str(self.is_recruitment_man)[0],
            str(self.is_recruitment_algo)[0],
            self.region_tags,
            self.department_tags
        ]
