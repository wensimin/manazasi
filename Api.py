import requests
import time
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import json
import config


# 进行ocr的请求
def ocrRequest(url, params):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=params, headers=headers)
    res = response.json()
    return res


class Api:
    def __init__(self, fileConfig):
        self.expires = 0
        self.token = None
        # 高精度ocr接口是否超限 ,生命周期单次启动内
        self.ocrLimitReached = False
        self.config = fileConfig

    # 获取token
    # 没有持久化token 目前只在一次运行中保证token的复用
    def getBaiduToken(self):
        nowTime = int(time.time())
        if nowTime > self.expires and self.token:
            return self.token
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        clientId = self.config["baiduId"]
        clientSecret = self.config["baiduKey"]
        tokenHost = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + clientId + "&client_secret=" + clientSecret
        response = requests.post(tokenHost)
        res = response.json()
        error = res.get("error")
        # 请求错误的处理
        if error:
            raise Exception(res.get("error_description"))
        # 60 为偏差值
        self.expires = res.get("expires_in") + nowTime - 60
        self.token = res.get("access_token")
        return self.token

    # ocr 接口,从图片转化成文字
    def image2text(self, image):
        imageBase = base64.b64encode(image)
        params = {
            "image": imageBase,
            "language_type": "JAP"
        }
        # 多行合并
        words = self.accurateOcr(params)
        wordString = ""
        for word in words:
            wordString += word.get("words")
        return wordString

    # 基础ocr
    def generalOcr(self, params):
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + self.getBaiduToken()
        res = ocrRequest(url, params)
        error = res.get("error_code")
        # 请求错误的处理
        if error:
            raise Exception(res.get("error_msg"))
        return res.get("words_result")

    # 高精度ocr
    def accurateOcr(self, params):
        if self.ocrLimitReached:
            return self.generalOcr(params)
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + self.getBaiduToken()
        res = ocrRequest(url, params)
        error = res.get("error_code")
        if error in [17, 18, 19]:
            self.ocrLimitReached = True
            return self.generalOcr(params)
        return res.get("words_result")

    # 翻译api 使用腾讯sdk
    def translate(self, text):
        try:
            cred = credential.Credential(self.config["tencentId"], self.config["tencentKey"])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)
            req = models.TextTranslateRequest()
            params = {
                "SourceText": text,
                "Source": "auto",
                "Target": "zh",
                "ProjectId": 0

            }
            req.from_json_string(json.dumps(params))
            resp = client.TextTranslate(req)
            res = json.loads(resp.to_json_string())
            return res.get("TargetText")
        except TencentCloudSDKException as err:
            raise Exception(err)


