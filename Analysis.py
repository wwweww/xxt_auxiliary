from re import findall
from lxml import etree



class Analysis_data:

    def __init__(self, html) -> None:
        self.html:str = html
        self.xpath:str

    def __a_data(self):
        html = etree.HTML(self.html) # type:ignore
        res = html.xpath(self.xpath)
        return res[0]

    def Get_id(self):
        self.xpath = "//*[@id=\"uid\"]/text()"
        return self.__a_data()

    def Get_num(self):
        self.xpath = "//*[@id=\"messagePhone\"]/text()"
        return self.__a_data()

    def Get_sId(self):
        self.xpath = "//p[@class=\"xuehao\"]/text()"
        return self.__a_data()[6:]

    def Get_name(self):
        self.xpath = "//p[@id=\"messageName\"]/text()"
        return self.__a_data()

    def Get_gender(self):
        res = findall("<span><i class=\"check checked\" value=\"1\"></i>(.*?)</span>", self.html)[0]
        return res