import app

#定义接口类
class loginAPI():
    #初始化
    def __init__(self):
        self.getimgCode_url = app.BASE_URL + "/common/public/verifycode1/"
        self.getphoneCode_url=app.BASE_URL +"/member/public/sendSms"
        self.register_url=app.BASE_URL+"/member/public/reg"
        self.login_url=app.BASE_URL+"/member/public/login"
    #获取图片验证码接口
    def getimgCode(self,session,r):
        # 准备参数
        url=self.getimgCode_url+r
        # 发送请求
        response=session.get(url)
        # 返回响应
        return response

    # 获取短信验证码接口
    def getphoneCode(self,session,phone1,imgVerifyCode):
        # 准备参数
        url=self.getphoneCode_url
        data = {'phone':phone1,'imgVerifyCode': imgVerifyCode ,'type':"reg"}
        # 发送请求
        response=session.post(url=url,data=data)
        # 返回响应
        return response

    # 注册接口
    def register(self,session, phone, password,imgVerifyCode="8888",phone_code="666666",dy_server="on",invite_phone=""):
        data={"phone":phone,
            "password":password,
            "verifycode":imgVerifyCode,
            "phone_code":phone_code,
            "dy_server":dy_server,
            "invite_phone":invite_phone}
        response=session.post(url=self.register_url,data=data)
        return response

    # 登录接口
    def login(self,session,phone,password):
        data={"keywords":phone,
            "password":password}
        response=session.post(url=self.login_url,data=data)
        return response

