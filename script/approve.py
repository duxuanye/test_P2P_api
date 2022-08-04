import logging
import unittest

import requests

from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from utils import assert_utils


class approve(unittest.TestCase):
    realname="胡明良"
    card_id="371521198710123153"
    phone1="15340812345"
    phone2 = "15340812346"
    password= "123456"
    def setUp(self):
        self.session=requests.Session()
        self.approveapi=approveAPI()
        self.loginapi=loginAPI()
    def tearDown(self):
        if self.session:
            self.session.close()
        #认证成功
    def test01_approve_success(self):
        # 1.登录
        response=self.loginapi.login(self.session,self.phone1,self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        # 2. 认证成功
        response=self.approveapi.approve(self.session,self.realname,self.card_id)
        logging.info("approve response={}".format(response.json()))
        assert_utils(self,response,200,200,"提交成功!")
        #认证失败-姓名为空
    def test02_approve_fail_name_null(self):
        # 1.登录
        response = self.loginapi.login(self.session, self.phone2, self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2.认证失败-姓名为空
        realname = ""
        response=self.approveapi.approve(self.session,realname,self.card_id)
        logging.info("approve response={}".format(response.json()))
        assert_utils(self,response,200,100,"姓名不能为空")

        # 认证失败-身份证为空
    def test03_approve_fail__null(self):
        # 1.登录
        response = self.loginapi.login(self.session, self.phone2, self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2.认证失败-身份证为空
        card_id=""
        response=self.approveapi.approve(self.session,self.realname,card_id)
        logging.info("approve response={}".format(response.json()))
        assert_utils(self,response,200,100,"身份证号不能为空")

    # 认证查询 - 已认证
    def test04_get_approve_ok(self):
        # 1.登录
        response = self.loginapi.login(self.session, self.phone1, self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2.认证查询-已认证
        response=self.approveapi.getapprove(self.session)
        logging.info("getapprove response={}".format(response.json()))
        self.assertEqual(200,response.status_code)

    # 认证查询 - 未认证
    def test05_get_approve_no(self):
        # 1.登录
        response = self.loginapi.login(self.session, self.phone2, self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2.认证查询-未认证
        response = self.approveapi.getapprove(self.session)
        logging.info("getapprove response={}".format(response.json()))
        self.assertEqual(200, response.status_code)
