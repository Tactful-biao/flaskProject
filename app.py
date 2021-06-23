import os.path

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flaskProject'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'dsfdghjgfsdassdfjhjkjjghfgdsewdsc'

# 发送邮件
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['BIAO_MAIL_SUBJECT_PREFIX'] = '[BIAO]'
app.config['SECURITY_EMAIL_SENDER'] = '1208339113@qq.com'


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.name.data).first()
    if user is None:
      user = User(username=form.name.data)
      db.session.add(user)
      session['known'] = False
      if app.config['SECURITY_EMAIL_SENDER']:
        send_email(app.config['SECURITY_EMAIL_SENDER'], 'New User', 'mail/new_user', user=user)
    else:
      session['known'] = True
    session['name'] = form.name.data
    form.name.data = ''
    return redirect(url_for('index'))

  return render_template("index.html", form=form, name=session.get('name'), known=session.get('known', False))


def send_email(to, subject, template, **kwargs):
  msg = Message(app.config['BIAO_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['SECURITY_EMAIL_SENDER'], recipients=[to])
  msg.body = render_template(template + '.txt', **kwargs)
  msg.html = render_template(template + '.html', **kwargs)
  mail.send(msg)


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500


@app.route('/user/<name>')
def user(name):
  return render_template("user.html", name=name)


def make_shell_context():
  return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('Shell', Shell(make_context=make_shell_context))


class NameForm(FlaskForm):
  name = StringField('What is your name?', validators=[DataRequired()])
  submit = SubmitField('Submit')


class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)
  users = db.relationship('User', backref='role', lazy='dynamic')

  def __repr__(self):
    return '<Role %r>' % self.name


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

  def __repr__(self):
    return '<User %r>' % self.username


if __name__ == '__main__':
  manager.run()
