import random
import unittest
from time import sleep

import requests
import logging

from api.loginAPI import loginAPI
from utils import assert_utils


class login(unittest.TestCase):
    phone1="15340812345"
    phone2 = "15340812346"
    phone3 = "15340812347"
    phone4 = "15340812348"
    phone5 = "15340812349"
    imgVerifyCode="8888"
    password="123456"
    phone_code="666666"


    def setUp(self):
        self.loginapi=loginAPI()   #实例化登录api接口
        self.session=requests.session()  #创建session

    def tearDown(self):
        if self.session:
            self.session.close()

        #1. 获取图片验证码成功-随机小数
    def test01_getimgCode_random_float(self):
        #定义参数（随机小数）
        r=random.random()
        #调用接口类中的接口
        response=self.loginapi.getimgCode(self.session,str(r))
        self.assertEqual(200,response.status_code)

        #2. 获取图片验证码成功-随机整数
    def test02_getimgCode_random_int(self):
        # 定义参数（随机整数）
        r=random.randint(1,100)
        response=self.loginapi.getimgCode(self.session,str(r))
        self.assertEqual(200,response.status_code)

        #3. 获取图片验证码失败-随机数为空
    def test03_getimgCode_random_null(self):
        # 定义参数（随机数为空）
        r=[]
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(400, response.status_code)

        #4. 获取图片验证码失败-随机数为字符串
    def test04_getimgCode_random_str(self):
        # 定义参数（随机数为字符串）
        r = random.sample("abcdefghigklmn",5)  #返回的是一个list
        rand="".join(r)   #使用拼接
        logging.info(rand)
        response = self.loginapi.getimgCode(self.session, rand)
        self.assertEqual(400, response.status_code)

        #5. 获取短信验证码成功-参数正确
    def test05_getphoneCode_success(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码成功-参数正确
        # 定义正确参数
        # 调用短信验证码接口
        response=self.loginapi.getphoneCode(self.session,self.phone1,self.imgVerifyCode)
        # 对收到得响应进行断言
        assert_utils(self,response,200,200,"短信发送成功")

        #6. 获取注册短信验证码失败-图片验证码错误
    def test06_getphoneCode_wrong_imgCode_wrong(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码失败（手机号正确，验证码错误）
        response = self.loginapi.getphoneCode(self.session, self.phone1, 8889)
        assert_utils(self,response,200,100,"图片验证码错误")

        #7. 获取注册短信验证码失败-手机号为空
    def test07_getphoneCode_wrong_phone_null(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码失败（手机号为空，验证码正确）
        response=self.loginapi.getphoneCode(self.session,"",self.imgVerifyCode)
        logging.info("get phone code response={}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))

        #8.获取注册短信验证码失败-图片验证码为空
    def test08_getphoneCode_wrong_imgCode_null(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码失败（图片验证码为空）
        response=self.loginapi.getphoneCode(self.session,self.phone1,"")
        assert_utils(self,response,200,100,"图片验证码错误")

        #9. 获取注册短信验证码失败-未调用获取图片验证码接口
    def test09_getphoneCode_wrong_imgCode_not_use(self):
        response=self.loginapi.getphoneCode(self.session,self.phone1,self.imgVerifyCode)
        logging.info("get phone code response={}".format(response.json()))
        assert_utils(self,response,200,100,"图片验证码错误")

        #10. 注册成功-必填参数
    def test10_register_success_must_print(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码成功-参数正确
        # 定义正确参数
        # 调用短信验证码接口
        response = self.loginapi.getphoneCode(self.session, self.phone1, self.imgVerifyCode)
        logging.info("get phone code response = {}".format(response.json()))
        # 对收到得响应进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.必填参数正确，注册成功
        response=self.loginapi.register(self.session,self.phone1,self.password)
        logging.info("register response = {}".format(response.json()))
        assert_utils(self,response,200,200,"注册成功")

        # 11. 注册成功-全部参数
    def test11_register_success_params(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码成功-参数正确
        # 定义正确参数
        # 调用短信验证码接口
        response = self.loginapi.getphoneCode(self.session, self.phone2, self.imgVerifyCode)
        logging.info("get phone code response = {}".format(response.json()))
        # 对收到得响应进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册成功-全部参数
        response=self.loginapi.register(self.session,self.phone2,self.password,invite_phone="15340803743")
        logging.info("register response = {}".format(response.json()))
        assert_utils(self,response,200,200,"注册成功")

        #12. 注册失败 - 图片验证码错误
    def test12_register_fail_imgCode_wrong(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码成功-参数正确
        # 定义正确参数
        # 调用短信验证码接口
        response = self.loginapi.getphoneCode(self.session, self.phone2, self.imgVerifyCode)
        logging.info("get phone code response = {}".format(response.json()))
        # 对收到得响应进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败-图片验证码错误
        response=self.loginapi.register(self.session,self.phone2,self.password,imgVerifyCode="wrong_code")
        logging.info("register response={}".format(response.json()))
        assert_utils(self,response,200,100,"验证码错误!")

        #13. 注册失败 - 短信验证码错误
    def test13_register_fail_phoneCode_wrong(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码成功-参数正确
        # 定义正确参数
        # 调用短信验证码接口
        response = self.loginapi.getphoneCode(self.session, self.phone3, self.imgVerifyCode)
        logging.info("get phone code response = {}".format(response.json()))
        # 对收到得响应进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败 - 短信验证码错误
        response=self.loginapi.register(self.session,self.phone3,self.password,phone_code="456456")
        logging.info("get register code response = {}".format(response.json()))
        assert_utils(self,response,200,100,"验证码错误")

        # 14. 注册失败 - 手机已存在
    def test14_register_fail_phone_exist(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码成功-参数正确
        # 定义正确参数
        # 调用短信验证码接口
        response = self.loginapi.getphoneCode(self.session, self.phone2, self.imgVerifyCode)
        logging.info("get phone code response = {}".format(response.json()))
        # 对收到得响应进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败 - 手机已存在
        response=self.loginapi.register(self.session,self.phone2,self.password)
        logging.info("get phone code response = {}".format(response.json()))
        assert_utils(self,response,200,100,"手机已存在!")

        # 15.注册失败-密码为空
    def test15_register_pwd_null(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码成功-参数正确
        # 定义正确参数
        # 调用短信验证码接口
        response = self.loginapi.getphoneCode(self.session, self.phone4, self.imgVerifyCode)
        logging.info("get phone code response = {}".format(response.json()))
        # 对收到得响应进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败-密码为空
        response=self.loginapi.register(self.session,self.phone4,password="")
        logging.info("register response={}".format(response.json()))
        assert_utils(self,response,200,100,"密码不能为空")

        # 16.注册失败-未同意条款
    def test16_register_disagree(self):
        # 1.获取图片验证码成功（随机数为小数）
        r = random.random()
        response = self.loginapi.getimgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码成功-参数正确
        # 定义正确参数
        # 调用短信验证码接口
        response = self.loginapi.getphoneCode(self.session, self.phone5, self.imgVerifyCode)
        logging.info("get phone code response = {}".format(response.json()))
        # 对收到得响应进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3.注册失败-未同意条款
        response=self.loginapi.register(self.session,self.phone5,self.password,dy_server="off")
        logging.info("register response={}".format(response.json()))
        assert_utils(self,response,200,100,"请同意我们的条款")

         #17.登录成功
    def test17_login_success(self):
        response=self.loginapi.login(self.session,self.phone1,self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")

        #18.登录失败-用户不存在
    def test18_login_fail_user_exist(self):
        wrong_phone="12345652222"
        response=self.loginapi.login(self.session,wrong_phone,self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self,response,200,100,"用户不存在")

        #19.登录失败-密码为空
    def test19_login_fail_pwd_null(self):
        # 定义参数
        pwd=""
        response=self.loginapi.login(self.session,self.phone1,pwd)
        logging.info("login response={}".format(response.json()))
        assert_utils(self,response,200,100,"密码不能为空")

        #20.登录失败-输入密码错误（1-3次）
    def test20_login_fail_pwd_wrong(self):
        pwd="123"
        # 1.输入错误密码，提示错误1次
        response=self.loginapi.login(self.session,self.phone1,pwd)
        logging.info("login response={}".format(response.json()))
        assert_utils(self,response,200,100,"密码错误1次,达到3次将锁定账户")
        # 2.输入错误密码，提示错误2次
        response = self.loginapi.login(self.session, self.phone1, pwd)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        # 3.输入错误密码，提示错误3次，锁定账户
        response = self.loginapi.login(self.session, self.phone1, pwd)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        # 4.输入正确密码及手机号，依旧锁定
        response = self.loginapi.login(self.session, self.phone1, self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        # 5.过了60s，重新输入正确密码手机号，登录成功
        sleep(60)
        response = self.loginapi.login(self.session, self.phone1, self.password)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")