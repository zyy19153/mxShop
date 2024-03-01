import requests
import json


class YunPian(object):
    # 初始化函数
    def __init__(self, api_key):
        self.api_key = api_key  # 实例化api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"  # 从云片文档中拷贝这个url，单条发送接口

    # 定义send_sms接口
    def send_sms(self, code, mobile):
        params = {
            "api_key": self.api_key,
            "mobile": mobile,
            # text内容一定要按照云片网站里申请的模板的格式来写，格式错误会发送失败，
            "text": "[慕学生鲜] 您的验证码是{code},如非本人操作,请忽略本短信.".format(code=code),
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == "__main__":
    yunpian = YunPian("xxxxx")   # xxxxx表示注册的云片网账户的APIKEY，复制过来
    yunpian.send_sms("2017", "13137007911")  # （code，mobile）
