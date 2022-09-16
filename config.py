import os

from yaml import load, dump, FullLoader, SafeDumper

CONFIG_PATH = os.path.join(os.getcwd(), "config")
CONFIGES = os.listdir(CONFIG_PATH)

def s_data(uname:str, pwd:str, x):
    """ 构造需要保存的数据 """
    data = {}
    data["uname"] = uname
    data["pwd"] = pwd
    data["cookies"]= []
    for cookie in list(x.client.cookies.jar):
        data["cookies"].append({cookie.name: cookie.value})
    return data

def dump_data(uname:str, pwd:str, x) -> None:
    """ 保存cookie等信息 """
    if uname not in CONFIGES:
        os.chdir("config")
        os.mkdir(uname)
        os.chdir("../")
    u_path = os.path.join(CONFIG_PATH, uname, f"{uname}_config.yml")
    data = s_data(uname, pwd, x)
    with open(u_path, "w") as f:
        dump(data, f, SafeDumper)

def load_data(uname:str):
    """ 读取cookie等信息 """
    if uname not in CONFIGES:
        return False
    u_path = os.path.join(CONFIG_PATH, uname, f"{uname}_config.yml")
    with open(u_path, "r") as f:
        data = f.read()
    data = load(data, Loader=FullLoader)
    return data