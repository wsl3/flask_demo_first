#encoding: utf-8
import os

DEBUG = True
#用于session和wtf的web表单加密
SECRET_KEY = os.urandom(24)

#数据库配置
#  mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format('root', 'wsl', '127.0.0.1', '3306', 'flask_app')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True



