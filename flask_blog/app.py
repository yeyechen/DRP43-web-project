import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

DATABASE_ACCOUNT = os.environ["DATABASE_ACCOUNT"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_DOMAIN_NAME = os.environ["DATABASE_DOMAIN_NAME"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
APP_CONFIG_KEY = os.environ["APP_CONFIG_KEY"]

app = Flask(__name__)


def setDatabase(app, test=False):
    app.config['SQLALCHEMY_DATABASE_URI'] \
        = 'mysql://' + DATABASE_ACCOUNT + ':' + DATABASE_PASSWORD + '@' \
          + DATABASE_DOMAIN_NAME + ':3306/' + DATABASE_NAME
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zhangziheng:@106.52.101.201:3306/accounts'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = APP_CONFIG_KEY
    # app.config['SECRET_KEY'] = "123"
    db = SQLAlchemy(app)
    pymysql.install_as_MySQLdb()
    return db


db = setDatabase(app)


def initDatabase(new=False):
    from flask_blog.db import completeClassInit
    if new:
        db.drop_all()
    completeClassInit()
    db.create_all()
    return db


db = initDatabase(True)
sql_query1 = "INSERT INTO account (create_date, username, password) " \
             "VALUES ('2021-6-3 10:00:00', 'Amy', 'Amy')"
sql_query2 = "INSERT INTO note (author_id, note_name, create_date, refs) " \
             "VALUES (1, 'The Tang Dynasty', '2021-6-3 10:00:00', 0)"
sql_query3 = "INSERT INTO history_node (note_id, title, start_date, end_date, content) " \
             "VALUES ('1', 'Flourishment Age of Kaiyuan Era', '712', '741', 'content')"
sql_query4 = "INSERT INTO history_node (note_id, title, start_date, end_date, content) " \
             "VALUES ('1', 'Government of Zhenguan', '627', '649', 'society developed quickly')"
sql_query5 = "INSERT INTO note (author_id, note_name, create_date, refs) " \
             "VALUES (1, 'The Qin Dynasty', '2021-6-3 10:00:00', 0)"
sql_query6 = "INSERT INTO history_node (note_id, title, start_date, end_date, content) " \
             "VALUES ('2', 'Building Great Wall', '-214', '-170', 'large labour force to build Great World')"
sql_query7 = "INSERT INTO history_node (note_id, title, start_date, end_date, content) " \
             "VALUES ('1', 'The Tang Dynasty establishment and destory', '618', '907', 'content')"
db.session.execute(sql_query1)
db.session.execute(sql_query2)
db.session.execute(sql_query3)
db.session.execute(sql_query4)
db.session.execute(sql_query5)
db.session.execute(sql_query6)
db.session.execute(sql_query7)
db.session.commit()

 
@app.route('/hello')
def hello_world():
    return "Hello World"


import flask_blog.auth as auth
app.register_blueprint(auth.bp)
import flask_blog.blog as blog
app.register_blueprint(blog.bp)
import flask_blog.main_page as main
app.register_blueprint(main.bp)
import flask_blog.edit_page as edit
app.register_blueprint(edit.bp)
app.add_url_rule('/', endpoint='index')


def getApp():
    return app


if __name__ == '__main__':
    app.run()
