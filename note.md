## Flask 学习笔记
+ Flask 定义路由的方式是通过app.route修饰器，把修饰的函数注册为路由
```
@app.route('/user/<name>')
def index(name):
  return '<h1>Hello %s!</h1> % name'
```
> 路由中的尖括号用来传递参数，也可以使用类型定义/user/<int:id> 支持int、float、path类型

+ app.run(debug=True) 开启调试模式
+ Flask 请求钩子函数
    * before_first_request: 注册一个函数，在处理第一个请求之前运行
    * before_request: 注册一个函数，在每次请求之前运行
    * after_request: 注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行
    * teardown_request: 注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。
+ return '', 400  可以直接返回响应码
+ make_response 可以用来设置响应，set_cookie等
+ redirect 用于重定向 return redirect('http://www.baidu.com')
+ abort 用于处理错误, abort(404)
+ flask_script中的Manager对象可以在命令行管理app
+ render_template 模板文件, 用于渲染文件，可以传递参数，使用Jinja2渲染引擎
+ Jinja2语法: {{}} 表示取值  {% %} 表示python语法
    * 变量过滤器
    * safe  渲染时不转译
    * capitalize  把值的首字母转换成大写，其它字母转换成小写
    * lower  把值转换成小写形式
    * upper 把值转换成大写形式
    * title  把值中每个单词的首字母都转换成大写
    * trim 把值的首位空格去掉
    * striptags  渲染之前把值中所有的HTML标签都删掉
    * reverse 反转字符
    * format  格式化输出
    * truncate  字符串截断
    * 列表操作
    * first、last、length、sum、sort -- {{[1,2,3,4,5] | sum}}
+ Jinja2支持宏操作, 为了重复使用宏，还可以保存到单独的文件中，在需要使用的模板中导入使用
```
{% macro render_comment(comment) %}
    <li>{{ comment }}</li>
{% endmacro %}

文件中使用
<ul>
    {% for comment in comments %}
        {{ render_comment(comment) }}
    {% endfor %}
</ul>

模板中导入使用
{% import 'macros.html' as macros %}
<ul>
    {% for comment in comments %}
        {{ macros.render_comment(comment) }}
    {% endfor %}
</ul>

多处使用可以通过include导入
{% include 'comment.html' %}
```
+ 模板继承的写法
```
<html>
<head>
    {% block head %}
    <title>{% block title %}{% endblock %} - My Application</title>
    {% endblock %}
</head>
<body>
{% block body %}
{% endblock %}
</body>
</html>

把通用的部分提取出来。
{% extends 'base.html' %}
{% block title %}Test{% endblock %}
{% block head %}
    {{ super() }}
    <style></style>
{% endblock %}
{% block body %}
    <h1>Hello Test Page.</h1>
{% endblock %}
```
+ flask-bootstrap 为flask引入bootstrap文件, 直接在模板中导入{% extends 'bootstrap/base.html' %}
    * flask-bootstrap 基模板中定义的块
    * doc 整个HTMl文档
    * html_attribs  <html>标签属性
    * html  <html>标签中的内容
    * head  <head>标签中的内容
    * title  <title>标签中的内容
    * metas  一组<meta>标签
    * styles  层叠样式表定义
    * body_attribs  <body> 标签的属性
    * body <body>标签的内容
    * navbar 用户定义的导航条
    * content 用户定义的页面内容
    * scripys  文档底部的JavaScript声明
```
需要引入自定义js, 必须使用super()
{% block scripts %}
{{ super() }}
<script type="text/javascript" src="my-script.js"></script>
{% endblock %}
```