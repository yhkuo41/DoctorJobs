def csv_header() -> list[str]:
    return ["utc_ts", "user", "content", "is_recruitment", "city_tags", "dept_tags"]


def set2str(s: set[str]):
    return "/".join(s)


def str2set(s: str):
    return set(s.split("/"))


class LineChatMsg:
    def __init__(self,
                 utc_ts: int,
                 user: str,
                 content: str,
                 city_tags: set[str] = None,
                 dept_tags: set[str] = None,
                 is_recruitment: bool = False):
        if not city_tags:
            city_tags = set()
        if not dept_tags:
            dept_tags = set()
        self.is_recruitment = is_recruitment
        self.dept_tags = dept_tags
        self.city_tags = city_tags
        self.content = content
        self.utc_ts = utc_ts
        self.user = user

    def to_csv_row(self) -> list:
        return [
            self.utc_ts,
            self.user,
            self.content,
            str(self.is_recruitment)[0],
            set2str(self.city_tags),
            set2str(self.dept_tags)
        ]
