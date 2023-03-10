from analysis_scripts.line_chat_msg import LineChatMsg


class JobMsgFilter:
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
