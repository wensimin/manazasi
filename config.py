import json


def loadConfig():
    """加载json格式配置"""
    with open("config.json", "r+", encoding='utf8') as f:
        c = json.loads(f.read())
        return c


def saveConfig(c):
    """保存配置信息至文件"""
    with open("config.json", "w", encoding='utf8') as f:
        f.write(json.dumps(c))

