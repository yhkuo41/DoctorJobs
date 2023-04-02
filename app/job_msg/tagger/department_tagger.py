from collections import defaultdict

from app.job_msg.schema import JobMsgDebugResponse
from app.job_msg.tagger.dept import Dept


class DepartmentTagger:
    def __init__(self, dept2keywords: dict[Dept:set[str]] = None, neg_keywords2depts: dict[str:set[Dept]] = None):
        """
        Tagger to extract doctor departments from the message
        Args:
            dept2keywords: 科別標準名稱 to 關鍵字列表
            neg_keywords2depts: 反向關鍵字 to 科別列表，排除過濾用
        """
        if not dept2keywords:
            dept2keywords = {
                Dept.GM: {
                    "一般內科", "一般內", "消化內科", "消化科", "肝膽腸胃內科", "肝膽腸胃科", "腸胃科",
                    "胸腔內科", "胸腔內科", "心臟內科", "心內", "血液腫瘤科", "血腫", "血液科",
                    "腫瘤科", "過敏風濕免疫科", "風濕免疫科", "風濕免疫", "風免", "新陳代謝科",
                    "內分泌科", "感染內科", "感染科", "感染"},
                Dept.GS: {
                    "一般外科", "心臟血管外科", "心臟外科", "心外", "胸腔外科", "胸外", "整形外科",
                    "整外", "神經外科", "神外", "泌尿外科", "泌尿科", "泌尿", "大腸直腸外科",
                    "直腸外科"
                },
                Dept.ENT: {"耳鼻喉", "五官科"},
                Dept.NEURO: {"神經內科", "神經科"},
                Dept.NS: {"腦神經外科", "神外", "神經外"},
                Dept.OBGYN: {"婦產", "婦科", "產科", "不孕", "人工生殖"},
                Dept.PEDIATRICS: {
                    "小兒", "小兒科", "兒童心臟科", "新生兒科", "兒童腎臟科", "兒童骨科", "小兒神經科", "小兒胃腸科",
                    "小兒血液腫瘤科", "小兒免疫風濕科", "兒科", "兒專"
                },
                Dept.OPH: {"眼科"},
                Dept.ANES: {"麻醉"},
                Dept.RAD: {"放射線科", "放射"},
                Dept.DERMA: {"皮膚科", "皮膚"},
                Dept.ORTH: {},
                Dept.GU: {"泌尿"},
                Dept.PSY: {"精神", "身心科"},
                Dept.PATHO: {"病理"},
                Dept.REH: {"復健", "運動醫學科", "運動醫學"},
                Dept.NUCLEAR: {"核子醫學", "核醫"},
                Dept.ER: {"急診醫學", "急診"},
                Dept.FM: {"家庭醫學", "家醫"},
                Dept.OM: {"職業醫學", "職醫", "廠醫"},
                Dept.AESTHETIC: {"醫學美容", "醫美", "醫療美容"},
                Dept.IMAGING: {"醫影", "醫療影像科", "放射科", "放射", "放射腫瘤科", "放腫"},
                Dept.GENERAL: {"不限專科", "各科", "不限科"},
                Dept.SPECIAL: {"疫苗診", "疫苗快打", "疫苗支援", "掛牌", "掛照", "開業科", "拓點"}
            }
        if not neg_keywords2depts:
            neg_keywords2depts = {
                "神經內外": {Dept.GS, Dept.GM}
            }
        self.neg_keywords2depts = neg_keywords2depts
        self.keyword2depts = defaultdict(set)
        """關鍵字 to 科別列表"""
        self.keyword2depts["神經內外"].update({Dept.NS, Dept.NEURO})
        self.keyword2depts["內外"].update({Dept.GS, Dept.GM})
        for dept, keywords in dept2keywords.items():
            self.keyword2depts[str(dept.value)].add(dept)  # 內科:內科
            for k in keywords:
                self.keyword2depts[k].add(dept)  # 一般內科:內科

    def debug(self, response: JobMsgDebugResponse) -> None:
        for k, depts in self.keyword2depts.items():
            if k in response.raw_msg:
                response.keyword_to_depts[k] = depts
        for nk, depts in self.neg_keywords2depts.items():
            if nk in response.raw_msg:
                response.keyword_to_neg_depts[nk] = depts
        response.dept_tags = self.tags_from_msg(response.raw_msg)

    def tags_from_msg(self, msg: str) -> set[Dept]:
        tags = set()
        if not msg:
            return tags
        for k, depts in self.keyword2depts.items():
            if k in msg:
                tags = tags.union(depts)
        for nk, depts in self.neg_keywords2depts.items():
            if nk in msg:
                tags -= depts
        return tags


dept_tagger = DepartmentTagger()
