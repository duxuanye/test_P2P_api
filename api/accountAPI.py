import app


class accountAPI():
    def __init__(self):
        self.account_url=app.BASE_URL+"/trust/trust/register"
        self.recharge_url = app.BASE_URL + '/trust/trust/recharge'
        self.get_recharge_verify_code_url = app.BASE_URL + '/common/public/verifycode/'
    # 开户请求接口
    def account(self,session):
        response=session.post(self.account_url)
        return response
    # 获取充值验证码接口
    def get_recharge_verify_code(self,session,r):
        url=self.get_recharge_verify_code_url+r
        response=session.get(url)
        return response

    # 充值接口
    def recharge(self,session,amount="1000",code="8888"):
        data={"paymentType":"chinapnrTrust",
            "amount":amount,
            "formStr":"reForm",
            "valicode":code}
        response=session.post(self.recharge_url,data=data)
        return response