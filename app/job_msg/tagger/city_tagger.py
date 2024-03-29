from collections import Counter

from app.job_msg.schema import JobMsgDebugResponse
from app.job_msg.tagger.city import City


class CityTagger:
    def __init__(self, special_keyword2cities: dict[str:set[City]] = None, distinct_districts: set[str] = None):
        """Tagger to extract Taiwan cities from the message
        Args:
            special_keyword2cities: 特殊關鍵字 to 城市清單 e.g. "北北基桃": {"臺北市", "新北市", "基隆市", "桃園市"}
            distinct_districts: 鄉鎮市區去掉最後一字，且其名稱必須明確是行政區，不會與街道、常用詞混淆
        """
        city2dist = {
            City.TAIPEI: {
                '中正區', '大同區', '中山區', '萬華區', '信義區', '松山區', '大安區', '南港區', '北投區', '內湖區',
                '士林區', '文山區'
            },
            City.NEW_TAIPEI: {
                '板橋區', '新莊區', '泰山區', '林口區', '淡水區', '金山區', '八里區', '萬里區', '石門區', '三芝區',
                '瑞芳區', '汐止區', '平溪區', '貢寮區', '雙溪區', '深坑區', '石碇區', '新店區', '坪林區', '烏來區',
                '中和區', '永和區', '土城區', '三峽區', '樹林區', '鶯歌區', '三重區', '蘆洲區', '五股區'
            },
            City.KEELUNG: {'仁愛區', '中正區', '信義區', '中山區', '安樂區', '暖暖區', '七堵區'},
            City.TAOYUAN: {
                '桃園區', '中壢區', '平鎮區', '八德區', '楊梅區', '蘆竹區', '龜山區', '龍潭區', '大溪區',
                '大園區', '觀音區', '新屋區', '復興區'
            },
            City.HSINCHU_COUNTY: {
                '竹北市', '竹東鎮', '新埔鎮', '關西鎮', '峨眉鄉', '寶山鄉', '北埔鄉', '橫山鄉', '芎林鄉',
                '湖口鄉', '新豐鄉', '尖石鄉', '五峰鄉'
            },
            City.HSINCHU_CITY: {'東區', '北區', '香山區'},
            City.MIAOLI: {
                '苗栗市', '通霄鎮', '苑裡鎮', '竹南鎮', '頭份鎮', '後龍鎮', '卓蘭鎮', '西湖鄉', '頭屋鄉',
                '公館鄉', '銅鑼鄉', '三義鄉', '造橋鄉', '三灣鄉', '南庄鄉', '大湖鄉', '獅潭鄉', '泰安鄉'
            },
            City.TAICHUNG: {
                '中區', '東區', '南區', '西區', '北區', '北屯區', '西屯區', '南屯區', '太平區', '大里區',
                '霧峰區', '烏日區', '豐原區', '后里區', '東勢區', '石岡區', '新社區', '和平區', '神岡區',
                '潭子區', '大雅區', '大肚區', '龍井區', '沙鹿區', '梧棲區', '清水區', '大甲區', '外埔區',
                '大安區'
            },
            City.NANTOU: {
                '南投市', '埔里鎮', '草屯鎮', '竹山鎮', '集集鎮', '名間鄉', '鹿谷鄉', '中寮鄉', '魚池鄉',
                '國姓鄉', '水里鄉', '信義鄉', '仁愛鄉'
            },
            City.CHANGHUA: {
                '彰化市', '員林鎮', '和美鎮', '鹿港鎮', '溪湖鎮', '二林鎮', '田中鎮', '北斗鎮', '花壇鄉',
                '芬園鄉', '大村鄉', '永靖鄉', '伸港鄉', '線西鄉', '福興鄉', '秀水鄉', '埔心鄉', '埔鹽鄉',
                '大城鄉', '芳苑鄉', '竹塘鄉', '社頭鄉', '二水鄉', '田尾鄉', '埤頭鄉', '溪州鄉'
            },
            City.YUNLIN: {
                '斗六市', '斗南鎮', '虎尾鎮', '西螺鎮', '土庫鎮', '北港鎮', '莿桐鄉', '林內鄉', '古坑鄉',
                '大埤鄉', '崙背鄉', '二崙鄉', '麥寮鄉', '臺西鄉', '東勢鄉', '褒忠鄉', '四湖鄉', '口湖鄉',
                '水林鄉', '元長鄉'
            },
            City.CHIAYI_COUNTY: {
                '太保市', '朴子市', '布袋鎮', '大林鎮', '民雄鄉', '溪口鄉', '新港鄉', '六腳鄉', '東石鄉',
                '義竹鄉', '鹿草鄉', '水上鄉', '中埔鄉', '竹崎鄉', '梅山鄉', '番路鄉', '大埔鄉', '阿里山鄉'
            },
            City.CHIAYI_CITY: {'東區', '西區'},
            City.TAINAN: {
                '中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區', '左鎮區',
                '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區',
                '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區',
                '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區', '安定區'
            },
            City.KAOHSIUNG: {
                '楠梓區', '左營區', '鼓山區', '三民區', '鹽埕區', '前金區', '新興區', '苓雅區', '前鎮區',
                '小港區', '旗津區', '鳳山區', '大寮區', '鳥松區', '林園區', '仁武區', '大樹區', '大社區',
                '岡山區', '路竹區', '橋頭區', '梓官區', '彌陀區', '永安區', '燕巢區', '田寮區', '阿蓮區',
                '茄萣區', '湖內區', '旗山區', '美濃區', '內門區', '杉林區', '甲仙區', '六龜區', '茂林區',
                '桃源區', '那瑪夏區'
            },
            City.PINGTUNG: {
                '屏東市', '潮州鎮', '東港鎮', '恆春鎮', '萬丹鄉', '長治鄉', '麟洛鄉', '九如鄉', '里港鄉',
                '鹽埔鄉', '高樹鄉', '萬巒鄉', '內埔鄉', '竹田鄉', '新埤鄉', '枋寮鄉', '新園鄉', '崁頂鄉',
                '林邊鄉', '南州鄉', '佳冬鄉', '琉球鄉', '車城鄉', '滿州鄉', '枋山鄉', '霧台鄉', '瑪家鄉',
                '泰武鄉', '來義鄉', '春日鄉', '獅子鄉', '牡丹鄉', '三地門鄉'
            },
            City.YILAN: {
                '宜蘭市', '羅東鎮', '蘇澳鎮', '頭城鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '冬山鄉', '五結鄉',
                '三星鄉', '大同鄉', '南澳鄉'
            },
            City.HUALIEN: {
                '花蓮市', '鳳林鎮', '玉里鎮', '新城鄉', '吉安鄉', '壽豐鄉', '秀林鄉', '光復鄉', '豐濱鄉',
                '瑞穗鄉', '萬榮鄉', '富里鄉', '卓溪鄉'
            },
            City.TAITUNG: {
                '臺東市', '成功鎮', '關山鎮', '長濱鄉', '海端鄉', '池上鄉', '東河鄉', '鹿野鄉', '延平鄉',
                '卑南鄉', '金峰鄉', '大武鄉', '達仁鄉', '綠島鄉', '蘭嶼鄉', '太麻里鄉'
            },
            City.PENGHU: {'馬公市', '湖西鄉', '白沙鄉', '西嶼鄉', '望安鄉', '七美鄉'},
            City.KINMEN: {'金城鎮', '金湖鎮', '金沙鎮', '金寧鄉', '烈嶼鄉', '烏坵鄉'},
            City.LIENCHIANG: {'南竿鄉', '北竿鄉', '莒光鄉', '東引鄉'}
        }
        if not special_keyword2cities:
            special_keyword2cities = {
                "北北基桃": {City.TAIPEI, City.NEW_TAIPEI, City.KEELUNG, City.TAOYUAN},
                "北北基": {City.TAIPEI, City.NEW_TAIPEI, City.KEELUNG},
                "雙北桃": {City.TAIPEI, City.NEW_TAIPEI, City.TAOYUAN},
                "雙北": {City.TAIPEI, City.NEW_TAIPEI},
                "双北": {City.TAIPEI, City.NEW_TAIPEI},
                "桃竹": {City.TAOYUAN, City.HSINCHU_COUNTY, City.HSINCHU_CITY},
                "竹苗": {City.HSINCHU_COUNTY, City.HSINCHU_CITY, City.MIAOLI},
                "雲嘉": {City.YUNLIN, City.CHIAYI_COUNTY, City.CHIAYI_CITY},
                "嘉南": {City.CHIAYI_COUNTY, City.CHIAYI_CITY, City.TAINAN},
                "高屏": {City.KAOHSIUNG, City.PINGTUNG},
                "花東": {City.HUALIEN, City.TAITUNG},
                "內壢": {City.TAOYUAN},
                "北市": {City.TAIPEI}
            }
        self.special_keyword2cities = special_keyword2cities
        self.keyword2city = {}
        """關鍵字 to 城市清單 e.g. {'臺北': '臺北市', '臺北中山': '臺北市', '臺北市中山': '臺北市'}"""
        counter = Counter()
        for city, districts in city2dist.items():
            for dist in districts:
                counter[dist] += 1
        if not distinct_districts:
            distinct_districts = {"萬華", "南港", "北投", "內湖", "烏來", "深坑", "三峽", "土城", "三重", "汐止",
                                  "板橋", "平溪", "新店", "瑞芳", "貢寮", "石碇", "鶯歌", "林口", "蘆洲", "新莊",
                                  "七堵", "蘆竹", "大園", "中壢", "平鎮", "楊梅", "龍潭", "竹東", "湖口", "竹北",
                                  "竹南", "南庄", "烏日", "大甲", "豐原", "神岡", "沙鹿", "后里", "石岡", "集集",
                                  "草屯", "埔里", "鹿港", "斗南", "土庫", "麥寮", "虎尾", "西螺", "北港", "古坑",
                                  "斗六", "官田", "歸仁", "新營", "左營", "鳳山", "苓雅", "楠梓", "旗津", "美濃",
                                  "橋頭", "潮州", "恆春", "琉球", "三地門", "東港", "枋寮", "礁溪", "蘇澳", "玉里",
                                  "瑞穗", "蘭嶼", "綠島", "太麻里", "馬公", "烏坵", "北竿", "東引", "南竿"}
        distinct_districts.union({k_ for k_, v_ in counter.items() if v_ == 1})

        for city, districts in city2dist.items():
            self.keyword2city[city.value] = city  # 新竹縣:新竹縣
            self.keyword2city[city.value[:-1]] = city  # 臺北:臺北市
            for dist in districts:
                self.keyword2city[city.value[:-1] + dist[:-1]] = city  # 臺北中正:臺北市
                self.keyword2city[city.value + dist[:-1]] = city  # 臺北市中正:臺北市
                # 僅獨特的鄉政市區名可以作為key，否則只講中正區，不能確定是台北市的中正區
                if dist[:-1] in distinct_districts:
                    self.keyword2city[dist[:-1]] = city  # 板橋:新北市
                elif dist in distinct_districts:
                    self.keyword2city[dist] = city  # 成功鎮:臺東縣

        alias_dict = {}
        for keyword, city in self.keyword2city.items():
            if keyword[0] == "臺":
                alias = "台" + keyword[1:]
                alias_dict[alias] = city
        self.keyword2city.update(alias_dict)

    def debug(self, response: JobMsgDebugResponse) -> None:
        for k, cities in self.special_keyword2cities.items():
            if k in response.raw_msg:
                response.keyword_to_cites[k] = cities
        for k, city in self.keyword2city.items():
            if k in response.raw_msg:
                response.keyword_to_cites[k] = {city}
        response.city_tags = self.tags_from_msg(response.raw_msg)

    def tags_from_msg(self, msg: str) -> set[City]:
        tags = set()
        if not msg:
            return tags
        for k, cities in self.special_keyword2cities.items():
            if k in msg:
                tags.update(cities)
        for k, city in self.keyword2city.items():
            if k in msg:
                tags.add(city)
        return tags


city_tagger = CityTagger()
