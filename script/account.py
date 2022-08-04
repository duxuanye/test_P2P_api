import random
import unittest
from bs4 import BeautifulSoup
import requests,logging

from api.loginAPI import loginAPI
from api.accountAPI import accountAPI
from utils import assert_utils, request_third_api


class account(unittest.TestCase):
    phone1 = "15340812345"
    password = "123456"

    def setUp(self):
        self.session=requests.Session()
        self.loginapi=loginAPI()
        self.accountapi=accountAPI()

    def tearDown(self):
        self.session.close()

    # 开户请求
    def test01_trust_success(self):
        # 1.认证通过得账户进行登录
        response=self.loginapi.login(self.session,self.phone1,self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        # 2.发送开户请求
        response=self.accountapi.account(self.session)
        logging.info("account response={}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        # 3.发送第三方得开户请求
        form_data=response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 调用第三方接口请求方法
        response=request_third_api(form_data)
        self.assertEqual(200,response.status_code)
        self.assertEqual("UserRegister OK",response.text)

        # 充值
    def test02_recharge(self):
        # 1.认证通过得账户进行登录
        response = self.loginapi.login(self.session, self.phone1, self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2.获取充值图片验证码-随机小数
        r = random.random()
        response = self.accountapi.get_recharge_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 3.发送充值请求
        response=self.accountapi.recharge(self.session)
        logging.info("recharge response={}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 4.发送第三方充值
            # 1.首先获取form表单中得数据，并提取为后续得第三方请求得参数
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
            # 2.调用第三方请求接口
        response=request_third_api(form_data)
            # 3.断言response是否正确
        self.assertEqual(200,response.status_code)
        self.assertEqual("NetSave OK",response.text)