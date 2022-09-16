from ddddocr import DdddOcr
from execjs import compile

from API import *

def get_headers():
    headers:dict[str,str] = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Host": "www.fanya.chaoxing.com",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://i.mooc.chaoxing.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

def getTime():
    cxt = compile(""" function a() {
        return new Date().getTime()
    } """)
    return cxt.call("a")

def identify_vcode(x) -> str:
        """ 获取网页验证码并使用 ddddocr 识别验证码 """
        vcode = x.client.get(f"{NUM_CODE}?{getTime()}")
        ocr = DdddOcr(show_ad=False)
        return ocr.classification(vcode.content)

def s_login_data(uname:str, pwd:str, numcode:str) -> dict[str,str]:
        """ 构造登录所需的data字典 """
        data:dict[str,str] = {
            "fid": "1665",
            "uname": "",
            "numcode": "",
            "password": "",
            "refer": "http%3A%2F%2Fzjgsu.fanya.chaoxing.com",
            "t": "true",
            "hidecompletephone": "0",
            "doubleFactorLogin": "0"
        }
        data["uname"] = uname
        data["numcode"] = numcode
        data["password"] = pwd
        return data

def DES_encode(pwd:str) -> str:
        """ 将密码使用DES算法加密 """
        with open("DES_E.js", "r") as f:
            js_code:str = f.read()
        ctx = compile(js_code)
        return ctx.call("DES_Encrypt", pwd)

def replenish_cookie(x):
    """ 补全cookie """
    for i in range(2, 8):
        eval(f"x.client.get(LOGIN_URL_0{i})")
    x.client.get(LOGIN_GERJ_URL)

def enroll(r):
    return r.json()["mes"]