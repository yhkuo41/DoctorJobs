from unittest import TestCase

from app.job_msg.tagger.department_tagger import DepartmentTagger


class TestDepartmentTagger(TestCase):
    tagger = DepartmentTagger()

    def test_init(self):
        expect = {
            '一般內': {'內科'},
            '一般內科': {'內科'},
            '一般外科': {'外科'},
            '一般科': {'一般科'},
            '不孕': {'婦產科'},
            '不限專科': {'一般科'},
            '不限科': {'一般科'},
            '五官科': {'耳鼻喉科'},
            '人工生殖': {'婦產科'},
            '兒專': {'小兒科'},
            '兒科': {'小兒科'},
            '兒童心臟科': {'小兒科'},
            '兒童腎臟科': {'小兒科'},
            '兒童骨科': {'小兒科'},
            '內分泌科': {'內科'},
            '內外': {'內科', '外科'},
            '內科': {'內科'},
            '各科': {'一般科'},
            '外科': {'外科'},
            '大腸直腸外科': {'外科'},
            '婦產': {'婦產科'},
            '婦產科': {'婦產科'},
            '婦科': {'婦產科'},
            '家庭醫學': {'家庭醫學科'},
            '家庭醫學科': {'家庭醫學科'},
            '家醫': {'家庭醫學科'},
            '小兒': {'小兒科'},
            '小兒免疫風濕科': {'小兒科'},
            '小兒神經科': {'小兒科'},
            '小兒科': {'小兒科'},
            '小兒胃腸科': {'小兒科'},
            '小兒血液腫瘤科': {'小兒科'},
            '廠醫': {'職業醫學科'},
            '復健': {'復健科'},
            '復健科': {'復健科'},
            '心內': {'內科'},
            '心外': {'外科'},
            '心臟內科': {'內科'},
            '心臟外科': {'外科'},
            '心臟血管外科': {'外科'},
            '急診': {'急診醫學科'},
            '急診醫學': {'急診醫學科'},
            '急診醫學科': {'急診醫學科'},
            '感染': {'內科'},
            '感染內科': {'內科'},
            '感染科': {'內科'},
            '拓點': {'特殊需求'},
            '掛照': {'特殊需求'},
            '掛牌': {'特殊需求'},
            '放射': {'醫學影像科', '放射線科'},
            '放射科': {'醫學影像科'},
            '放射線科': {'放射線科'},
            '放射腫瘤科': {'醫學影像科'},
            '放腫': {'醫學影像科'},
            '整外': {'外科'},
            '整形外科': {'外科'},
            '新生兒科': {'小兒科'},
            '新陳代謝科': {'內科'},
            '核子醫學': {'核子醫學科'},
            '核子醫學科': {'核子醫學科'},
            '核醫': {'核子醫學科'},
            '泌尿': {'泌尿科', '外科'},
            '泌尿外科': {'外科'},
            '泌尿科': {'泌尿科', '外科'},
            '消化內科': {'內科'},
            '消化科': {'內科'},
            '特殊需求': {'特殊需求'},
            '產科': {'婦產科'},
            '疫苗快打': {'特殊需求'},
            '疫苗支援': {'特殊需求'},
            '疫苗診': {'特殊需求'},
            '病理': {'病理科'},
            '病理科': {'病理科'},
            '皮膚': {'皮膚科'},
            '皮膚科': {'皮膚科'},
            '直腸外科': {'外科'},
            '眼科': {'眼科'},
            '神外': {'外科', '神經外科'},
            '神經內外': {'神經內科', '神經外科'},
            '神經內科': {'神經內科'},
            '神經外': {'神經外科'},
            '神經外科': {'外科', '神經外科'},
            '神經科': {'神經內科'},
            '精神': {'精神科'},
            '精神科': {'精神科'},
            '耳鼻喉': {'耳鼻喉科'},
            '耳鼻喉科': {'耳鼻喉科'},
            '職業醫學': {'職業醫學科'},
            '職業醫學科': {'職業醫學科'},
            '職醫': {'職業醫學科'},
            '肝膽腸胃內科': {'內科'},
            '肝膽腸胃科': {'內科'},
            '胸外': {'外科'},
            '胸腔內科': {'內科'},
            '胸腔外科': {'外科'},
            '腦神經外科': {'神經外科'},
            '腫瘤科': {'內科'},
            '腸胃科': {'內科'},
            '血液科': {'內科'},
            '血液腫瘤科': {'內科'},
            '血腫': {'內科'},
            '身心科': {'精神科'},
            '運動醫學': {'復健科'},
            '運動醫學科': {'復健科'},
            '過敏風濕免疫科': {'內科'},
            '醫學影像科': {'醫學影像科'},
            '醫學美容': {'醫學美容科'},
            '醫學美容科': {'醫學美容科'},
            '醫影': {'醫學影像科'},
            '醫療影像科': {'醫學影像科'},
            '醫療美容': {'醫學美容科'},
            '醫美': {'醫學美容科'},
            '開業科': {'特殊需求'},
            '風免': {'內科'},
            '風濕免疫': {'內科'},
            '風濕免疫科': {'內科'},
            '骨科': {'骨科'},
            '麻醉': {'麻醉科'},
            '麻醉科': {'麻醉科'}
        }
        self.assertEqual(expect, self.tagger.keyword2depts)

    def test_keywords_from_msg1(self):
        msg = "新竹/專任兼任/骨科復健神經內科(轉自 ptt by spotjelly)誠徵骨科、復健科、神經內外科醫師正職、兼職皆可目前有3間診所新竹縣竹東鎮長春聯合診所(長春路2段89號)新竹市松青診所(" \
              "長春街58號)新竹縣新埔鎮頂竹骨科診所(田新六街56號)享保障薪及PPF 歡迎面談意者請聯繫陳醫師0921430288市話03-5772636（請勿寄站內信）"
        expect = {'內科', '外科', '復健', '內外', '骨科', '復健科', '神經內外', '神經內科'}
        self.assertEqual(expect, self.tagger.keywords_from_msg(msg))

    def test_keywords_from_msg2(self):
        msg = "😊謝謝前輩分享貼文 生活類/聊天討論類  (下次發文) 請幫我們移到  子群 ~聊天討論群喔    " \
              "再次謝謝前輩😊@大甲東醫霸您已被邀請加入「醫聊無上限醫起聊~醫師Lounge/教育學分/職缺討論/醫藥材團購、轉讓 1688 " \
              "DocJob」！請點選以下連結加入社群！https://line.me/ti/g2/afOBW9YvGhmiRf1Fx5_0oK7au3tH3bZ2DBpoAg?utm_source=invitation" \
              "&utm_medium=link_copy&utm_campaign=default"
        expect = set()
        self.assertEqual(expect, self.tagger.keywords_from_msg(msg))

    def test_keywords_from_empty(self):
        msg = "以上職缺(部分重複刊登)轉載自5000人/實名制群 👉歡迎雇主自貼 待聘醫師自薦👈"
        expect = set()
        self.assertEqual(expect, self.tagger.keywords_from_msg(msg))

    def test_tags_from_msg1(self):
        msg = "新竹/專任兼任/骨科復健神經內科(轉自 ptt by spotjelly)誠徵骨科、復健科、神經內外科醫師正職、兼職皆可目前有3間診所新竹縣竹東鎮長春聯合診所(長春路2段89號)新竹市松青診所(" \
              "長春街58號)新竹縣新埔鎮頂竹骨科診所(田新六街56號)享保障薪及PPF 歡迎面談意者請聯繫陳醫師0921430288市話03-5772636（請勿寄站內信）"
        expect = {'骨科', '神經外科', '神經內科', '復健科'}
        self.assertEqual(expect, self.tagger.tags_from_msg(msg))

    def test_tags_from_msg_empty(self):
        msg = "以上職缺(部分重複刊登)轉載自5000人/實名制群 👉歡迎雇主自貼 待聘醫師自薦👈"
        expect = set()
        self.assertEqual(expect, self.tagger.tags_from_msg(msg))