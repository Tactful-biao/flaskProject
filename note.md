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
+ 使用Session把数据存储到session中，通过redirect函数重定向，模板传递的参数从Session中取。
+ flash Flask提供的消息提醒函数
+ get_flashed_messages() 获取所有的提醒
+ flask-sqlalchemy flask数据库交互的库
+ ORM 对象关系模型，通过类定义属性的方式，自动生成相应的表结构
+ SQLAlchemy列类型
    * Integer  普通整数，一般是32位
    * SmallInteger  取值范围小的整数，一般是16位
    * BigInteger  不限制精度的整数
    * Float  浮点数 
    * Numeric  定点数
    * String  变长字符串
    * Text  变长字符串，对较长或不限长度的字符串做了优化
    * Unicode  变长Unicode字符串
    * UnicodeText  变长Unicode字符串，对较长或不限长度的字符串做了优化
    * Boolean  布尔值
    * Date  日期
    * Time  时间
    * DateTime  日期和时间
    * Interval  时间间隔
    * Enum  一组字符串
    * PickleType  自动使用Pickle序列化
    * LargeBinary  二进制文件
+ SQLAlchemy列选项
    * primary_key  如果设为True，这列就是表的主键
    * unique  不允许出现重复的健
    * index  为这列创建索引，提示查询效率
    * nullable  是否可以为空
    * default  设置默认值
+ SQLAlchemy关系选项
    * backref 在关系的另一个模型中添加反向引用
    * primaryjoin  明确指定两个模型之间使用的联接条件。只在模棱两可的关系中需要指定
    * lazy  指定如何加载相关记录。可选值有select(首次访问时按需加载)、immediate(源对象加载后就加载)、joined(加载记录，但使用联结)、subquery(立即加载，但使用子查询)，noload(永不加载)和dynamic(不加载记录，但提供加载记录的查询)
    * uselist 如果设置为Fales，不使用列表，而使用表量值
    * order_by 指定关系中记录的排序方式
    * secondary 指定多对多关系中关系表的名字
    * secondaryjoin  SQLAlchemy无法自行决定时，指定多对多关系中的二级联结条件。
+ SQLAlchemy要求每个模型都要定义主键，这一列经常命名为id，推荐定义__repr()__方法，返回一个可读性的字符串便是模型，方便调试。
+ SQLAlchemy 搭配pymysql使用
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flaskProject'
```
+ Flask使用shell交互环境命令，在虚拟环境中：flask shell
+ Flask shell常用命令
    * db.create_all()  建表
    * db.drop_all()  删除所有表
    * db.session.add()  添加数据
    * db.session.delete()  删除数据
    * db.session.add_all([])  多行添加
    * db.session.commit()  提交到数据库
    * db.session.rollback()  回滚操作
    * Role.query.all()、first、first_or_404、get、get_or_404、count、paginate  查询数据
```
>>> from app import db
>>> db.create_all()
>>> db.drop_all();
>>> db.create_all()
>>> from app import Role, User
>>> admin_role = Role(name='Admin')
>>> mod_role = Role(name='Moderator')
>>> user_role = Role(name='User')
>>> user_john = User(username='john', role=admin_role)
>>> user_susan = User(username='susan', role=user_role)
>>> user_david = User(username='david', role=user_role)

>>> db.session.add(admin_role)
>>> db.session.add(mod_role)
>>> db.session.add(user_role)
>>> db.session.add(user_john)
>>> db.session.add(user_susan)
>>> db.session.add(user_david)
>>> db.session.commit()
```

+ SQLAlchemy 查询过滤器
    * filter()  把过滤器添加到原查询上，返回一个新查询
    * filter_by()  把等值过滤器添加到原查询上，返回一个新查询
    * limit()  使用指定的值限制原查询返回的结果数量，返回一个新查询
    * offset()  偏移原查询返回的结果，返回一个新查询
    * order_by()  根据指定条件对原查询结果进行排序，返回一个新查询
    * group_by()  根据指定条件对原查询进行分组，返回一个新查询  
