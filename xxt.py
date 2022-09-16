import httpx

from Util import *
from API import *
from Analysis import Analysis_data
from config import *

class Xxt(Analysis_data):
    def __init__(self, uname:str, pwd:str):
        self.client = httpx.Client(headers=get_headers())
        self.uname = uname
        self.pwd = DES_encode(pwd)
        self.vcode = identify_vcode(self)
        self.auto_login()

    def auto_login(self):
        """ 尝试使用cookie登录 """
        datas = load_data(self.uname)
        self.client.headers['cookies'] = ''
        for data in datas["cookies"]:  # type: ignore
            self.client.cookies.set(list(data.keys())[0],list(data.values())[0])
        try:
            self.info()
        except:
            self.login() 

    def login(self):
        """ 登录 """
        data = s_login_data(self.uname, self.pwd, self.vcode)
        d = self.client.post(LOGIN_URL_01, data=data).json()["type"]
        replenish_cookie(self)   
        match str(d):
            case "0":
                print("--------登录成功--------")
                self.info()
                dump_data(self.uname, self.pwd, self)
            case _:
                print("请检查账号密码后重试")


    def info(self):
        """ 打印信息 """
        r = self.client.get(INFO_URL)
        with open("1.html", "w", encoding="utf8") as f:
            print(r.text, file=f)
        Analysis_data.__init__(self, r.text)
        print(f"姓名:", self.Get_name())
        print(f"性别:", self.Get_gender())
        print(f"账号:", self.Get_id())
        print(f"学号:", self.Get_sId())
        print(f"电话:", self.Get_num())
        print("\n")

    def get_notice(self):
        r = self.client.post(NOTICE_URL, data={'type':'2',
            'notice_type':'',
            'lastValue':'',
            'sort':'',
            'folderUUID':'',
            'kw':'',
            'startTime':'',
            'endTime':'',
            'gKw':'',
            'gName':''	,
            'year':'2022'
        })
        res = r.json()
        from json import dump
        with open("data.json", 'w', encoding="utf8") as f:
            dump(res, f, indent=4, ensure_ascii=False)
        res = res["notices"]["list"]
        for data in res:
            print(data["completeTime"]+"\n")
            print(data["content"].replace("\r", "\n"))
            print("-"*60)

if __name__ == "__main__":
    My_Xxt = Xxt("账号", "密码")
    My_Xxt.get_notice()