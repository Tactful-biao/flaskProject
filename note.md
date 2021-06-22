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
    * html_attribs  html标签属性
    * html  html标签中的内容
    * head  head标签中的内容
    * title  title>标签中的内容
    * metas  一组meta标签
    * styles  层叠样式表定义
    * body_attribs  body 标签的属性
    * body body标签的内容
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

+ flask-moment 处理日期和时间
    * moment提供的格式化选项
    * format()
    * fromNow()
    * fromTime()
    * calendar()
    * valueOf()
    * unix()
```
引入moment
{% block scripts %}
{{ super() }}
{{ moment.include_moment() }}
{% endblock %}

使用moment
<p>The local date and time is {{ moment(current_time).format('LLL') }}.</p> <p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
```

+ WTForms 表单处理
    * 支持的标准字段
    * StringField 文本字段
    * TextAreaField  多行文本字段
    * PasswordField  密码文本字段
    * HiddenField  隐藏文本字段
    * DateField  文本字段，值为datetime.date格式
    * DateTimeField 文本字段，值为datetime.datetime格式
    * IntegerFile  文本字段，值为整数
    * DecimalFile  文本字段，值为decimal.Decimal
    * FloatField  文本字段，值为浮点数
    * BooleanField  复选框，值为True和False
    * RadioField  一组单选框
    * SelectField  下拉列表
    * FileField  文件上传字段
    * SubmitField  表单提交按钮
    * FormField  把表单作为字段嵌入另一个表单
    * FieldList  一组指定类型的字段
+ WTForms验证函数
    * Email  验证电子邮件地址
    * EqualTo 比较两个字段的值，常用于要求确认密码的情况
    * IPAddress  验证IPv4地址
    * Length  验证输入字符串的长度
    * NumberRange  验证输入的值在数字范围内
    * Optional  无输入值时跳过其他验证函数
    * Required  确保字段中有数据
    * Regexp  使用正则表达式验证输入值
    * URL  验证URL
    * AnyOf  确保输入值在可选列表中
    * NoneOf  确保输入值不在可选值列表中
+ wtf提供的quick_form方法可以快速创建一个表单
```
在html中引入
{{ wtf.quick_form(form) }}

在路由中传入form
return render_template("index.html",form=form)
```
+ 在定义路由的时候通过传入methods来定义接收的请求方法