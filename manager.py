#encoding: utf-8

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app
from exts import db
from models import User, Question, Answer


manager = Manager(app)


#使用app和db初始化数据库迁移工具Migrate
migrate = Migrate(app, db)

#在命令行中添加数据库迁移命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


