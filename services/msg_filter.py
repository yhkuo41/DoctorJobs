from analysis_scripts.line_chat_msg import LineChatMsg


class KeywordFilter:
    def __init__(self, keywords=None, neg_keywords=None):
        if keywords is None:
            keywords = {}
        if neg_keywords is None:
            neg_keywords = {}
        self.keywords = keywords.copy()
        """關鍵字清單，訊息包含至少一個關鍵字才視為職缺訊息"""
        self.neg_keywords = neg_keywords.copy()
        """反向關鍵字清單，訊息中包含任一關鍵字則非職缺訊息"""

    def apply(self, msg) -> bool:
        """
        return True if the msg is a recruitment message
        """
        if isinstance(msg, str):
            return self.contains_any_keyword(msg) and self.not_contains_any_neg_keyword(msg)
        elif isinstance(msg, LineChatMsg):
            return self.contains_any_keyword(msg.content) and self.not_contains_any_neg_keyword(msg.content)

        raise NotImplementedError(f"not support msg type: {type(msg)}")

    def contains_any_keyword(self, msg: str) -> bool:
        for k in self.keywords:
            if k in msg:
                return True
        return False

    def not_contains_any_neg_keyword(self, msg: str) -> bool:
        for k in self.neg_keywords:
            if k in msg:
                return False
        return True

    def filter_condition(self):
        return f"""包含 {self.keywords} 其中一個關鍵字
且不包含 {self.neg_keywords} 任一關鍵字"""


class StrLenFilter:
    def __init__(self, min_len: int):
        self.min_len = min_len
        """最小字串長度，訊息長度大於等於此長度才視為職缺訊息"""

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
        return f"訊息長度 >= {self.min_len}"


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
    KeywordFilter(
        keywords={"徵", "職缺", "禮聘", "誠聘", "支援", "急需", "需求", "每診", "聯絡", "請洽", "意者", "工作經驗",
                  "疫苗診", "疫苗快打", "疫苗支援", "掛牌", "掛照", "開業科", "拓點", "不限專科", "各科", "不限科",
                  "一般科"},
        neg_keywords={"參考格式", "格式參考", "已被邀請加入", "善用關鍵字搜尋", "內幕", "請問", "需自行查證"}
    ),
    StrLenFilter(30),
    DeptOrCityFilter()
]
