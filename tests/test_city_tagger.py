from unittest import TestCase

from city_tagger import CityTagger


class TestCityTagger(TestCase):
    tagger = CityTagger()

    def test_init(self):
        expect = {'臺北': '臺北市', '臺北中山': '臺北市', '臺北市中山': '臺北市', '臺北大同': '臺北市',
                  '臺北市大同': '臺北市', '臺北中正': '臺北市', '臺北市中正': '臺北市', '臺北南港': '臺北市',
                  '臺北市南港': '臺北市', '南港': '臺北市', '臺北內湖': '臺北市', '臺北市內湖': '臺北市',
                  '內湖': '臺北市', '臺北信義': '臺北市', '臺北市信義': '臺北市', '臺北大安': '臺北市',
                  '臺北市大安': '臺北市', '臺北文山': '臺北市', '臺北市文山': '臺北市', '臺北北投': '臺北市',
                  '臺北市北投': '臺北市', '北投': '臺北市', '臺北萬華': '臺北市', '臺北市萬華': '臺北市',
                  '萬華': '臺北市', '臺北松山': '臺北市', '臺北市松山': '臺北市', '臺北士林': '臺北市',
                  '臺北市士林': '臺北市', '新北': '新北市', '新北汐止': '新北市', '新北市汐止': '新北市',
                  '汐止': '新北市', '新北土城': '新北市', '新北市土城': '新北市', '土城': '新北市',
                  '新北萬里': '新北市', '新北市萬里': '新北市', '新北鶯歌': '新北市', '新北市鶯歌': '新北市',
                  '鶯歌': '新北市', '新北蘆洲': '新北市', '新北市蘆洲': '新北市', '蘆洲': '新北市',
                  '新北林口': '新北市', '新北市林口': '新北市', '林口': '新北市', '新北八里': '新北市',
                  '新北市八里': '新北市', '新北石門': '新北市', '新北市石門': '新北市', '新北金山': '新北市',
                  '新北市金山': '新北市', '新北瑞芳': '新北市', '新北市瑞芳': '新北市', '瑞芳': '新北市',
                  '新北平溪': '新北市', '新北市平溪': '新北市', '平溪': '新北市', '新北新莊': '新北市',
                  '新北市新莊': '新北市', '新莊': '新北市', '新北樹林': '新北市', '新北市樹林': '新北市',
                  '新北三重': '新北市', '新北市三重': '新北市', '三重': '新北市', '新北板橋': '新北市',
                  '新北市板橋': '新北市', '板橋': '新北市', '新北三峽': '新北市', '新北市三峽': '新北市',
                  '三峽': '新北市', '新北烏來': '新北市', '新北市烏來': '新北市', '烏來': '新北市',
                  '新北貢寮': '新北市', '新北市貢寮': '新北市', '貢寮': '新北市', '新北雙溪': '新北市',
                  '新北市雙溪': '新北市', '新北石碇': '新北市', '新北市石碇': '新北市', '石碇': '新北市',
                  '新北坪林': '新北市', '新北市坪林': '新北市', '新北深坑': '新北市', '新北市深坑': '新北市',
                  '深坑': '新北市', '新北五股': '新北市', '新北市五股': '新北市', '新北泰山': '新北市',
                  '新北市泰山': '新北市', '新北新店': '新北市', '新北市新店': '新北市', '新店': '新北市',
                  '新北淡水': '新北市', '新北市淡水': '新北市', '新北中和': '新北市', '新北市中和': '新北市',
                  '新北三芝': '新北市', '新北市三芝': '新北市', '新北永和': '新北市', '新北市永和': '新北市',
                  '基隆': '基隆市', '基隆中山': '基隆市', '基隆市中山': '基隆市', '基隆仁愛': '基隆市',
                  '基隆市仁愛': '基隆市', '基隆安樂': '基隆市', '基隆市安樂': '基隆市', '基隆暖暖': '基隆市',
                  '基隆市暖暖': '基隆市', '基隆七堵': '基隆市', '基隆市七堵': '基隆市', '七堵': '基隆市',
                  '基隆中正': '基隆市', '基隆市中正': '基隆市', '基隆信義': '基隆市', '基隆市信義': '基隆市',
                  '桃園': '桃園市', '桃園大溪': '桃園市', '桃園市大溪': '桃園市', '桃園八德': '桃園市',
                  '桃園市八德': '桃園市', '桃園龍潭': '桃園市', '桃園市龍潭': '桃園市', '龍潭': '桃園市',
                  '桃園大園': '桃園市', '桃園市大園': '桃園市', '大園': '桃園市', '桃園楊梅': '桃園市',
                  '桃園市楊梅': '桃園市', '楊梅': '桃園市', '桃園平鎮': '桃園市', '桃園市平鎮': '桃園市',
                  '平鎮': '桃園市', '桃園桃園': '桃園市', '桃園市桃園': '桃園市', '桃園復興': '桃園市',
                  '桃園市復興': '桃園市', '桃園龜山': '桃園市', '桃園市龜山': '桃園市', '桃園觀音': '桃園市',
                  '桃園市觀音': '桃園市', '桃園中壢': '桃園市', '桃園市中壢': '桃園市', '中壢': '桃園市',
                  '桃園新屋': '桃園市', '桃園市新屋': '桃園市', '桃園蘆竹': '桃園市', '桃園市蘆竹': '桃園市',
                  '蘆竹': '桃園市', '新竹': '新竹市', '新竹尖石': '新竹縣', '新竹縣尖石': '新竹縣',
                  '新竹關西': '新竹縣', '新竹縣關西': '新竹縣', '新竹竹東': '新竹縣', '新竹縣竹東': '新竹縣',
                  '竹東': '新竹縣', '新竹竹北': '新竹縣', '新竹縣竹北': '新竹縣', '竹北': '新竹縣',
                  '新竹湖口': '新竹縣', '新竹縣湖口': '新竹縣', '湖口': '新竹縣', '新竹芎林': '新竹縣',
                  '新竹縣芎林': '新竹縣', '新竹五峰': '新竹縣', '新竹縣五峰': '新竹縣', '新竹北埔': '新竹縣',
                  '新竹縣北埔': '新竹縣', '新竹寶山': '新竹縣', '新竹縣寶山': '新竹縣', '新竹新埔': '新竹縣',
                  '新竹縣新埔': '新竹縣', '新竹峨眉': '新竹縣', '新竹縣峨眉': '新竹縣', '新竹新豐': '新竹縣',
                  '新竹縣新豐': '新竹縣', '新竹橫山': '新竹縣', '新竹縣橫山': '新竹縣', '新竹香山': '新竹市',
                  '新竹市香山': '新竹市', '新竹北': '新竹市', '新竹市北': '新竹市', '新竹東': '新竹市',
                  '新竹市東': '新竹市', '苗栗': '苗栗縣', '苗栗造橋': '苗栗縣', '苗栗縣造橋': '苗栗縣',
                  '苗栗西湖': '苗栗縣', '苗栗縣西湖': '苗栗縣', '苗栗後龍': '苗栗縣', '苗栗縣後龍': '苗栗縣',
                  '苗栗三義': '苗栗縣', '苗栗縣三義': '苗栗縣', '苗栗獅潭': '苗栗縣', '苗栗縣獅潭': '苗栗縣',
                  '苗栗公館': '苗栗縣', '苗栗縣公館': '苗栗縣', '苗栗頭份': '苗栗縣', '苗栗縣頭份': '苗栗縣',
                  '苗栗大湖': '苗栗縣', '苗栗縣大湖': '苗栗縣', '苗栗卓蘭': '苗栗縣', '苗栗縣卓蘭': '苗栗縣',
                  '苗栗泰安': '苗栗縣', '苗栗縣泰安': '苗栗縣', '苗栗通霄': '苗栗縣', '苗栗縣通霄': '苗栗縣',
                  '苗栗銅鑼': '苗栗縣', '苗栗縣銅鑼': '苗栗縣', '苗栗竹南': '苗栗縣', '苗栗縣竹南': '苗栗縣',
                  '竹南': '苗栗縣', '苗栗南庄': '苗栗縣', '苗栗縣南庄': '苗栗縣', '南庄': '苗栗縣',
                  '苗栗苑裡': '苗栗縣', '苗栗縣苑裡': '苗栗縣', '苗栗苗栗': '苗栗縣', '苗栗縣苗栗': '苗栗縣',
                  '苗栗頭屋': '苗栗縣', '苗栗縣頭屋': '苗栗縣', '苗栗三灣': '苗栗縣', '苗栗縣三灣': '苗栗縣',
                  '臺中': '臺中市', '臺中南屯': '臺中市', '臺中市南屯': '臺中市', '臺中龍井': '臺中市',
                  '臺中市龍井': '臺中市', '臺中太平': '臺中市', '臺中市太平': '臺中市', '臺中大里': '臺中市',
                  '臺中市大里': '臺中市', '臺中西屯': '臺中市', '臺中市西屯': '臺中市', '臺中大肚': '臺中市',
                  '臺中市大肚': '臺中市', '臺中潭子': '臺中市', '臺中市潭子': '臺中市', '臺中大安': '臺中市',
                  '臺中市大安': '臺中市', '臺中后里': '臺中市', '臺中市后里': '臺中市', '后里': '臺中市',
                  '臺中大雅': '臺中市', '臺中市大雅': '臺中市', '臺中和平': '臺中市', '臺中市和平': '臺中市',
                  '臺中清水': '臺中市', '臺中市清水': '臺中市', '臺中北': '臺中市', '臺中市北': '臺中市',
                  '臺中南': '臺中市', '臺中市南': '臺中市', '臺中沙鹿': '臺中市', '臺中市沙鹿': '臺中市',
                  '沙鹿': '臺中市', '臺中神岡': '臺中市', '臺中市神岡': '臺中市', '神岡': '臺中市', '臺中西': '臺中市',
                  '臺中市西': '臺中市', '臺中新社': '臺中市', '臺中市新社': '臺中市', '臺中石岡': '臺中市',
                  '臺中市石岡': '臺中市', '石岡': '臺中市', '臺中霧峰': '臺中市', '臺中市霧峰': '臺中市',
                  '臺中東': '臺中市', '臺中市東': '臺中市', '臺中中': '臺中市', '臺中市中': '臺中市',
                  '臺中北屯': '臺中市', '臺中市北屯': '臺中市', '臺中豐原': '臺中市', '臺中市豐原': '臺中市',
                  '豐原': '臺中市', '臺中外埔': '臺中市', '臺中市外埔': '臺中市', '臺中梧棲': '臺中市',
                  '臺中市梧棲': '臺中市', '臺中大甲': '臺中市', '臺中市大甲': '臺中市', '大甲': '臺中市',
                  '臺中烏日': '臺中市', '臺中市烏日': '臺中市', '烏日': '臺中市', '臺中東勢': '臺中市',
                  '臺中市東勢': '臺中市', '南投': '南投縣', '南投埔里': '南投縣', '南投縣埔里': '南投縣',
                  '埔里': '南投縣', '南投國姓': '南投縣', '南投縣國姓': '南投縣', '南投竹山': '南投縣',
                  '南投縣竹山': '南投縣', '南投鹿谷': '南投縣', '南投縣鹿谷': '南投縣', '南投魚池': '南投縣',
                  '南投縣魚池': '南投縣', '南投中寮': '南投縣', '南投縣中寮': '南投縣', '南投仁愛': '南投縣',
                  '南投縣仁愛': '南投縣', '南投南投': '南投縣', '南投縣南投': '南投縣', '南投草屯': '南投縣',
                  '南投縣草屯': '南投縣', '草屯': '南投縣', '南投集集': '南投縣', '南投縣集集': '南投縣',
                  '集集': '南投縣', '南投信義': '南投縣', '南投縣信義': '南投縣', '南投名間': '南投縣',
                  '南投縣名間': '南投縣', '南投水里': '南投縣', '南投縣水里': '南投縣', '彰化': '彰化縣',
                  '彰化大村': '彰化縣', '彰化縣大村': '彰化縣', '彰化二林': '彰化縣', '彰化縣二林': '彰化縣',
                  '彰化芳苑': '彰化縣', '彰化縣芳苑': '彰化縣', '彰化溪州': '彰化縣', '彰化縣溪州': '彰化縣',
                  '彰化田中': '彰化縣', '彰化縣田中': '彰化縣', '彰化埤頭': '彰化縣', '彰化縣埤頭': '彰化縣',
                  '彰化彰化': '彰化縣', '彰化縣彰化': '彰化縣', '彰化田尾': '彰化縣', '彰化縣田尾': '彰化縣',
                  '彰化花壇': '彰化縣', '彰化縣花壇': '彰化縣', '彰化和美': '彰化縣', '彰化縣和美': '彰化縣',
                  '彰化芬園': '彰化縣', '彰化縣芬園': '彰化縣', '彰化線西': '彰化縣', '彰化縣線西': '彰化縣',
                  '彰化二水': '彰化縣', '彰化縣二水': '彰化縣', '彰化福興': '彰化縣', '彰化縣福興': '彰化縣',
                  '彰化員林': '彰化縣', '彰化縣員林': '彰化縣', '彰化伸港': '彰化縣', '彰化縣伸港': '彰化縣',
                  '彰化溪湖': '彰化縣', '彰化縣溪湖': '彰化縣', '彰化社頭': '彰化縣', '彰化縣社頭': '彰化縣',
                  '彰化秀水': '彰化縣', '彰化縣秀水': '彰化縣', '彰化鹿港': '彰化縣', '彰化縣鹿港': '彰化縣',
                  '鹿港': '彰化縣', '彰化北斗': '彰化縣', '彰化縣北斗': '彰化縣', '彰化埔心': '彰化縣',
                  '彰化縣埔心': '彰化縣', '彰化竹塘': '彰化縣', '彰化縣竹塘': '彰化縣', '彰化永靖': '彰化縣',
                  '彰化縣永靖': '彰化縣', '彰化埔鹽': '彰化縣', '彰化縣埔鹽': '彰化縣', '彰化大城': '彰化縣',
                  '彰化縣大城': '彰化縣', '雲林': '雲林縣', '雲林大埤': '雲林縣', '雲林縣大埤': '雲林縣',
                  '雲林褒忠': '雲林縣', '雲林縣褒忠': '雲林縣', '雲林斗南': '雲林縣', '雲林縣斗南': '雲林縣',
                  '斗南': '雲林縣', '雲林虎尾': '雲林縣', '雲林縣虎尾': '雲林縣', '虎尾': '雲林縣',
                  '雲林元長': '雲林縣', '雲林縣元長': '雲林縣', '雲林西螺': '雲林縣', '雲林縣西螺': '雲林縣',
                  '西螺': '雲林縣', '雲林臺西': '雲林縣', '雲林縣臺西': '雲林縣', '雲林東勢': '雲林縣',
                  '雲林縣東勢': '雲林縣', '雲林崙背': '雲林縣', '雲林縣崙背': '雲林縣', '雲林林內': '雲林縣',
                  '雲林縣林內': '雲林縣', '雲林口湖': '雲林縣', '雲林縣口湖': '雲林縣', '雲林斗六': '雲林縣',
                  '雲林縣斗六': '雲林縣', '斗六': '雲林縣', '雲林土庫': '雲林縣', '雲林縣土庫': '雲林縣',
                  '土庫': '雲林縣', '雲林水林': '雲林縣', '雲林縣水林': '雲林縣', '雲林北港': '雲林縣',
                  '雲林縣北港': '雲林縣', '北港': '雲林縣', '雲林四湖': '雲林縣', '雲林縣四湖': '雲林縣',
                  '雲林二崙': '雲林縣', '雲林縣二崙': '雲林縣', '雲林麥寮': '雲林縣', '雲林縣麥寮': '雲林縣',
                  '麥寮': '雲林縣', '雲林古坑': '雲林縣', '雲林縣古坑': '雲林縣', '古坑': '雲林縣',
                  '雲林莿桐': '雲林縣', '雲林縣莿桐': '雲林縣', '嘉義': '嘉義市', '嘉義大埔': '嘉義縣',
                  '嘉義縣大埔': '嘉義縣', '嘉義東石': '嘉義縣', '嘉義縣東石': '嘉義縣', '嘉義竹崎': '嘉義縣',
                  '嘉義縣竹崎': '嘉義縣', '嘉義中埔': '嘉義縣', '嘉義縣中埔': '嘉義縣', '嘉義溪口': '嘉義縣',
                  '嘉義縣溪口': '嘉義縣', '嘉義新港': '嘉義縣', '嘉義縣新港': '嘉義縣', '嘉義鹿草': '嘉義縣',
                  '嘉義縣鹿草': '嘉義縣', '嘉義梅山': '嘉義縣', '嘉義縣梅山': '嘉義縣', '嘉義朴子': '嘉義縣',
                  '嘉義縣朴子': '嘉義縣', '嘉義布袋': '嘉義縣', '嘉義縣布袋': '嘉義縣', '嘉義番路': '嘉義縣',
                  '嘉義縣番路': '嘉義縣', '嘉義六腳': '嘉義縣', '嘉義縣六腳': '嘉義縣', '嘉義水上': '嘉義縣',
                  '嘉義縣水上': '嘉義縣', '嘉義義竹': '嘉義縣', '嘉義縣義竹': '嘉義縣', '嘉義民雄': '嘉義縣',
                  '嘉義縣民雄': '嘉義縣', '嘉義阿里山': '嘉義縣', '嘉義縣阿里山': '嘉義縣', '嘉義大林': '嘉義縣',
                  '嘉義縣大林': '嘉義縣', '嘉義太保': '嘉義縣', '嘉義縣太保': '嘉義縣', '嘉義東': '嘉義市',
                  '嘉義市東': '嘉義市', '嘉義西': '嘉義市', '嘉義市西': '嘉義市', '臺南': '臺南市',
                  '臺南後壁': '臺南市', '臺南市後壁': '臺南市', '臺南中西': '臺南市', '臺南市中西': '臺南市',
                  '臺南下營': '臺南市', '臺南市下營': '臺南市', '臺南新市': '臺南市', '臺南市新市': '臺南市',
                  '臺南白河': '臺南市', '臺南市白河': '臺南市', '臺南仁德': '臺南市', '臺南市仁德': '臺南市',
                  '臺南南': '臺南市', '臺南市南': '臺南市', '臺南山上': '臺南市', '臺南市山上': '臺南市',
                  '臺南大內': '臺南市', '臺南市大內': '臺南市', '臺南楠西': '臺南市', '臺南市楠西': '臺南市',
                  '臺南將軍': '臺南市', '臺南市將軍': '臺南市', '臺南安平': '臺南市', '臺南市安平': '臺南市',
                  '臺南佳里': '臺南市', '臺南市佳里': '臺南市', '臺南安南': '臺南市', '臺南市安南': '臺南市',
                  '臺南南化': '臺南市', '臺南市南化': '臺南市', '臺南善化': '臺南市', '臺南市善化': '臺南市',
                  '臺南龍崎': '臺南市', '臺南市龍崎': '臺南市', '臺南關廟': '臺南市', '臺南市關廟': '臺南市',
                  '臺南麻豆': '臺南市', '臺南市麻豆': '臺南市', '臺南安定': '臺南市', '臺南市安定': '臺南市',
                  '臺南新化': '臺南市', '臺南市新化': '臺南市', '臺南七股': '臺南市', '臺南市七股': '臺南市',
                  '臺南北': '臺南市', '臺南市北': '臺南市', '臺南學甲': '臺南市', '臺南市學甲': '臺南市',
                  '臺南東山': '臺南市', '臺南市東山': '臺南市', '臺南柳營': '臺南市', '臺南市柳營': '臺南市',
                  '臺南玉井': '臺南市', '臺南市玉井': '臺南市', '臺南東': '臺南市', '臺南市東': '臺南市',
                  '臺南六甲': '臺南市', '臺南市六甲': '臺南市', '臺南鹽水': '臺南市', '臺南市鹽水': '臺南市',
                  '臺南永康': '臺南市', '臺南市永康': '臺南市', '臺南西港': '臺南市', '臺南市西港': '臺南市',
                  '臺南官田': '臺南市', '臺南市官田': '臺南市', '官田': '臺南市', '臺南新營': '臺南市',
                  '臺南市新營': '臺南市', '新營': '臺南市', '臺南左鎮': '臺南市', '臺南市左鎮': '臺南市',
                  '臺南北門': '臺南市', '臺南市北門': '臺南市', '臺南歸仁': '臺南市', '臺南市歸仁': '臺南市',
                  '歸仁': '臺南市', '高雄': '高雄市', '高雄阿蓮': '高雄市', '高雄市阿蓮': '高雄市',
                  '高雄楠梓': '高雄市', '高雄市楠梓': '高雄市', '楠梓': '高雄市', '高雄彌陀': '高雄市',
                  '高雄市彌陀': '高雄市', '高雄大社': '高雄市', '高雄市大社': '高雄市', '高雄仁武': '高雄市',
                  '高雄市仁武': '高雄市', '高雄田寮': '高雄市', '高雄市田寮': '高雄市', '高雄三民': '高雄市',
                  '高雄市三民': '高雄市', '高雄桃源': '高雄市', '高雄市桃源': '高雄市', '高雄內門': '高雄市',
                  '高雄市內門': '高雄市', '高雄岡山': '高雄市', '高雄市岡山': '高雄市', '高雄橋頭': '高雄市',
                  '高雄市橋頭': '高雄市', '橋頭': '高雄市', '高雄鹽埕': '高雄市', '高雄市鹽埕': '高雄市',
                  '高雄那瑪夏': '高雄市', '高雄市那瑪夏': '高雄市', '高雄林園': '高雄市', '高雄市林園': '高雄市',
                  '高雄左營': '高雄市', '高雄市左營': '高雄市', '左營': '高雄市', '高雄永安': '高雄市',
                  '高雄市永安': '高雄市', '高雄燕巢': '高雄市', '高雄市燕巢': '高雄市', '高雄甲仙': '高雄市',
                  '高雄市甲仙': '高雄市', '高雄梓官': '高雄市', '高雄市梓官': '高雄市', '高雄美濃': '高雄市',
                  '高雄市美濃': '高雄市', '美濃': '高雄市', '高雄鼓山': '高雄市', '高雄市鼓山': '高雄市',
                  '高雄鳥松': '高雄市', '高雄市鳥松': '高雄市', '高雄小港': '高雄市', '高雄市小港': '高雄市',
                  '高雄茂林': '高雄市', '高雄市茂林': '高雄市', '高雄前金': '高雄市', '高雄市前金': '高雄市',
                  '高雄前鎮': '高雄市', '高雄市前鎮': '高雄市', '高雄鳳山': '高雄市', '高雄市鳳山': '高雄市',
                  '鳳山': '高雄市', '高雄茄萣': '高雄市', '高雄市茄萣': '高雄市', '高雄新興': '高雄市',
                  '高雄市新興': '高雄市', '高雄大樹': '高雄市', '高雄市大樹': '高雄市', '高雄六龜': '高雄市',
                  '高雄市六龜': '高雄市', '高雄路竹': '高雄市', '高雄市路竹': '高雄市', '高雄大寮': '高雄市',
                  '高雄市大寮': '高雄市', '高雄湖內': '高雄市', '高雄市湖內': '高雄市', '高雄旗山': '高雄市',
                  '高雄市旗山': '高雄市', '高雄苓雅': '高雄市', '高雄市苓雅': '高雄市', '苓雅': '高雄市',
                  '高雄杉林': '高雄市', '高雄市杉林': '高雄市', '高雄旗津': '高雄市', '高雄市旗津': '高雄市',
                  '旗津': '高雄市', '屏東': '屏東縣', '屏東獅子': '屏東縣', '屏東縣獅子': '屏東縣',
                  '屏東崁頂': '屏東縣', '屏東縣崁頂': '屏東縣', '屏東林邊': '屏東縣', '屏東縣林邊': '屏東縣',
                  '屏東春日': '屏東縣', '屏東縣春日': '屏東縣', '屏東潮州': '屏東縣', '屏東縣潮州': '屏東縣',
                  '潮州': '屏東縣', '屏東麟洛': '屏東縣', '屏東縣麟洛': '屏東縣', '屏東東港': '屏東縣',
                  '屏東縣東港': '屏東縣', '東港': '屏東縣', '屏東滿州': '屏東縣', '屏東縣滿州': '屏東縣',
                  '屏東枋寮': '屏東縣', '屏東縣枋寮': '屏東縣', '枋寮': '屏東縣', '屏東牡丹': '屏東縣',
                  '屏東縣牡丹': '屏東縣', '屏東屏東': '屏東縣', '屏東縣屏東': '屏東縣', '屏東枋山': '屏東縣',
                  '屏東縣枋山': '屏東縣', '屏東三地門': '屏東縣', '屏東縣三地門': '屏東縣', '三地門': '屏東縣',
                  '屏東高樹': '屏東縣', '屏東縣高樹': '屏東縣', '屏東九如': '屏東縣', '屏東縣九如': '屏東縣',
                  '屏東新埤': '屏東縣', '屏東縣新埤': '屏東縣', '屏東鹽埔': '屏東縣', '屏東縣鹽埔': '屏東縣',
                  '屏東內埔': '屏東縣', '屏東縣內埔': '屏東縣', '屏東里港': '屏東縣', '屏東縣里港': '屏東縣',
                  '屏東車城': '屏東縣', '屏東縣車城': '屏東縣', '屏東琉球': '屏東縣', '屏東縣琉球': '屏東縣',
                  '琉球': '屏東縣', '屏東佳冬': '屏東縣', '屏東縣佳冬': '屏東縣', '屏東瑪家': '屏東縣',
                  '屏東縣瑪家': '屏東縣', '屏東南州': '屏東縣', '屏東縣南州': '屏東縣', '屏東萬巒': '屏東縣',
                  '屏東縣萬巒': '屏東縣', '屏東恆春': '屏東縣', '屏東縣恆春': '屏東縣', '恆春': '屏東縣',
                  '屏東新園': '屏東縣', '屏東縣新園': '屏東縣', '屏東萬丹': '屏東縣', '屏東縣萬丹': '屏東縣',
                  '屏東泰武': '屏東縣', '屏東縣泰武': '屏東縣', '屏東長治': '屏東縣', '屏東縣長治': '屏東縣',
                  '屏東竹田': '屏東縣', '屏東縣竹田': '屏東縣', '屏東來義': '屏東縣', '屏東縣來義': '屏東縣',
                  '屏東霧台': '屏東縣', '屏東縣霧台': '屏東縣', '宜蘭': '宜蘭縣', '宜蘭三星': '宜蘭縣',
                  '宜蘭縣三星': '宜蘭縣', '宜蘭羅東': '宜蘭縣', '宜蘭縣羅東': '宜蘭縣', '宜蘭大同': '宜蘭縣',
                  '宜蘭縣大同': '宜蘭縣', '宜蘭蘇澳': '宜蘭縣', '宜蘭縣蘇澳': '宜蘭縣', '蘇澳': '宜蘭縣',
                  '宜蘭五結': '宜蘭縣', '宜蘭縣五結': '宜蘭縣', '宜蘭宜蘭': '宜蘭縣', '宜蘭縣宜蘭': '宜蘭縣',
                  '宜蘭頭城': '宜蘭縣', '宜蘭縣頭城': '宜蘭縣', '宜蘭南澳': '宜蘭縣', '宜蘭縣南澳': '宜蘭縣',
                  '宜蘭壯圍': '宜蘭縣', '宜蘭縣壯圍': '宜蘭縣', '宜蘭員山': '宜蘭縣', '宜蘭縣員山': '宜蘭縣',
                  '宜蘭礁溪': '宜蘭縣', '宜蘭縣礁溪': '宜蘭縣', '礁溪': '宜蘭縣', '宜蘭冬山': '宜蘭縣',
                  '宜蘭縣冬山': '宜蘭縣', '花蓮': '花蓮縣', '花蓮瑞穗': '花蓮縣', '花蓮縣瑞穗': '花蓮縣',
                  '瑞穗': '花蓮縣', '花蓮壽豐': '花蓮縣', '花蓮縣壽豐': '花蓮縣', '花蓮卓溪': '花蓮縣',
                  '花蓮縣卓溪': '花蓮縣', '花蓮富里': '花蓮縣', '花蓮縣富里': '花蓮縣', '花蓮萬榮': '花蓮縣',
                  '花蓮縣萬榮': '花蓮縣', '花蓮新城': '花蓮縣', '花蓮縣新城': '花蓮縣', '花蓮吉安': '花蓮縣',
                  '花蓮縣吉安': '花蓮縣', '花蓮光復': '花蓮縣', '花蓮縣光復': '花蓮縣', '花蓮玉里': '花蓮縣',
                  '花蓮縣玉里': '花蓮縣', '玉里': '花蓮縣', '花蓮豐濱': '花蓮縣', '花蓮縣豐濱': '花蓮縣',
                  '花蓮花蓮': '花蓮縣', '花蓮縣花蓮': '花蓮縣', '花蓮秀林': '花蓮縣', '花蓮縣秀林': '花蓮縣',
                  '花蓮鳳林': '花蓮縣', '花蓮縣鳳林': '花蓮縣', '臺東': '臺東縣', '臺東延平': '臺東縣',
                  '臺東縣延平': '臺東縣', '臺東金峰': '臺東縣', '臺東縣金峰': '臺東縣', '臺東關山': '臺東縣',
                  '臺東縣關山': '臺東縣', '臺東臺東': '臺東縣', '臺東縣臺東': '臺東縣', '臺東達仁': '臺東縣',
                  '臺東縣達仁': '臺東縣', '臺東卑南': '臺東縣', '臺東縣卑南': '臺東縣', '臺東綠島': '臺東縣',
                  '臺東縣綠島': '臺東縣', '綠島': '臺東縣', '臺東太麻里': '臺東縣', '臺東縣太麻里': '臺東縣',
                  '太麻里': '臺東縣', '臺東蘭嶼': '臺東縣', '臺東縣蘭嶼': '臺東縣', '蘭嶼': '臺東縣',
                  '臺東成功': '臺東縣', '臺東縣成功': '臺東縣', '臺東長濱': '臺東縣', '臺東縣長濱': '臺東縣',
                  '臺東東河': '臺東縣', '臺東縣東河': '臺東縣', '臺東鹿野': '臺東縣', '臺東縣鹿野': '臺東縣',
                  '臺東池上': '臺東縣', '臺東縣池上': '臺東縣', '臺東海端': '臺東縣', '臺東縣海端': '臺東縣',
                  '臺東大武': '臺東縣', '臺東縣大武': '臺東縣', '澎湖': '澎湖縣', '澎湖望安': '澎湖縣',
                  '澎湖縣望安': '澎湖縣', '澎湖七美': '澎湖縣', '澎湖縣七美': '澎湖縣', '澎湖白沙': '澎湖縣',
                  '澎湖縣白沙': '澎湖縣', '澎湖湖西': '澎湖縣', '澎湖縣湖西': '澎湖縣', '澎湖西嶼': '澎湖縣',
                  '澎湖縣西嶼': '澎湖縣', '澎湖馬公': '澎湖縣', '澎湖縣馬公': '澎湖縣', '馬公': '澎湖縣',
                  '金門': '金門縣', '金門金寧': '金門縣', '金門縣金寧': '金門縣', '金門烏坵': '金門縣',
                  '金門縣烏坵': '金門縣', '烏坵': '金門縣', '金門金城': '金門縣', '金門縣金城': '金門縣',
                  '金門金沙': '金門縣', '金門縣金沙': '金門縣', '金門金湖': '金門縣', '金門縣金湖': '金門縣',
                  '金門烈嶼': '金門縣', '金門縣烈嶼': '金門縣', '連江': '連江縣', '連江莒光': '連江縣',
                  '連江縣莒光': '連江縣', '連江北竿': '連江縣', '連江縣北竿': '連江縣', '北竿': '連江縣',
                  '連江南竿': '連江縣', '連江縣南竿': '連江縣', '南竿': '連江縣', '連江東引': '連江縣',
                  '連江縣東引': '連江縣', '東引': '連江縣', '台北': '臺北市', '台北中山': '臺北市',
                  '台北市中山': '臺北市', '台北大同': '臺北市', '台北市大同': '臺北市', '台北中正': '臺北市',
                  '台北市中正': '臺北市', '台北南港': '臺北市', '台北市南港': '臺北市', '台北內湖': '臺北市',
                  '台北市內湖': '臺北市', '台北信義': '臺北市', '台北市信義': '臺北市', '台北大安': '臺北市',
                  '台北市大安': '臺北市', '台北文山': '臺北市', '台北市文山': '臺北市', '台北北投': '臺北市',
                  '台北市北投': '臺北市', '台北萬華': '臺北市', '台北市萬華': '臺北市', '台北松山': '臺北市',
                  '台北市松山': '臺北市', '台北士林': '臺北市', '台北市士林': '臺北市', '台中': '臺中市',
                  '台中南屯': '臺中市', '台中市南屯': '臺中市', '台中龍井': '臺中市', '台中市龍井': '臺中市',
                  '台中太平': '臺中市', '台中市太平': '臺中市', '台中大里': '臺中市', '台中市大里': '臺中市',
                  '台中西屯': '臺中市', '台中市西屯': '臺中市', '台中大肚': '臺中市', '台中市大肚': '臺中市',
                  '台中潭子': '臺中市', '台中市潭子': '臺中市', '台中大安': '臺中市', '台中市大安': '臺中市',
                  '台中后里': '臺中市', '台中市后里': '臺中市', '台中大雅': '臺中市', '台中市大雅': '臺中市',
                  '台中和平': '臺中市', '台中市和平': '臺中市', '台中清水': '臺中市', '台中市清水': '臺中市',
                  '台中北': '臺中市', '台中市北': '臺中市', '台中南': '臺中市', '台中市南': '臺中市',
                  '台中沙鹿': '臺中市', '台中市沙鹿': '臺中市', '台中神岡': '臺中市', '台中市神岡': '臺中市',
                  '台中西': '臺中市', '台中市西': '臺中市', '台中新社': '臺中市', '台中市新社': '臺中市',
                  '台中石岡': '臺中市', '台中市石岡': '臺中市', '台中霧峰': '臺中市', '台中市霧峰': '臺中市',
                  '台中東': '臺中市', '台中市東': '臺中市', '台中中': '臺中市', '台中市中': '臺中市',
                  '台中北屯': '臺中市', '台中市北屯': '臺中市', '台中豐原': '臺中市', '台中市豐原': '臺中市',
                  '台中外埔': '臺中市', '台中市外埔': '臺中市', '台中梧棲': '臺中市', '台中市梧棲': '臺中市',
                  '台中大甲': '臺中市', '台中市大甲': '臺中市', '台中烏日': '臺中市', '台中市烏日': '臺中市',
                  '台中東勢': '臺中市', '台中市東勢': '臺中市', '台南': '臺南市', '台南後壁': '臺南市',
                  '台南市後壁': '臺南市', '台南中西': '臺南市', '台南市中西': '臺南市', '台南下營': '臺南市',
                  '台南市下營': '臺南市', '台南新市': '臺南市', '台南市新市': '臺南市', '台南白河': '臺南市',
                  '台南市白河': '臺南市', '台南仁德': '臺南市', '台南市仁德': '臺南市', '台南南': '臺南市',
                  '台南市南': '臺南市', '台南山上': '臺南市', '台南市山上': '臺南市', '台南大內': '臺南市',
                  '台南市大內': '臺南市', '台南楠西': '臺南市', '台南市楠西': '臺南市', '台南將軍': '臺南市',
                  '台南市將軍': '臺南市', '台南安平': '臺南市', '台南市安平': '臺南市', '台南佳里': '臺南市',
                  '台南市佳里': '臺南市', '台南安南': '臺南市', '台南市安南': '臺南市', '台南南化': '臺南市',
                  '台南市南化': '臺南市', '台南善化': '臺南市', '台南市善化': '臺南市', '台南龍崎': '臺南市',
                  '台南市龍崎': '臺南市', '台南關廟': '臺南市', '台南市關廟': '臺南市', '台南麻豆': '臺南市',
                  '台南市麻豆': '臺南市', '台南安定': '臺南市', '台南市安定': '臺南市', '台南新化': '臺南市',
                  '台南市新化': '臺南市', '台南七股': '臺南市', '台南市七股': '臺南市', '台南北': '臺南市',
                  '台南市北': '臺南市', '台南學甲': '臺南市', '台南市學甲': '臺南市', '台南東山': '臺南市',
                  '台南市東山': '臺南市', '台南柳營': '臺南市', '台南市柳營': '臺南市', '台南玉井': '臺南市',
                  '台南市玉井': '臺南市', '台南東': '臺南市', '台南市東': '臺南市', '台南六甲': '臺南市',
                  '台南市六甲': '臺南市', '台南鹽水': '臺南市', '台南市鹽水': '臺南市', '台南永康': '臺南市',
                  '台南市永康': '臺南市', '台南西港': '臺南市', '台南市西港': '臺南市', '台南官田': '臺南市',
                  '台南市官田': '臺南市', '台南新營': '臺南市', '台南市新營': '臺南市', '台南左鎮': '臺南市',
                  '台南市左鎮': '臺南市', '台南北門': '臺南市', '台南市北門': '臺南市', '台南歸仁': '臺南市',
                  '台南市歸仁': '臺南市', '台東': '臺東縣', '台東延平': '臺東縣', '台東縣延平': '臺東縣',
                  '台東金峰': '臺東縣', '台東縣金峰': '臺東縣', '台東關山': '臺東縣', '台東縣關山': '臺東縣',
                  '台東臺東': '臺東縣', '台東縣臺東': '臺東縣', '台東達仁': '臺東縣', '台東縣達仁': '臺東縣',
                  '台東卑南': '臺東縣', '台東縣卑南': '臺東縣', '台東綠島': '臺東縣', '台東縣綠島': '臺東縣',
                  '台東太麻里': '臺東縣', '台東縣太麻里': '臺東縣', '台東蘭嶼': '臺東縣', '台東縣蘭嶼': '臺東縣',
                  '台東成功': '臺東縣', '台東縣成功': '臺東縣', '台東長濱': '臺東縣', '台東縣長濱': '臺東縣',
                  '台東東河': '臺東縣', '台東縣東河': '臺東縣', '台東鹿野': '臺東縣', '台東縣鹿野': '臺東縣',
                  '台東池上': '臺東縣', '台東縣池上': '臺東縣', '台東海端': '臺東縣', '台東縣海端': '臺東縣',
                  '台東大武': '臺東縣', '台東縣大武': '臺東縣'}
        self.assertEqual(expect, self.tagger.keyword2city)

    def test_tags_from_msg1(self):
        """tags from keyword 雙北"""
        msg = "招募：雙北地區企業臨場服務醫師- 職缺：正職，需職登本醫院；- 醫師證書：1. 具備醫師專科證書（專科不限）；2. 臨場服務受訓合格證書；- 服務範圍：雙北地區；- " \
              "工作時間：排班制，正常工作日，時間靈活；- 工作內容：協助企業執行臨場服務；- 薪資：面談，掛照費+節金；- 其他注意事項：1. 需配合醫院排班；2. 需有交通工具；3. " \
              "需配合醫院關於臨場服務的規範和要求；4. 在提前告知並被允許的情況下，可以兼職支援其他醫療機構；5.無臨場服務經驗，亦可.若有興趣，可電話聯繫徐小姐：02-2577-8660#263."
        expect = {"新北市", "臺北市"}

        self.assertEqual(expect, self.tagger.tags_from_msg(msg))

    def test_tags_from_msg2(self):
        """tags from long msg"""
        msg = "屏東多點/單次/疫苗?(其實公部門是可以找出名目，從3435 加到5000 的🤭🤔👈👈👈👈)與原住民共度聖誕跨年佳節，  " \
              "這職缺貼文要轉念一下，親近大自然的好機會。屏東醫師公會會務人員，轉自轉知衛生局詢問需要找支援醫師，請可以支援醫師填寫姓名於下方空格，謝謝。支援單位@施打地點泰武鄉衛生所@Singlit樂智社區服務據點12" \
              "/23(五)上午0850-1200 (          )1位來義鄉衛生所@南和活動中心12/24(六)上午0850-1200(洪敏榮)1位來義鄉衛生所@望嘉活動中心12/24(" \
              "六)下午1250-1600(         )1位鹽埔鄉衛生所@7-11永盛門市12/24(六)上午0850-1200(          )1位鹽埔鄉衛生所@洛陽村龍虎宮12/24(" \
              "六)下午1250-1600(          )1位春日鄉衛生所@力里集會所12/26(一)上午0850-1200(         )1位春日鄉衛生所@春日集會所12/26(" \
              "一)下午1250-1600(         )1位獅子鄉衛生所@丹路活動中心12/26(一)上午0850-1200(         )1位獅子鄉衛生所@內獅活動中心12/26(" \
              "一)下午1250-1600(          )1位內埔鄉衛生所@和興村活動中心12/28(三)下午1250-1600( 李昭仁 )1位牡丹鄉衛生所@牡丹集會所12/26(一)上午0850-1200(  " \
              "        )1位牡丹鄉衛生所@石門集會所12/26(一)下午1250-1600(       　)1位林邊鄉衛生所@林邊火車站12/27(二)下午1250-1600( " \
              "蘇榮承）1位滿州鄉衛生所@滿州鄉公所對面12/29(一)上午0850-1200(         )1位滿州鄉衛生所@永靖羅峰寺12/29(一)下午1250-1600(         " \
              ")1位竹田鄉衛生所@西勢村辦公處12/29(四)上午0850-1200( 李昭仁 )1位潮州鎮衛生所@尚青黃昏市場12/30(五)下午1250-1600( 李昭仁 " \
              ")1位支援費用：3435元（施打人數超過100人支援費用5000元）"
        expect = {'屏東縣'}

        self.assertEqual(expect, self.tagger.tags_from_msg(msg))

    def test_tags_from_msg3(self):
        """tags from keyword 高屏"""
        msg = "轉po「急」誠徵職業醫學專科醫師掛照高屏地區醫院掛牌費：優聯絡： 0963309077 或吳小姐 0902217168"
        expect = {"屏東縣", "高雄市"}

        self.assertEqual(expect, self.tagger.tags_from_msg(msg))

    def test_tags_from_msg4(self):
        """tags from keyword 桃竹, 竹苗"""
        msg = "桃竹苗地區"
        expect = {"桃園市", "新竹市", "新竹縣", "苗栗縣"}

        self.assertEqual(expect, self.tagger.tags_from_msg(msg))

    def test_tags_from_msg5(self):
        """tags from keyword 內壢"""
        msg = "內壢/專任/不分科(家醫科)"
        expect = {"桃園市"}

        self.assertEqual(expect, self.tagger.tags_from_msg(msg))

    def test_tags_from_msg6(self):
        """tags from keyword 北市"""
        msg = "*北市信義區優質健保診所禮聘：【掛牌負責人醫師】待遇：掛牌費+診費+PPF合作模式可面議請联络：0910100785黃小姐"
        expect = {"臺北市"}

        self.assertEqual(expect, self.tagger.tags_from_msg(msg))

    def test_tags_from_msg_empty(self):
        """tags from keyword 內壢"""
        msg = "以上職缺(部分重複刊登)轉載自5000人/實名制群 👉歡迎雇主自貼 待聘醫師自薦👈"
        expect = set()

        self.assertEqual(expect, self.tagger.tags_from_msg(msg))

    def test_keywords_from_msg1(self):
        """keywords from long msg"""
        msg = "屏東多點/單次/疫苗?(其實公部門是可以找出名目，從3435 加到5000 的🤭🤔👈👈👈👈)與原住民共度聖誕跨年佳節，  " \
              "這職缺貼文要轉念一下，親近大自然的好機會。屏東醫師公會會務人員，轉自轉知衛生局詢問需要找支援醫師，請可以支援醫師填寫姓名於下方空格，謝謝。支援單位@施打地點泰武鄉衛生所@Singlit樂智社區服務據點12" \
              "/23(五)上午0850-1200 (          )1位來義鄉衛生所@南和活動中心12/24(六)上午0850-1200(洪敏榮)1位來義鄉衛生所@望嘉活動中心12/24(" \
              "六)下午1250-1600(         )1位鹽埔鄉衛生所@7-11永盛門市12/24(六)上午0850-1200(          )1位鹽埔鄉衛生所@洛陽村龍虎宮12/24(" \
              "六)下午1250-1600(          )1位春日鄉衛生所@力里集會所12/26(一)上午0850-1200(         )1位春日鄉衛生所@春日集會所12/26(" \
              "一)下午1250-1600(         )1位獅子鄉衛生所@丹路活動中心12/26(一)上午0850-1200(         )1位獅子鄉衛生所@內獅活動中心12/26(" \
              "一)下午1250-1600(          )1位內埔鄉衛生所@和興村活動中心12/28(三)下午1250-1600( 李昭仁 )1位牡丹鄉衛生所@牡丹集會所12/26(一)上午0850-1200(  " \
              "        )1位牡丹鄉衛生所@石門集會所12/26(一)下午1250-1600(       　)1位林邊鄉衛生所@林邊火車站12/27(二)下午1250-1600( " \
              "蘇榮承）1位滿州鄉衛生所@滿州鄉公所對面12/29(一)上午0850-1200(         )1位滿州鄉衛生所@永靖羅峰寺12/29(一)下午1250-1600(         " \
              ")1位竹田鄉衛生所@西勢村辦公處12/29(四)上午0850-1200( 李昭仁 )1位潮州鎮衛生所@尚青黃昏市場12/30(五)下午1250-1600( 李昭仁 " \
              ")1位支援費用：3435元（施打人數超過100人支援費用5000元）"
        expect = {'潮州', '屏東'}
        self.assertEqual(expect, self.tagger.keywords_from_msg(msg))

    def test_keywords_from_msg2(self):
        msg = "禮聘優質醫師桃園，中壢，三峽優質社區診所聯盟，環境佳, 醫師相處互助融洽, 歡迎有衝勁或有經驗的醫師加入團隊，備有完整的基層看診培及入股機會, 培訓完成鼓勵醫師開業或合作經營舊診所或新診所開發, " \
              "讓優質醫師共享創業利潤!科別不拘，家醫科內科復健科尤佳請聯絡03-2550908人資李主任安排各診所院長詳談時間, 期待找到熱情的您，一起跟著診所成長！(轉載 沈將軍 桃園群)"
        expect = {'中壢', '三峽', '桃園'}
        self.assertEqual(expect, self.tagger.keywords_from_msg(msg))

    def test_keywords_from_msg_empty(self):
        msg = "以上職缺(部分重複刊登)轉載自5000人/實名制群 👉歡迎雇主自貼 待聘醫師自薦👈"
        expect = set()
        self.assertEqual(expect, self.tagger.keywords_from_msg(msg))
