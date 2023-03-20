from analysis_scripts.line_chat_msg import LineChatMsg


class KeywordFilter:
    def __init__(self, keywords=None):
        if keywords is None:
            keywords = {}
        self.keywords = keywords.copy()

    def apply(self, msg) -> bool:
        """
        return True if the msg is a recruitment message
        """
        if isinstance(msg, str):
            return self.contains_any_keyword(msg)
        elif isinstance(msg, LineChatMsg):
            return self.contains_any_keyword(msg.content)

        raise NotImplementedError(f"not support msg type: {type(msg)}")

    def contains_any_keyword(self, msg: str) -> bool:
        for k in self.keywords:
            if k in msg:
                return True
        return False

    def filter_condition(self):
        return f"包含其中一個關鍵字 {self.keywords}"


class StrLenFilter:
    def __init__(self, min_len: int):
        self.min_len = min_len

    def apply(self, msg) -> bool:
        """
        return True if the msg is a recruitment message
        """
        if isinstance(msg, str):
            return len(msg) >= self.min_len
        elif isinstance(msg, LineChatMsg):
            return len(msg.content) >= self.min_len

        raise NotImplementedError(f"not support msg type: {type(msg)}")

    def filter_condition(self):
        return f"訊息長度 > {self.min_len}"


class DeptFilter:
    @staticmethod
    def apply(msg: LineChatMsg) -> bool:
        """
        return True if the msg is a recruitment message
        """
        if msg.dept_tags:
            return True
        return False

    @staticmethod
    def filter_condition():
        return f"經過DepartmentTagger後有醫師科別標籤"


class CityFilter:
    @staticmethod
    def apply(msg: LineChatMsg) -> bool:
        """
        return True if the msg is a recruitment message
        """
        if msg.city_tags:
            return True
        return False

    @staticmethod
    def filter_condition():
        return f"經過CityTagger後有縣市行政區標籤"


class DeptOrCityFilter:
    @staticmethod
    def apply(msg: LineChatMsg) -> bool:
        """
        return True if the msg is a recruitment message
        """
        return CityFilter.apply(msg) or DeptFilter.apply(msg)

    @staticmethod
    def filter_condition():
        return f"{DeptFilter.filter_condition()} OR {CityFilter.filter_condition()}"


filters = [
    KeywordFilter({"徵", "職缺", "禮聘", "誠聘", "支援", "急需", "需求", "每診"}),
    StrLenFilter(30),
    DeptOrCityFilter()
]
