from flask import Flask, request, make_response, abort
# from flask_script import Manager

app = Flask(__name__)

# manager = Manager(app)

@app.route('/')
def index():
  user_agent = request.headers.get('User-Agent')
  print(request.headers)
  return 'Your Browser is %s!' % user_agent


@app.route('/user/<name>')
def user(name):
  return '<h1>Hello %s!</h1>' % name


@app.route('/status')
def status():
  response = make_response('This is response!')
  response.set_cookie('answer', '42')
  return response

@app.route('/except/<id>')
def exception(id):
  print(id)
  if id != '5':
    abort(404)
  return 'Hello %s' % id


if __name__ == '__main__':
  app.run()
