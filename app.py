# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
from flask import g
from flask_bootstrap import Bootstrap
import config
from exts import db
from models import User, Question, Answer
from decorator import login_required

app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-time').all()
    }
    return render_template('index.html', **context)


@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(Question.title.contains(q))

    return render_template('index.html', questions=questions)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phone = request.form.get('phonenumber')
        password = request.form.get('password')
        # print(password)

        # 查找手机号为phone的对象
        user = User.query.filter_by(phone=phone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            # print("id:%s"%user.phone)
            return redirect(url_for('index'))
        else:
            return "输入错误或未注册"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        phone = request.form.get('phonenumber')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(phone=phone).first()
        print(password2)

        # 手机号码验证
        if user:
            return "该手机已经注册！"
        # 密码验证
        if password1 != password2:
            return "密码不一致！"
        userNew = User(username=username, phone=phone, password=password1)
        db.session.add(userNew)
        db.session.commit()
        return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # 清除session的user_id退出
    # session.clear()
    # del session['user_id']
    session.pop('user_id')
    return redirect(url_for('register'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        q = Question(title=title, content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter_by(id=user_id).first()
        q.author = g.user
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/details/<question_id>', methods=['GET', 'POST'])
def details(question_id):
    question = Question.query.filter_by(id=question_id).first()
    return render_template('details.html', question=question)


@app.route('/add_answer/', methods=['POST'])
def answer():
    content = request.form.get('answer')
    question_id = request.form.get('question_id')
    question = Question.query.filter_by(id=question_id).first()

    # author_id = session.get('user_id')
    # author = User.query.filter_by(id=author_id).first()

    answer = Answer(content=content)
    answer.author = g.user
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('details', question_id=question_id))


# 程序优化
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        g.user = user


# 查看用户是否登录 只要session中有user_id就已经登录
@app.context_processor
def my_context_processor():
    # user_id = session.get("user_id")
    if hasattr(g, 'user'):
        # user = User.query.filter_by(id=user_id).first()
        return {'user': g.user}
    return {}


if __name__ == '__main__':
    app.run()
