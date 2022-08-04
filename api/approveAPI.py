import app


class approveAPI():
    def __init__(self):
        self.approve_url=app.BASE_URL+"/member/realname/approverealname"
        self.getapprove_url=app.BASE_URL+"/member/member/getapprove"

    # 认证接口
    def approve(self,session,realname,card_id):
        data={"realname":realname,"card_id":card_id}
        response=session.post(self.approve_url,data=data,files={"x":"y"})  #multipart是多消息体
        return response
    # 获取认证接口
    def getapprove(self,session):
        response=session.post(self.getapprove_url)
        return response