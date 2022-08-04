import logging

import pymysql
import requests
from bs4 import BeautifulSoup

import app


def assert_utils(self,response,status_code,status,des):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(des, response.json().get("description"))

def request_third_api(form_data):
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form["action"]
    logging.info("third response={}".format(third_url))
    data = {}
    for input in soup.find_all("input"):
        data.setdefault(input["name"], input["value"])
    logging.info("third response={}".format(data))
    response = requests.post(url=third_url,data=data)
    logging.info("third response={}".format(form_data))
    return response

#定义一个数据库类
class DButils():
    @classmethod   #可以不用实例化，直接调用
    def get_conn(cls,db_name):  #建立连接
        conn=pymysql.connect(app.DB_URL,app.DB_USERNAME,app.DB_PASSWORD,app.db_name,autocommit=True)
        return conn
    @classmethod
    def close(cls,cursor=None,conn=None):  #关闭游标和连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    @classmethod
    def delete(cls,db_name,sql):   #删除数据库中数据
        try:
            conn=cls.get_conn(db_name)  #创建连接
            cursor=conn.cursor()       #创建游标
            cursor.execute(sql)        #执行sql
        except Exception as e:
            conn.rollback()
        finally:
            cls.close()


