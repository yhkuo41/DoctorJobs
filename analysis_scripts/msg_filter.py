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


class DeptFilter:
    @staticmethod
    def apply(msg: LineChatMsg) -> bool:
        """
        return True if the msg is a recruitment message
        """
        if msg.dept_tags:
            return True
        return False


class CityFilter:
    @staticmethod
    def apply(msg: LineChatMsg) -> bool:
        """
        return True if the msg is a recruitment message
        """
        if msg.city_tags:
            return True
        return False
