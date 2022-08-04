import logging
import random
import unittest

import requests

from api.loginAPI import loginAPI
from api.tenderAPI import tenderAPI
from utils import assert_utils, request_third_api


class tender(unittest.TestCase):
    status="tender"
    id="56"
    amount=1000
    def setUp(self) -> None:
        self.tenderapi=tenderAPI()
        self.session=requests.Session()
        self.loginapi=loginAPI()
        r = random.random()
        # 调用接口类中的接口
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
    def tearDown(self) -> None:
        if self.session:
            self.session.close()
        #获取投资详情信息
    def test01_get_loaninfo(self):
        response=self.tenderapi.loaninfo(self.session,self.id)
        logging.info("get_loaninfo response = {}".format(response.json()))
        assert_utils(self,response,200,200,"OK")
        self.assertEqual("56",response.json().get("data").get("loan_info").get("id"))
        #投资
    def test02_tender(self):
        response=self.tenderapi.tender(self.session,self.id,self.amount)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 调用第三方开户请求
        response=request_third_api(form_data)
        self.assertEqual('InitiativeTender OK', response.text)
        #获取我的投资列表
    def test03_get_tenderlist(self):
        response=self.tenderapi.get_tenderlist(self.session,self.status)
        logging.info("get_tender response = {}".format(response.json()))
        self.assertEqual(200,response.status_code)
