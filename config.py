import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
  SECRET_KEY = 'dsfdghjgfsdassdfjhjkjjghfgdsewdsc'
  SQLALCHEMY_COMMIT_ON_TEARDOWN = True
  BIAO_MAIL_SUBJECT_PREFIX = '[BIAO]'
  SECURITY_EMAIL_SENDER = '1208339113@qq.com'
  MAIL_SERVER = 'smtp.qq.com'
  MAIL_PORT = 465
  MAIL_USE_SSL = True
  MAIL_USE_TLS = False
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@localhost/flaskProject'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  @staticmethod
  def init_app(app):
    pass


class DevelopmentConfig(Config):
  DEBUG = True


config = {
 'default': DevelopmentConfig
}