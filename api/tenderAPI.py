import app


class tenderAPI():
    def __init__(self):
        self.tender_url=app.BASE_URL+"/trust/trust/tender"
        self.tenderlist_url=app.BASE_URL+"/loan/tender/mytenderlist" #我的投资列表
        self.loaninfo_url = app.BASE_URL + "/common/loan/loaninfo" #投资产品详情
        # 投资产品详情接口
    def loaninfo(self,session,id):
        data = {"id": id}
        response=session.post(self.loaninfo_url,data=data)
        return response
    # 投资接口
    def tender(self,session,id,amount,depositCertificate=-1):
        data={"id":id,
        "depositCertificate":depositCertificate,
        "amount": amount}
        response=session.post(self.tender_url,data=data)
        return response
    # 我的投资列表接口
    def get_tenderlist(self, session, status):
        data = {"status": status}
        response=session.post(self.tenderlist_url,data=data)
        return response