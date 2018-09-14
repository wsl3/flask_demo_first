from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    #密码优化 加密
    def __init__(self, *args, **kw):
        self.username = kw.get('username')
        self.phone = kw.get('phone')
        self.password = generate_password_hash(kw.get('password'))

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('question'))


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = db.relationship('Question', backref=db.backref('answers'))
    author = db.relationship('User', backref=db.backref('answers'))


#错误１　models.py文件中的 __tablename__ 写成了 __table__ ,出错
#错误２　exts.py文件中的SQLAlchemy() 没有用app初始化
#错误３　form表单中标签和属性距离４个空格
#错误４　form表单中 name 属性如果和前面有４个空格,request得不到name属性值,报错
#错误5  发表评论时报错 incurrent string 不正确的字符类型 title,解决方法：删除数据库重建
#注意设置charset=utf8