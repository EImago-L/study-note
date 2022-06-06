# Flask

## **初识flask**

### **Pipenv工作流**

1. **安装Pipenv**

   `pip install pipenv`

2. **创建虚拟环境**

   `pipenv install`

   单独使用Virtualenv时，通常会显式地激活虚拟环境。使用`pipenv shell`命令显式激活虚拟环境

   `pipenv run python hello.py`命令可以不显式激活虚拟环境即可执行命令。

3. 管理依赖

   创建虚拟环境时，如果项目根目录下没有Pipfile文件，`pipenv install`命令会在该项目根目录中创建Pipfile和Pipfile.lock文件，使用pipenv安装/删除/更新依赖包时，这两个文件会自动更新

   在新的环境运行程序时，执行`pipenv install`命令，Pipenv会创建一个新的虚拟环境，自动Pipfile文件中读取依赖安装



### **安装flask**

`pipenv install flask`



### **最小Flask程序**

```python
from flask import Flask

# 创建程序实例
app = Flask(__name__)

# @app.route()注册路由
@app.route('/')
def index():
    return "<h1>Hello Flask</h1>"


# 一个视图绑定多个URL
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'

# 动态URL，添加默认值
@app.route('/greet', defaults={'name':'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello , %s!' % name

```



### **启动开发服务器**

命令`flask run`

如果出现报错“Error: Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.”

记得进入要运行地py文件的目录下，如果py文件名不是`app.py`或者`wsgi.py`而是其他名字，如hello.py
linux下：`export FLASK_APP=hello`
Windows下：`set FLASK_APP=hello`



#### **管理环境变量**

如果安装了python-dotenv，使用`flask run`或其他命令时它会自动从`.flaskenv`和`.env`文件中加载环境变量，没有就自己建一个

优先级：手动设置的环境变量>.env中的环境变量>.flaskenv中的环境变量



### **设置运行环境**

Flask提供一个`FLASK_ENV`环境变量来设置环境，默认为`production`。开发时，我们设置为`development`
在.flaskenv文件中写入：

```python
FLASK_ENV=development
```



### **Flask拓展**

如果一个拓展名为Flask_foo,初始化类为Foo则使用拓展为：

```python
from flask import Flask
from flask_foo import Foo

app = Flask(__name__)
foo = Foo(app)
```



### **项目配置**

配置变量可以通过Flask对象的app.config属性作为统一的接口来设置，可以像操作字典一样操作它

如：

```python
app.config['ADMIN_NAME'] = 'Peter'
```

也可以用`update()`方法一次加载多值

```python
app.config.update(
    TESTING=True,
    SECRET_KEY='_654#$sf'
)
```

拿到配置中值

```python
value = app.config('ADMIN_NAME')
```



### **URL与端点**

`url_for()`函数返回视图函数对用的url，如

```python
@app.route('/')
def index():
    return "<h1>Hello Flask</h1>"
```

执行`url_for('index')`的返回值为：/

如果url含有动态的部分

```python
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello , %s!' % name
```

`url_for('greet', name='Jack')`返回值为：/greet/Jack

`url_for()`函数返回的是相对URL，要想返回绝对URL可以添加参数`_external=True`



### **Flask命令**

我们可以自定义flask命令，如：

```python
import click

@app.cli.command()
def hello():
    '''
    just say hello
    '''
    click.echo('Hello, Human！')
```

在这里使用命令`flask hello`来触发函数，函数的文档字符串会作为帮助信息显示，可以在`@app.cli.command()`装饰器中传入参数来设置命令名称



## **Flask与HTTP**

### **HTTP请求**

url组成部分：

|       信息       |            说明            |
| :--------------: | :------------------------: |
|     http://      | 协议字符串，指定要用的协议 |
|  helloflask.com  |    服务器的地址（域名）    |
| /hello?name=Grey |  要获取的资源路径（path）  |



请求报文：

|          组成说明           |                         请求报文内容                         |
| :-------------------------: | :----------------------------------------------------------: |
| 请求首行（方法，URL，协议） |      GET http://helloflask.com/hello?name=Grey HTTP/1.1      |
|           请求头            | Host:helloflask.com<br />Connection:keep-alive<br />User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64)<br />... |
|            空行             |                                                              |
|          报文主体           |                                                              |

![image-20220109115920502](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20220109115920502.png)



### **Request对象**

Request对象封装了从客户端发来的请求报文，通过它可以获取请求报文中的所有数据

**使用request的属性获取请求：**
以`http://helloflask.com/hello?name=Grey`为例

|   属性    |                   值                    |
| :-------: | :-------------------------------------: |
|   path    |                ’/hello‘                 |
| full_path |           '/hello?name=Grey'            |
|   host    |            'hellofalsk.com'             |
| host_url  |        'http://helloflask.com/'         |
| base_url  |      'http://helloflask.com/hello'      |
|    url    | 'http://helloflask.com/hello?name=Grey' |
| url_root  |        'http://helloflask.com/'         |



**request对象常用的属性和方法**
![](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/8433115-e4064fe26aa64083.jpg)



### **在Flask中处理请求**

#### **路由匹配**

命令行输入命令`flask routes`
![image-20220109121253051](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20220109121253051.png)



#### **设置监听的HTTP方法**

```python
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return '<h1>hello, Flask!</h1>'
```



#### **URL处理**

flask 内置url变量转换器：

| 转换器 |             说明             |
| :----: | :--------------------------: |
| string | 不包含斜线的字符串（默认值） |
|  int   |             整型             |
| float  |            浮点数            |
|  path  |       包含斜线的字符串       |
|  any   | 匹配一系列给定值中的一个元素 |
|  uuid  |          UUID字符串          |

```python
@app.route('/goback/<int:year>')
def goback(year):
    return 'Welcom to %d' % (2022-year)


colors = ['blue', 'white', 'red']
@app.route('/goback/<any(%s):color>'%format(str(colors)[1:-1]))
def three_color(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or  rude</p>'
```



#### **请求钩子**

|         钩子         |                             说明                             |
| :------------------: | :----------------------------------------------------------: |
| before_first_request |             注册一个函数，在处理第一个请求前运行             |
|    before_request    |              注册一个函数，在处理每个请求先运行              |
|    after_request     | 注册一个函数，如果没有未处理的异常抛出，会在每个请求结束后运行 |
|   teardown_request   | 注册一个函数，即使有未处理的异常抛出，会在每个请求结束后运行。<br />如果发生异常，会传入异常对象作为参数到注册的函数中 |
|  after_this_request  |       在视图函数内注册一个函数，会在这个请求结束后运行       |

```python
@app.before_request
def do_something():
    pass # 这里的代码会在每个请求处理前执行
```



### **HTTP响应**

#### **响应报文**

|              组成说明              |                         响应报文内容                         |
| :--------------------------------: | :----------------------------------------------------------: |
| 响应首行（协议、状态码、原因短语） |                       HTTP/1.1 200 OK                        |
|               响应头               | Content-Length: 44 <br />Content-Type: application/json <br />Date: Sun, 09 Jan 2022 03:47:17 GMT <br />Server: Werkzeug/2.0.2 Python/3.8.2<br />... |
|                空行                |                                                              |
|               响应体               |                    \<h1>Hello,Human\</h1>                    |



#### **在Flask中生成响应**

视图函数返回最多三个元素组成：响应体、状态码、响应头

如果要生成状态码为3xx的重定向响应，需要在响应头中的location字段设置目标url

```python
@app.route('/hello')
def hello():
    ...
    return '', 302, {'location':'https://www.strongforu.top'}
```



Flask提供了`redirect()`函数来生成重定向响应

```python
from flask import Flask,redirect
# ...
@app.route('/res')
def func1():
    return redirect('https://www.strongforu.top')

@app.route('/hi')
def hi():
    return redirect(url_for('hello'))
```



返回404错误响应

```python
from flask import Flask,abort
# ...
@app.route('/404')
def not_found():
    abort(404)
```



#### **响应格式**

如果使用其他MIME类型，可以通过Flask提供的**`make_response()`**方法生成响应

```python
from flask import Flask,make_response
# ...
@app.route('/foo')
def foo():
    data = {
        'name':'grey li',
        'gender':'male'
    }
    response = make_response(json.dumps(data))
    response.mimetype = 'text/json'
    return response
```



Flask提供了**`jsonify()`**函数，它会将传入的参数序列化，转换为json字符串作为响应主体，生成响应对象，并设置MIME类型

```python
from flask import Flask,make_response
# ...
@app.route('/foo')
def foo():
    return jsonify(name='eimago', gender='male')
```



#### **Cookie**

在响应中添加cookie需要使用`make_response()`方法生成一个响应，然后使用`set_cookie()`方法。

**Response类常用属性和方法：**

|  方法/属性   |                          说明                           |
| :----------: | :-----------------------------------------------------: |
|   headers    | 一个Werkzeug的Headers对象，表示响应头，可像字典一样操作 |
|    status    |                    状态码，文本类型                     |
| status_code  |                      状态码，整型                       |
|   mimetype   |                        MIME类型                         |
| set_cookie() |                   用来设置一个cookie                    |



**set_cookie()方法的参数：**

|   属性   |                             说明                             |
| :------: | :----------------------------------------------------------: |
|   key    |                          cookie的键                          |
|  value   |                          cookie的值                          |
| max_age  | cookie被保存的时间，单位秒；默认会话结束（关闭浏览器）时过期 |
| expires  |          具体过期时间，一个datetime对象或UNIX时间戳          |
|   path   |         限制cookie只在给定的路径可用，默认为整个域名         |
|  domain  |                     设置cookie可用的域名                     |
|  secure  |               如果为True，只用通过HTTPS才可用                |
| httponly |             如果设为True，禁止客户端JS获取cookie             |

```python
from flask import Flask, make_response
# ...
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name',name)
    return response
```

**从request中获取cookie**

```python
from flask import Flask, request
# ...
@app.route('/hello')
def hello():
    name = requests.args.get('name')
    if name is None:
        name = request.cookie.get('name', 'Human')
    return '<h1>Hello, %s</h1>' % name
```



#### **Session**

session通过密钥对数据进行签名以加密数据，所以我们得先设置一个密钥

- 通过Flask.secret_key属性设置
  `app.secret_key = 'secret string'`

- 将密钥写进环境变量中（export或set命令），或者写在.env / .flaskenv文件中（推荐这种）
  `SECRET_KEY = secret string`

  之后在程序中使用os模块提供得`getenv()`获取

  ```python
  import os
  app.secret_key = os.getenv('SECRET_KEY','secret string') # 类似于字典得get，没有获取到环境变量时使用第二个参数为默认值
  ```



**模拟用户认证**

```python
from flask import Flask, redirect, url_for, session, abort
from markupsafe import escape
# ...
@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','human')
    response = '<h1>hello, %s!</h1>' % escape(name)
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    print(g.name)
    return response

@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))

# 模拟管理后台
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'

# 登出用户
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))
```



### **HTTP 进阶实践**

**重回上一个页面:**

```python
from flask import Flask, url_for, redirect
from urllib.parse import urlparse, urljoin
@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)

@app.route('/do-something')
def do_something():
    # do something
    return redirect_back()

def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
```



### **Web 安全防范**

#### **注入攻击**

以sql注入为例

防范方法：

1. 使用ORM可以一定程度上避免SQL注入问题
2. 验证输入类型，如某视图函数接收整型id来查询，那么就在URL规则里限制URL变量为整型
3. 参数化查询。构造SQL语句时，使用各类接口库提供得参数或查询方法



#### **Xss攻击**

防范方法：

1. HTML转义，使用markupsafe的escape方法
2. 验证用户输入







#### **CSRF 攻击**

防范方法：

1. 正确使用HTTP方法
2. CSRF令牌校验



## **Flask模板**

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{user.username}}</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <link href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<a href="{{url_for('index')}}">&larr; Return</a>
<h2>{{user.username}}</h2>
{% if user.bio %}
    <i>{{user.bio}}</i>
{% else %}
    <i>This user has not provided a bio</i>
{% endif %}
<h5> {{user.username}}'s Watchlist {{ movies|length }} :</h5>
<ul>
    {% for movie in movies %}
        <li>{{movie.name}} - {{movie.year}}</li>
    {% endfor %}
</ul>
</body>
</html>
```

1. 语句

   比如if判断，for循环等
   `{% ... %}`

2. 表达式

   比如字符串、变量、函数调用等
   `{{ ... }}`

3. 注释
   `{# ... #}`



### **模板基本用法**

**控制结构：**

```jinja2
{% if user.bio %}
    <i>{{user.bio}}</i>
{% else %}
    <i>This user has not provided a bio</i>
{% endif %}
```

```jinja2
<ul>
    {% for movie in movies %}
        <li>{{movie.name}} - {{movie.year}}</li>
    {% endfor %}
</ul>
```



**常用的Jinja2 for循环特殊变量：**

| 变量名         | 说明                          |
| -------------- | ----------------------------- |
| loop.index     | 当前迭代数（从1开始计数）     |
| loop.index0    | 当前迭代数（从0开始计数）     |
| loop.revindex  | 当前反向迭代数（从1开始计数） |
| loop.revindex0 | 当前反向迭代数（从0开始计数） |
| loop.first     | 如果是第一个元素，则为True    |
| loop.last      | 如果是最后一个元素，则为True  |
| loop.previtem  | 上一个迭代的条目              |
| loop.nextitem  | 下一个迭代的条目              |
| loop.length    | 序列包含的元素数量            |



#### **渲染模板**

在视图函数中渲染模板时，我们使用**`render_template()`**

```python
from flask import Flask, render_template
@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)
```

Flask会自动在程序根目录下的templates文件夹中寻找模板文件，user和movies是向模板中传递的变量，可以是任意类型



### **模板辅助工具**

#### **上下文**

模板中有许多变量，我们可以使用`render_template()`函数传递，也可以在模板中定义变量

```jinja2
{% set navigation = [('/', 'Home'), ('/about', 'About')] %}
```

也可以将一部分模板数据定义为变量

```jinja2
{% set navigation %}
	<li><a href='/'>Home</a></li>
	<li><a href='/about'>About</a></li>
{% endset %}
```



##### **内置上下文变量：**

| 变量    | 说明                                           |
| ------- | ---------------------------------------------- |
| config  | 当前的配置对象                                 |
| request | 当前的请求对象，在已激活的请求环境下可用       |
| session | 当前的会话对象，在已激活的请求环境下可用       |
| g       | 与请求绑定的全局变量，在已激活的请求环境下可用 |



##### **自定义上下文**

Flask提供一个**`app.context_processor`**装饰器，可以用来注册模板上下文处理函数

```python
@app.context_processor
def inject_foo():
    foo = 'I am foo'
    return dict(foo=foo)
```

使用`render_template()`函数渲染模板时，**所有使用`app.context_processor`装饰的函数都会被执行**，**函数的返回值会被添加到模板中，所以我们可以直接在模板中使用foo变量**

也可以将`app.context_processor`作为方法调用

```python
# ...
def inject_foo():
    foo = 'I am foo'
    return dict(foo=foo)
app.context_processor(inject_foo)
```



#### **全局对象**

**Jinja2 内置模板全局函数（部分）：**

| 函数                                    | 说明                                                         |
| --------------------------------------- | ------------------------------------------------------------ |
| range([start,]stop[,step])              | 和python中的range()用法相同                                  |
| lipsum(n=5, html=True, min=20, max=100) | 生成随机文本，测试时用来填充页面。默认生成5段，每段20~100单词 |
| dict(**items)                           | 和python中的dict()用法相同                                   |

**Flask 内置模板全局函数：**

| 函数                   | 说明                    |
| ---------------------- | ----------------------- |
| url_for()              | 用于生成URL的函数       |
| get_flashed_messages() | 用于获取flash消息的函数 |



##### **自定义全局函数**

使用**`app.template_global()`**装饰器直接将函数注册为模板全局函数

```python
@app.template_global()
def bar():
    return 'I am bar'
```

默认使用函数原名称传入模板，在`app.template_global()`中使用name参数可以指定名称。`app.template_global()`仅能注册自定义全局函数

> 可以直接使用**`app.add_template_global()`**方法注册自定义全局函数，传入函数对象和可选的自定义名称，如`app.add_template_global(your_global_function)`



#### **过滤器**

```jinja2
{{ name|title }}
{{ movies|length }}
{% filter upper %}
	This text becomes uppercase.
{% endfilter %}
```



**Jinja2 常用内置过滤器：**

| 过滤器                                                       | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| abs(value)                                                   | 返回value的绝对值                                            |
| default(value,default_value)                                 | 设置默认值，如果value没有定义，则返回默认的default_value值   |
| escape(value)/e(value)                                       | 将value中的<,>等符号转义为html符号                           |
| first(value)                                                 | 获取value(序列)中的第一个值                                  |
| last(value)                                                  | 获取value(序列)中的最后一个值                                |
| length(value)                                                | 获取value的长度                                              |
| random(seq)                                                  | 接受一个序列对象, 随机返回其中的一个元素                     |
| safe(value)                                                  | 标记传入的value值是安全的, 使用escape转码时不会发生二次转码  |
| trim(value)                                                  | 去掉字符串开始和末尾多余的空白字符                           |
| max(value, case_sensitive=False, attribute=None)             | 返回序列中的最大值                                           |
| min(value, case_sensitive=False, attribute=None)             | 返回序列中的最小值                                           |
| unique(value, case_sensitive=False, attribute=None)          | 返回序列中不重复的值                                         |
| striptags(values)                                            | 剥离HTML/XML标签, 并且将多个空白字符转换成单空格             |
| urlize(value, trim_url_limit = None, nofollow = False， tartget=None， rel=None) | 将url文本转换为可单机的HTML链接                              |
| wordcount(string)                                            | 计算string中的单词数                                         |
| tojson(value, indent=None)                                   | 将变量值转换为JSON格式                                       |
| truncate(string, length = 255, killwords = False, end = “…”) | 截取前length个字符，killwords设置是否阶段单词，end设置结尾的符号 |

防范XSS攻击的主要措施是对用户输入的文本进行转义，Jinja2会对模板中的变量进行转义。如果想避免转义可以使用safe过滤器

```jinja2
{{ sanitized_text|safe }}
```

也可以在渲染前将变量转换为Markup对象

```python
from flask import Markup
def musical(s):
    return s + Markup('&#9835;')
```



##### **自定义过滤器**

使用**`app.template_filter()`**装饰器注册自定义过滤器

```python
@app.template_filter()
def musical(s):
    return s + Markup('&#9835;')
```

```jinja2
{# 调用 #}
{{ name|musical }}
```

默认使用函数原名称传入模板，在`app.template_filter()`中使用name参数可以指定名称。

>可以直接使用**`app.add_template_filter()`**方法注册自定义过滤器，传入函数对象和可选的自定义名称，如`app.add_template_filter()(your_filter_function)`



#### **测试器**

测试器用来测试变量或表达式，返回布尔值，如

```jinja2
{% if age is number %}
	{{ age * 365}}
{% else %}
	无效的数字
{% endif %}
```



**常用内置测试器：**

| 测试器               | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| callable(object)     | 测试一个对象是否是可调用对象                                 |
| defined(value)       | 测试传入的对象是否已经定义了                                 |
| undefined(value)     | 检查一个对象是否未定义                                       |
| none(value)          | 检查对象是否是空对象None                                     |
| number(value)        | 检查对象是否是一个数字                                       |
| string(value)        | 检查对象是否是string                                         |
| sequence(value)      | 检查对象是否是序列, 序列同样是可迭代对象                     |
| iterable(value)      | 检查对象是否是可迭代的                                       |
| sameas(value, other) | 检查传入的对象和other指定的对象是否在内存中的同一块地址(同一个对象) |

is左侧是测试器的第一个参数，其他参数可以添加在括号内，也可以写在右侧

```jinja2
{% if foo is sameas(bar) %}
{% if foo is sameas bar %}
```



##### **自定义测试器**

使用**`app.template_test()`**装饰器来注册自定义测试器

```python
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False
```

默认使用函数原名称传入模板，在`app.template_test()`中使用name参数可以指定名称。

>可以直接使用**`app.add_template_test()`**方法注册自定义过滤器，传入函数对象和可选的自定义名称，如`app.add_template_test(your_test_function)`



#### **模板环境对象**

我们可以使用`app.jinja_env`更改Jinja2的设置。全局函数、过滤器、测试器分别存储在Environment对象的globals、filters、tests属性中，可以像操作字典一样添加相应的函数和变量

1. 添加自定义全局对象

   ```python
   def bar():
       return 'I am bar.'
   foo = 'I am foo'
   app.jinja_env.globals['bar'] = bar
   app.jinja_env.globals['foo'] = foo
   ```

2. 添加自定义过滤器

   ```python
   def smiling(s):
       return s + ':)'
   app.jinja_env.filters['smiling'] = smiling
   ```

3. 添加自定义测试器

   ```python
   def baz(n):
       if n == 'baz':
           return True
       return False
   app.jinja_env.tests['baz'] = baz
   ```



### **模板结构组织**

#### **局部模板**

当多个独立模板中都会使用同一块HTML代码时，我们可以把这部分代码抽离出来，存储到局部模板中，假如局部模板文件名为_banner.html

我们就可以用include标签在任意位置插入模板

```jinja2
{% include '_banner.html' %}
```



#### **宏**

类似与python中的函数，把一部分模板代码封装到宏里，使用传递参数来构建内容。

我们可以把宏存储在单独的文件中，加入文件名为macros.html

```jinja2
{% macro qux(amount=1) %}
	{% if amount ==1  %}
		I am qux.
    {% elif amount > 1 %}
    	We are quxs.
    {% endif %}
{% endmacro %}
```

调用：

```jinja2
{% from 'macros.html' import qux %}
{{ qux(amount=5) }}
```

使用非直接渲染的模板时（如macros.html），这个模板不包含一下对象

- 扩展使用内置的模板上下文处理函数提供的变量
- 自定义模板上下文处理器传入的变量
- 使用`render_template()`函数传入的变量

如果想要使用，需要在导入时显式地使用with context声明

```jinja2
{% from "macros.html" import foo with context %}
```



#### **模板继承**

**基模板base.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
    <meta charset="UTF-8">
    <title>{% block title %}Template - HelloFlask{% endblock %}</title>
    {% block style %}
        <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.css') }}">
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    {% endblock %}
    {% endblock %}
</head>
<body>
<nav>
    <ul><li><a href="{{ url_for('index') }}">Home</a></li></ul>
</nav>
<main>
    {% for message in get_flashed_messages() %}
        <div class="alert">{{ message }}</div>
    {% endfor %}
    {% block content %}
    {% endblock %}
</main>
<footer>
    {% block footer %}
        ......
    {% endblock %}
</footer>
{% block scripts %}
<script src="{{ url_for('static', filename='js/bootstrap.min.js') }}"></script>
{% endblock %}
</body>
</html>
```

**子模版index.html**

```html
{% extends 'base.html' %}
{% from 'macros.html' import qux %}

{% block content %}
{% set name='baz' %}
<h1>Template</h1>
<ul>
    <li><a href="{{ url_for('watchlist') }}">Watchlist</a></li>
    <li>Filter:{{ foo|musical }}</li>
    <li>Global:{{ bar() }}</li>
    <li>Test:{% if name is baz %}I am baz.{% endif %}</li>
    <li>Macro:{{ qux(amount=5) }}</li>
</ul>
{% endblock %}
```

- 覆盖内容
  在子模版中创建同名的块

- 追加内容
  在子模版中向基模板追加内容需要用到**`super()`**函数

  ```jinja2
  {% block styles %}
  {{ super() }}
  <style>
  ......
  </style>
  {% endblock %}
  ```

  

### **模板进阶实践**

#### **空白控制**

实际输出的HTML文件中，模板中的Jinja2语句、表达式等会被保留移除后的空行
![image-20220110205629691](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20220110205629691.png)

如果想要在渲染时自动去掉这些空行，需要在定界符内测添加减号

```jinja2
{% if user.bio -%}
    <i>{{user.bio }}</i>
{%- else %}
<ul>
    {%- for movie in movies %}
        <li>{{movie.name}} - {{movie.year}}</li>
    {%- endfor %}
</ul>
```

右侧移除语句前的空白，左侧移除语句后的空白

也可以通过模板环境对象的**`trim_blocks`**和**`lstrip_blocks`**属性设置
`trim_blocks`删除Jinja2语句后的第一个空行
`lstrip_blocks`删除Jinja2语句所在行之前的空格和制表符

```python
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
```

> 宏内的空白不受则两个属性控制，需要手动设置



#### **加载静态文件**

使用**`url_for()`**函数来获取静态文件的URL。Flask内置了用于获取静态文件的视图函数，端点值为static，规则为`/static/<path:filename>`，filename是相较于static文件夹的根目录的文件路径

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<link rel="icon" type="image/x-icon" href="{{url_for('static', filename='favicon.ico')}}">
<img src="{{url_for('static', filename='avatar.jpg')}}" alt="" width="50">
```



我们也可以创建一个专门的宏来加载静态资源

```jinja2
{% macro static_file(type, filename_or_url, local=True) %}
    {% if local -%}
        {% set filename_or_url = url_for('static', filename=filename_or_url) %}
    {%- endif %}
    {% if type == 'css' -%}
        <link rel="stylesheet" href="{{ filename_or_url }}" type="text/css">
    {%- elif type == 'js' -%}
        <script type="text/javascript" src="{{ filename_or_url }}"></script>
    {%- elif type == 'icon' -%}
        <link rel="icon" href="{{ filename_or_url }}">
    {%- endif %}
{% endmacro %}
```

在模板导入宏后，调用时传入静态资源类别和文件路径

```jinja2
{{ static_file('css', 'css/bootstrap.min.css') }}

{# 从cdn加载资源时，local设置为False #}
{{ static_file('css', 'https://.../bootstrap.min.css', local=False) }}
```



#### **消息闪现**

Flask提供`flash()`函数，来“闪现”需要显式给用户的消息。`flash()`函数发送的消息会存储在session中，模板中使用全局函数`get_flashed_messages()`时将消息显示出来

> 使用这个函数需要先设置密钥

```python
app.secret_key = os.getenv('SECRET_KEY','secret string')

@app.route('/flash')
def just_flask():
    flash('I am flash!')
    return redirect(url_for('index'))
```

```jinja2
<main>
    {% for message in get_flashed_messages() %}
        <div class="alert">{{ message }}</div>
    {% endfor %}
    {% block content %}
    {% endblock %}
</main>
```



#### **自定义错误页面**

使用**`app.errorhandler()`**装饰器注册错误处理函数来自定义错误页面，**需要将错误状态码作为参数传入装饰器，异常类作为错误处理函数的参数**

```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404
```

**错误模板文件：**

```jinja2
{% extends 'base.html' %}
{% block title %}
    404-Page Not Found
{% endblock %}

{% block content %}
    <h1>Page Not Found</h1>
   	<p>You are lost...</p>
{% endblock %}
```



错误处理函数接收异常对象作为参数，内置的异常对象提供了下列常用属性

| 属性        | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| code        | 状态码                                                       |
| name        | 原因短语                                                     |
| description | 错误描述，另外使用`get_description()`方法可以获取HTML格式的错误描述代码 |



## **Flask 表单**

### **使用Flask-WTF处理表单**

**安装：**`pipenv install flask-wtf email-validator`

Flask-WTF默认为表单开启csrf保护。默认情况下，Flask-WTF使用程序密钥对csrf令牌进行签名，所以需要设置密钥`app.secret_key = 'secret string'`



#### **定义WTForms表单类**

```python
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='名字不能为空!')])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')
```

每一个类属性都表示一个form表单的字段。字段属性的名称将作为对应HTML\<input>元素的name属性及id属性值

> 字段属性名称大小写敏感,不能以下划线或validata开头



**常用的WTForms字段：**

| 字段对象           | 说明                                      |
| ------------------ | ----------------------------------------- |
| StringField        | 文本字段                                  |
| TextAreaField      | 多行文本字段                              |
| PasswordField      | 密码文本字段                              |
| HiddenField        | 隐藏文件字段                              |
| DateField          | 文本字段，值为 datetime.date 文本格式     |
| DateTimeField      | 文本字段，值为 datetime.datetime 文本格式 |
| IntegerField       | 文本字段，值为整数                        |
| DecimalField       | 文本字段，值为decimal.Decimal             |
| FloatField         | 文本字段，值为浮点数                      |
| BooleanField       | 复选框，值为True 和 False                 |
| RadioField         | 一组单选框                                |
| SelectField        | 下拉列表                                  |
| SelectMutipleField | 下拉列表，可选择多个值                    |
| FileField          | 文件上传字段                              |
| SubmitField        | 表单提交按钮                              |
| FormField          | 把表单作为字段嵌入另一个表单              |
| FieldList          | 一组指定类型的字段                        |

**实例化字段类常用参数：**

| 参数       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| label      | 字段\<label>的值，也就是渲染后显示在输入字段前的文章         |
| render_kw  | 一个字典，用来设置对应HTML\<input>标签的属性                 |
| validators | 一个列表，包含一系列验证器，会在表单提交后逐一调用验证表单数据 |
| default    | 字符串或可调用对象，用来为表单设置默认值                     |

验证器（validator）是一系列用于验证字段数据的类，我们在实例化字段类时使用validators关键字来指定附加的验证器列表。验证器从WTForms.validators模块中导入

**常用的WTForms验证器：**

| 验证器                                              | 说明                                     |
| :-------------------------------------------------- | :--------------------------------------- |
| DataRequired(message=None)                          | 确保字段中有数据                         |
| EqualTo(fieldname, message=None)                    | 比较两个字段的值，常用于比较两次密码输入 |
| Length(min=-1, max=-1, message=None)                | 验证输入的字符串长度                     |
| NumberRange(min=None, max=None, message=None)       | 验证输入的值在数字范围内                 |
| URL(reqire_tld=True, message=None)                  | 验证URL                                  |
| AnyOf(values, message=None, values_formatter=None)  | 验证输入值在可选列表中                   |
| NoneOf(values, message=None, values_formatter=None) | 验证输入值不在可选列表中                 |
| Regexp(regex, flags=0, message=None)                | 使用正则表达式验证输入值                 |
| Email(message=None)                                 | 验证Email地址                            |

>  Message参数用来传入自定义错误消息



#### **输出HTML代码**

```python
>>> form = LoginForm()
>>> form.username()
Markup('<input id="username" name="username" required type="text" value="">')
>>> form.password()
Markup('<input id="password" maxlength="128" minlength="8" name="password" required type="password" value="">')
>>> form.submit()
Markup('<input id="submit" name="submit" type="submit" value="Log in">')
>>> form.username.label
Label('username', 'Username')
>>> form.username.label()
Markup('<label for="username">Username</label>')
```



如果要对input标签添加额外的属性有下面2种方法

- 使用render_kw属性

  ```python
  username = StringField('Username', render_kw={'class':'form-control'})
  ```

- 在调用字段时传入

  ```python
  form.username(style='width:200px;', class_='bar')
  ```

  > class是Python的保留关键字，这里我们使用class_来代替class，在模板中调用时可以直接使用class



#### **在模板中渲染表单**

在视图函数里实例化表单类，然后在`render_template()`函数中使用关键字参数form将表单实例传入模板

```python
@app.route('/basic')
def basic():
    form = LoginForm()
    return render_template('basic.html', form=form)
```

```jinja2
<form method="post">
	{{ form.csrf_token}}
    {{ form.username.label }}<br>{{ form.username(class='form-control') }}<br>
    {{ form.password.label }}<br>{{ form.password(class='form-control') }}<br>
    {{ form.remember(class='form-check-input')}}<br>{{form.remember.label}}<br>
    {{ form.submit(class='btn btn-primary')}}<br>
</form>
```



### **处理表单数据**

```python
@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    return render_template('basic.html', form=form)
```



#### **验证表单数据**

```python
@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        ... # 处理post请求
    return render_template('basic.html', form=form)
```

当请求是POST并且表单数据合法时处理post请求，`validate()`方法用来验证表单数据是否合法，返回布尔值1

我们可以用**`validate_on_submit()`**方法合并这两个操作

```python
@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcom home, %s' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)
```



#### **在模板中渲染错误消息**

```jinja2
<form method="post">
	{% from 'macros.html' import form_field %}
    {{ form.csrf_token}}
    {{ form.username.label }}<br>{{ form.username(class='form-control') }}<br>
    {% for message in form.username.error %}
        <small class="danger">{{ message }}</small>
    {% endfor %}
    {{ form.password.label }}<br>{{ form.password(class='form-control') }}<br>
    {% for message in form.password.error %}
        <small class="danger">{{ message }}</small>
    {% endfor %}
    {{ form.remember(class='form-check-input')}}<br>{{form.remember.label}}<br>
    {{ form.submit(class='btn btn-primary')}}<br>
</form>
```

对于验证未通过的字段WTForms会把错误消息添加到表单类的errors属性中，这是一个匹配作为表单字段的类属性到对应的错误消息列表的字典，通过form.字段名.errors获取错误消息



### **表单进阶实践**

#### **设置错误消息语言**

```python
from flask_wtf import FlaskForm
app = Flask(__name__)
app.config['WTF_I18N_ENABLED'] = False

class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']
        
class HelloForm(MyBaseForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField()
```

我们需要将配置变量WTF_I18N_ENABLED设为False，这会让Flask-WTF使用WTForms内置的错误消息翻译。

也可以在实例化表单类时通过meta关键字传入locales值

```python
form = MyForm(meta={'locales':['en_US', 'en']})
```



#### **使用宏渲染表单**

```jinja2
{% macro form_field(field) %}
    {{ field.label }}<br>
    {{ field(**kwargs) }}<br>
    {% if field.errors %}
        {% for error in field.errors %}
            <small class="danger">{{ error }}</small>
        {% endfor %}
    {% endif %}
{% endmacro %}
```

```jinja2
<form method="post">
    {{ form_field(form.username) }}<br>
    {{ form_field(form.password) }}<br>
    {{ form_field(form.remember) }}
    {{ form_field(form.submit) }}
</form>
```



#### **自定义验证器**

1. 行内验证器

   ```python
   from wtforms import SubmitField, IntegerField
   from wtforms.validators import ValidationError
   
   
   class FortyTwoForm(FlaskForm):
       answer = IntegerField('Ith Number', render_kw={'class':'form-control'})
       submit = SubmitField('submit', render_kw={'class':'btn btn-primary'})
   
       def validate_answer(form, field):
           if field.data != 42:
               raise ValidationError('Must be 42')
   
   ```

   当表单内中包含以`validate_字段属性名`形式命名的方法时，在验证字段数据时会同时调用这个方法来验证对应的字段。验证方法接收两个位置参数，依次为form和field，前者为表单类实例，后者是字段对象，我们可以通过field.data获取字段数据

2. 全局验证器

   ```python
   from wtforms.validators import ValidationError
   
   def is_42(form, field):
       if field.data != 42:
           raise ValidationError('Must be 42')
           
   class FortyTwoForm(FlaskForm):
       answer = IntegerField('Ith Number', render_kw={'class':'form-control'}, validators=[is_42])
       submit = SubmitField('submit', render_kw={'class':'btn btn-primary'})
   ```

   但是这种方法无法支持我们传递自定义错误消息，所以我们更推荐下面这种方法

   ```python
   from wtforms.validators import ValidationError
   
   def is_42(message=None):
       if message is None:
           message = 'Must be 42'
   
       def _is_42(form, field):
           if field != 42:
               raise ValidationError(message)
       return is_42
   
   class FortyTwoForm(FlaskForm):
       answer = IntegerField('Ith Number', render_kw={'class':'form-control'}, validators=[is_42()])
       submit = SubmitField('submit', render_kw={'class':'btn btn-primary'})
   ```

   

#### **文件上传**

**上传表单类：**

```python
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField()
```

![image-20220112004412360](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20220112004412360.png)

在表单类中创建文件上传字段时，我们使用扩展Flask-WTF提供的FileField类。

**Flask-WTF提供的上传文件验证器：**

| 验证器                                | 说明                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| FileRequired(message=None)            | 验证是否包含文件对象                                         |
| FileAllowed(upload_set, message=None) | 用来验证文件类型，upload_set参数用来传入包含允许的文件后缀名列表 |

使用HTM 5中的accept属性也可以在客户端实现简单的类型过滤

```html
<input type="file" id="profile_pic", name="profile_pic" accept=".jeg, .jpeg, .png">
```



通过设置Flask内置的配置变量`MAX_CONTENT_LENGTH`可以限制请求报文的最大长度，单位为字节(byte)

```python
# 将最大长度限制为5M
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
```



**表单html文件：** 

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <link href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container-fluid">
    <div class="col-md-8 col-md-offset-2" >
        {% for message in get_flashed_messages() %}
            <div class="blockquote-reverse">{{ message }}</div>
        {% endfor %}
        <form action="" method="post" enctype="multipart/form-data" >
            {{ form.csrf_token }}
            {{ form.photo }}
            {% for message in form.photo.errors %}
                <small>{{ message }}</small>
            {% endfor %}
            {{ form.submit }}
        </form>
    </div>
</div>
</body>
</html>
```



**处理上传文件视图：**

```python
import os
import uuid

app.config["UPLOAD_PATH"] = os.path.join(app.root_path, 'uploads') #指定存储路径

if not os.path.exists(app.config['UPLOAD_PATH']):# 如果存储路径不存在就创建文件夹
    os.makedirs(app.config['UPLOAD_PATH'])

def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename)) # 保存文件
        flash('Upload success')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)

@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')
```

文件对象可以通过`request.files.get('photo')`获取，也可以通过表单对象获取`form.photo.data`

表单通过验证后存储上传的文件时，需要处理文件名通常有3种处理方式

1. 使用源文件
   如果能够确定文件的来源安全可以直接使用原文件名
   `filename = f.filename`

2. 使用过滤后的文件名
   如果文件名中就恶意路径，会导致服务器上的系统文件被覆盖或篡改，还有可能执行恶意脚本。我们可以使用Werkzeug提供的`secure_filename()`函数对文件名过滤

   ```python
   >>> from werkzeug.utils import secure_filename
   >>> secure_filename('avatar!@#//\\%$^&.jpg')
   'avatar_.jpg'
   >>> secure_filename('avatar头像.jpg')
   'avatar.jpg'
   ```

3. 统一重命名
   `secure_filename()`会过滤掉非ASCII字符，如果文件名字都是由非ASCII字符组成，那么会得到一个空文件名

   ```python
   >>> secure_filename('头像.jpg')
   'jpg'
   ```

   为了避免这种情况我们使用pytho内置的uuid模块随机生成文件名

   ```python
   def random_filename(filename):
       ext = os.path.splitext(filename)[1]
       new_filename = uuid.uuid4().hex + ext
       return new_filename
   ```



uploaded.html模板里，我们将传入·的文件名作为url变量，通过`get_file`视图获取文件url

```python
@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
```

```html
<img src="{{ url_for('get_file', filename=filename) }}">
```



#### **多文件上传**

**表单类：**

```python
from wtforms import MultipleFileField, SubmitField

class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField()
```



**视图函数：**

```python
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

@app.route('/multi-upload', methods=['GET', 'POST'])
def multi_upload():
    form = MultiUploadForm()
    if request.method == "POST":
        filenames = []
        # 验证csrf令牌
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error')
            return redirect(url_for('multi_upload'))

        # 检查文件是否存在
        if 'photo' not in request.files:
            flash('This field is required.')
            return redirect(url_for('multi_upload'))

        for f in request.files.getlist('photo'):
            # 检查文件类型
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(
                    os.path.join(
                        app.config["UPLOAD_PATH"], filename
                    )
                )
                filenames.append(filename)
            else:
                flash('Invalid file type')
                return redirect(url_for('multi_upload'))

        flash('Upload success')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)
```



#### **使用Flask-CKEditor集成富文本编辑器**

安装：`pipenv install flask-ckeditor`

实例化Flask-CKEditor提供的CKEditor类，传入程序实例

```python
from flask_ckeditor import CKEditor
ckeditor = CKEditor(app)
```



**Flask-CKEditor常用配置：**

| 配置键               | 默认值     | 说明                                          |
| -------------------- | ---------- | --------------------------------------------- |
| CKEDITOR_SERVE_LOCAL | False      | 设置为True会使用内置的本地资源                |
| CKEDITOR_PKG_TYPE    | ’standard‘ | CKEditor包类型，可选值为basic、standard、full |
| CKEDITOR_LANGUAGE    | ''         | 界面语言，传入ISO 639格式的语言码             |
| CKEDITOR_HEIGHT      | ''         | 编辑器高度                                    |
| CKEDITOR_WIDTH       | ’‘         | 编辑器宽度                                    |

示例：`app.config["CKEDITOR_SERVE_LOCAL"] = True`

**表单类：**

```python
from flask_ckeditor import CKEditorField
class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')
```



**表单html文件：**

```jinja2
{% extends 'base.html' %}
{% from 'macros.html' import form_field %}

{% block content %}
<h1>Integrate CKEditor with Flask-CKEditor</h1>
<form action="" method="post">
    {{ form.csrf_token }}
    {{ form_field(form.title) }}
    {{ form_field(form.body) }}
    {{ form.submit }}
</form>
{% endblock %}

{% block scripts %}
{{ super()}}
{{ ckeditor.load() }}
{% endblock %}
```



**视图函数：**

```python
@app.route('/ckeditor')
def ckeditor():
    form = RichTextForm()
    return render_template('ckeditor.html', form=form)
```

![image-20220112010705948](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20220112010705948.png)



#### **单个表单多个提交按钮**

**表单类：**

```python
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save')
    publish = SubmitField('Publish')
```



**视图函数：**

```python
@app.route('/two-submits', methods=['GET', 'POST'])
def two_submits():
    form = NewPostForm()
    if form.validate_on_submit():
        if form.save.data:
            # ... save it
            flash('You click the "Save" button.')

        if form.publish.data:
            # publish it.
            flash('You click th "Publish"button')

        return redirect(url_for('index'))
    return render_template('2submit.html', form=form)
```

哪个表单的按钮被点击，相应字段的data值就为True



#### **单个页面多个表单：**

##### **单视图处理：**

**表单类：**

```python
class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit1 = SubmitField('Sigh in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1,245)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit2 = SubmitField('Register')
```



**视图函数：**

```python
@app.route('/multi-form', methods=['GET', 'POST'])
def multi_form():
    signin_form = SigninForm()
    register_form = RegisterForm()

    if signin_form.submit1.data and signin_form.validate():
        print('sign in')
        username = signin_form.username.data
        flash('%s, you just submit the Signin Form' % username)
        return redirect(url_for('index'))

    if register_form.submit2.data and register_form.validate():
        print('register')
        username = register_form.username.data
        flash('%s, you just submit the Register Form' % username)
        return redirect(url_for('index'))

    return render_template('2form.html', signin_form=signin_form, register_form=register_form)
```

两个表单的提交字段设置不同的名称，通过对应的名称来判断是哪一个表单提交的请求



##### **多视图处理**

把表单的渲染在单独的视图函数中处理，处理post请求解耦成两个单独的函数

```python
@app.route('/multi-form-multi-view')
def multi_form_multi_view():
    signin_form = SigninForm()
    register_form = RegisterForm()
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)

@app.route('/handle-signin', methods=['POST'])
def handle_signin():
    signin_form = SigninForm()
    if signin_form.validate_on_submit():
        username = signin_form.username.data
        flash('%s, you just submit the Signin Form' % username)
        return redirect(url_for('index'))
    flash_errors(signin_form)
    return redirect(url_for('multi_form_multi_view'))

@app.route('/handle-register', methods=['POST'])
def handle_register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        flash('%s, you just submit the Register Form' % username)
        return redirect(url_for('index'))
    flash_errors(register_form)
    return redirect(url_for('multi_form_multi_view'))
```



给表单设置action属性

```jinja2
{% extends 'base.html' %}
{% from 'macros.html' import form_field%}

{% block content %}
<h2>Sign in form</h2>
<form  method="post" action="{{ url_for('handle_signin') }}">
    {{ signin_form.csrf_token }}
    {{ form_field(signin_form.username) }}
    {{ form_field(signin_form.password) }}
    {{ signin_form.submit1 }}
</form>

<h2>Register form</h2>
<form  method="post" action="{{ url_for('handle_register') }}">
    {{ register_form.csrf_token }}
    {{ form_field(register_form.username) }}
    {{ form_field(register_form.email) }}
    {{ form_field(register_form.password) }}
    {{ register_form.submit2 }}
</form>
{% endblock %}
```



通过专门的函数来发送错误消息

```python
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (getattr(form, field).label.text, error))
```



## **Flask 数据库**

### **ORM魔法**

ORM把底层的SQL数据实体转化成高层的Python对象

- 表 :arrow_right:Python类
- 字段（列）:arrow_right:类属性
- 记录（行）:arrow_right:类实例

如下列SQL语句

```sql
create table contacts(
    name varchar(100) not null,
    phone_number varchar(32)
);
```

转化成ORM

```python
from foo_orm import Model, Column, String

class Contact(Model):
    __tablename__ = 'contacts'
    name = Column(String(100), nulltable=False)
    phone_number = Column(String(32))
```



我们要插入一条记录，需要使用下面的SQL语句

```sql
insert into contacts(name, phone_number)
values('Grey li', '12345678');
```

而ORM子要创建一个Contact类的实例

```python
contact = Contact(name='Grey li', phone_number='12324678')
```



### **使用Flask-SQLAlchemy 管理数据库**

安装：`pipenv install flask-sqlalchemy`

**初始化：**

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL","sqlite:///" + os.path.join(app.root_path, "data.db"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
```

数据库的URI通过配置变量`SQLALCHEMY_TRACK_MODIFICATIONS`s设置，这里默认设置的是sqlite，URI可以配置在环境变量里。初始化后，启动程序会有警告信息，设置`app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False`来忽略警告信息

> 一定要先配置好，再进行初始化



**常用的数据库URI格式：**

| DBMS                 | URI                                                          |
| -------------------- | ------------------------------------------------------------ |
| 模式                 | dialect+driver://username:password@host:port/database        |
| Microsoft SQL Server | mssql://username:password@host:port/databasename             |
| Postgres             | postgresql://username:password@host/databasename             |
| MySQL                | mysql://username:password@host/databasename                  |
| Oracle               | oracle://username:password@host:port/sidname                 |
| SQLite (Unix)        | sqlite:////absolute/path/to/foo.db                           |
| SQLite (Windows)     | sqlite:///absolute\\\path\\\to\\\foo.db 或 r'sqlite:///absolute\\path\\to\\foo.db' |
| SQLite(内存型)       | sqlite:///或sqlite:///:memory:                               |



#### **定义数据库模型**

```python
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
```



**SQLAlchemy 常用的字段类型：**

| 类型名       | python中类型      | 说明                                                |
| ------------ | ----------------- | --------------------------------------------------- |
| Integer      | int               | 普通整数，一般是32位                                |
| SmallInteger | int               | 取值范围小的整数，一般是16位                        |
| BigInteger   | int或long         | 不限制精度的整数                                    |
| Float        | float             | 浮点数                                              |
| Numeric      | decimal.Decimal   | 普通整数，一般是32位                                |
| String       | str               | 变长字符串                                          |
| Text         | str               | 变长字符串，对较长或不限长度的字符串做了优化        |
| Unicode      | unicode           | 变长Unicode字符串                                   |
| UnicodeText  | unicode           | 变长Unicode字符串，对较长或不限长度的字符串做了优化 |
| Boolean      | bool              | 布尔值                                              |
| Date         | datetime.date     | 时间                                                |
| Time         | datetime.datetime | 日期和时间                                          |
| LargeBinary  | str               | 二进制文件                                          |

**常用的SQLAlchemy列选项 ：**

| **选项名**  | **说明**                                          |
| ----------- | ------------------------------------------------- |
| primary_key | 如果为True，代表表的主键                          |
| unique      | 如果为True，代表这列不允许出现重复的值            |
| index       | 如果为True，为这列创建索引，提高查询效率          |
| nullable    | 如果为True，允许有空值，如果为False，不允许有空值 |
| default     | 为这列定义默认值                                  |

默认情况下Flask-SQLAlchemy会根据模型类的名称生成一个表名称生成规则如下

```python
Message  -->  message	# 单个单词转换为小写
FooBar  -->  foo_bar	# 多个单词转换为小写并使用下划线分隔
```



#### **创建数据库和表**

```python
$ flask shell
>>> from app import db
>>> db.create_all()
```



通过下面的方式可以查看模型对应的SQL模式（建表语句）

```python
>>> from app import Note
>>> from sqlalchemy.schema import CreateTable
>>> print(CreateTable(Note.__table__))

CREATE TABLE note (
        id INTEGER NOT NULL,
        body TEXT,
        PRIMARY KEY (id)
)
```



我们可以自己自定义一个flask命令完成这个工作

```python
import click
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
```



### **数据库操作**

数据库操作主要是CRUD，既Create（创建）、Read（读取/查询）、Update（更新）和Delete（删除）

SQLALchemy使用数据库会话来管理数据库操作，这里数据库会话也称为事务，Flask-SQLAlchemy自动帮我们创建会话，通过`db.session`获取。

> 这个session和flask的session无关



#### **CRUD**

1. Create

   ```python
   >>> from app import db
   >>> note1 = Note(body='remember sammy Jankis')
   >>> note2 = Note(body='SHAVE')
   >>> note3 = Note(body='DON \'T BELIEVE HIS LIES,HE IS THE ONE, KILL HIM')
   >>> db.session.add(note1)
   >>> db.session.add(note2)
   >>> db.session.add(note3)
   >>> db.session.commit()
   >>> note1.id
   1
   >>> note1.body
   'remember sammy Jankis'
   >>> note2.body
   'SHAVE'
   >>> note3.body
   "DON 'T BELIEVE HIS LIES,HE IS THE ONE, KILL HIM"
   >>>
   ```

2. Read

   完整的查询遵循下面的模式：

   ```python
   <模型类>.query.<过滤方法>.<查询方法>
   ```

   **常用的SQLAlchemy查询方法：**

   | 查询方法              | 说明                                                         |
   | --------------------- | ------------------------------------------------------------ |
   | all()                 | 返回包含所有查询记录的列表                                   |
   | first()               | 返回查询的第一条记录，如果未找到，则返回None                 |
   | get(id)               | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回None |
   | count()               | 返回查询结果的数量                                           |
   | first_or_404()        | 返回查询的第一条记录，如果未找到，则返回404错误响应          |
   | get_or_404(id)        | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回404错误响应 |
   | paginate()            | 返回一个Pagination对象，可以对记录进行分页处理               |
   | one()                 | 返回第一条记录，且仅允许有一条记录。如果记录数量大于1或小于1，则抛出错误 |
   | one_or_none()         | 类似one()，数量不为一返回None                                |
   | with_parent(instance) | 传入模型类实例作为参数，返回和这个实例相关联的对象           |

   **示例：**

   ```python
   >>> Note.query.all()
   [<Note 1>, <Note 2>, <Note 3>]
   >>> note1 = Note.query.first()
   >>> note1
   <Note 1>
   >>> note1.body
   'remember sammy Jankis'
   >>> note2 = Note.query.get(2)
   >>> note2
   <Note 2>
   >>> note2.body
   'SHAVE'
   >>> Note.query.count()
   3
   ```

   **常用的SQLALchemy过滤方法：**

   | 过滤器      | 说明                                             |
   | ----------- | ------------------------------------------------ |
   | filter()    | 把过滤器添加到原查询上，返回一个新查询           |
   | filter_by() | 把等值过滤器添加到原查询上，返回一个新查询       |
   | limit       | 使用指定的值限定原查询返回的结果                 |
   | offset()    | 偏移原查询返回的结果，返回一个新查询             |
   | order_by()  | 根据指定条件对原查询结果进行排序，返回一个新查询 |
   | group_by()  | 根据指定条件对原查询结果进行分组，返回一个新查询 |

   **示例：**

   ```python
   >>> Note.query.filter(Note.body=='SHAVE').first()
   <Note 2>
   ```

   直接打印对象可以查看对应的SQL语句：

   ```python
   >>> print(Note.query.filter(Note.body=='SHAVE'))
   SELECT note.id AS note_id, note.body AS note_body
   FROM note
   WHERE note.body = ?
   ```

   除了“==”和“!=”还有其他用法
   **LIKE：**
   `filter(Note.body.like('%foo%'))`

   **IN：**
   `filter(Note.body.in_(['foo', 'bar', 'baz']))`

   **NOT IN：**
   `filter(~Note.body.in_(['foo', 'bar', 'baz']))`
   **AND：**

   ```python
   from sqlalchemy import and_
   # 使用and_
   filter(and_(Note.body=='foo', Note.title=='FooBar'))
   
   # 多个表达式，用逗号隔开
   filter(Note.body == 'foo', Note.title=='FooBar')
   
   # 叠加多个filter()/filter_by()
   filter(Note.body == 'foo').filter(Note.title=='FooBar')
   ```

   **OR：**

   ```python
   from sqlalchemy import or_
   filter(or_(Note.body=='foo', Note.title=='FooBar'))
   ```


   比起`filter(),filter_by()`可以使用关键字表达式来指定过滤规则

   ```python
   >>> Note.query.filter_by(body='SHAVE').first()
   <Note 2>
   ```

3. Update

   ```python
   >>> note = Note.query.get(2)
   >>> note.body
   'SHAVE'
   >>> note.body = 'SHAVE LEFT THIGH'
   >>> db.session.commit()
   >>> Note.query.get(2).body
   'SHAVE LEFT THIGH'
   ```

   更新现有的记录时，不要使用`add()`方法

4. Delete

   ```python
   >>> note = Note.query.get(2)
   >>> db.session.delete(note)
   >>> db.session.commit()
   >>> Note.query.count()
   2
   ```



#### **在视图函数里操作数据库**

以一个简单的笔记程序为例

##### **Creat**

```python
# 表单类
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NewNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')
```



**视图函数：**

```python
@app.route('/')
def index():
    notes = Note.query.all()
    form = DeleteNoteForm()
    return render_template('index.html', notes=notes, form=form)

@app.route('/new', methods=['GET', 'POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('You note is saved')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)
```



**表单模板：**

```jinja2
{% extends 'base.html' %}
{% from 'macros.html' import form_field %}
{% block content %}
<h2>New Note</h2>
<form action="" method="post">
    {{ form.csrf_token }}
    {{ form_field(form.body, rows=5, cols=50) }}
    {{ form.submit }}
</form>
{% endblock%}
```

在index.html中，我们添加一个指向创建笔记页面的链接

```html
<h1>Notebook</h1>
<a href="{{ url_for('new_note') }}">New Note</a>
```



##### **Read**

我们将笔记在index.html中展示出来

```python
# index视图
@app.route('/')
def index():
    notes = Note.query.all()
    form = DeleteNoteForm()
    return render_template('index.html', notes=notes, form=form)
```

```jinja2
{# index.html #}

{% extends 'base.html' %}
{% block content %}
<h1>Notebook</h1>
<a href="{{ url_for('new_note') }}">New Note</a>
<h4>{{ notes|length }}</h4>
{% for note in notes %}
    <div class="note">
        <p>{{ note.body }}</p>
    </div>
{% endfor%}
{% endblock%}
```



##### **Update**

创建一个新笔记的表单类，继承自NewNoteForm

```python
class EditNoteForm(NewNoteForm):
    submit = SubmitField('Update')
```



更新笔记内容的视图：

```python
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get_or_404(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('Your note is updated.')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html', form=form)
```

当我们打开修改笔记页面时，这个页面表单必然要包含原来表单的内容。`form.body.data = note.body`，渲染表单时，如果data属性不为空，WTForms会自动把data属性的值添加到表单字段的value中。

修改笔记页面模板：

```jinja2
{% extends 'base.html' %}
{% from 'macros.html' import form_field %}
{% block content %}
<h2>Edit note</h2>
<form action="" method="post">
    {{ form.csrf_token }}
    {{ form_field(form.body, rows=5, cols=50) }}
    {{ form.submit }}
</form>
{% endblock %}
```

在index.html中给每个笔记的下面添加一个编辑按钮

```jinja2
{% extends 'base.html' %}
{% block content %}
<h1>Notebook</h1>
<a href="{{ url_for('new_note') }}">New Note</a>
<h4>{{ notes|length }}</h4>
{% for note in notes %}
    <div class="note">
        <p>{{ note.body }}</p>
        <a href="{{ url_for('edit_note', note_id=note.id) }}" class="btn">Edit</a>
    </div>
{% endfor%}
{% endblock%}
```



##### **Delete**

表单类：

```python
class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')
```



视图函数：

```python
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is deleted')
    else:
        abort(400)
    return redirect(url_for('index'))
```



最终的模板：

```jinja2
{% extends 'base.html' %}
{% block content %}
<h1>Notebook</h1>
<a href="{{ url_for('new_note') }}">New Note</a>
<h4>{{ notes|length }}</h4>
{% for note in notes %}
    <div class="note">
        <p>{{ note.body }}</p>
        <a href="{{ url_for('edit_note', note_id=note.id) }}" class="btn">Edit</a>
        <form action="{{ url_for('delete_note', note_id=note.id) }}" method="post">
            {{ form.csrf_token }}
            {{ form.submit(class='btn') }}
        </form>
    </div>
{% endfor%}
{% endblock%}
```

之所以新建一个删除按钮的表单类，是为避免csrf攻击，并且修改数据类的操作绝不能通过get请求实现

![image-20220112170158294](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20220112170158294.png)



### **定义关系**

#### **配置Python Shell上下文**

每次使用flask shell命令启动Python Shell后都要从APP模块里导入db对象和相应的模型类。我们可以使用**`app.shell_context_processor`**装饰器注册一个shell上下文处理函数

```python
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Note)
```

和模板上下文处理函数一样，也需要返回包含变量和变量值的字典

  

#### **一对多**

以作者和文章关系为例

```python
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20))
    articles = db.relationship('Article')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
```



##### **定义外键**

在Article模型中，我们定义一个author_id字段作为外键，放在“多”的一侧

```python
class Article(db.Model):
    # ......
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
```

`ForeignKey`的参数要为：表名.字段名 的字符串。外键字段名可随意修改



##### **定义关系属性**

在“一”的一侧定义

```python
class Author(db.Model):
  	# ......
    articles = db.relationship('Article')
```

`db.relationship()`关系函数定义为关系属性，我们称之为集合关系属性



##### **建立关系**

下面演示怎样对实际的对象建立关系

```python
>>> foo = AUthor(name='Foo')
>>> spam = Article(title='Spam')
>>> ham = Article(title='Ham')
>>> db.session.add(foo)
>>> db.session.add(spam)
>>> db.session.add(ham)
>>> spam.author_id = 1
>>> ham.author_id = 1
>>> db.session.commit()
```

这是一种方式，但我们更推荐下面这种

```python
>>> foo.articles.append(spam)
>>> foo.articles.append(ham)
>>> db.session.commit()
```

和`append()`相对，对关系属性调用remove()方法可以解除对应关系

```python
>>> foo.articles.remove(spam)
>>> db.session.commit()
```



**常用的 SQLAlchemy关系函数参数：**
![](https://s2.ax1x.com/2019/03/20/AKnfCq.png)



**常用的SQLAlchemy关系记录加载方式(lazy参数可选值)：**

![](https://s2.ax1x.com/2019/03/20/AKn5vT.png)



##### **建立双向关系**

```python
class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    books = db.relationship('Book', back_populates='writer')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    writer = db.relationship('Writer', back_populates='books')
```

使用`back_populates`参数来连接对方，back_populates参数的值需要设为关系另一侧的关系属性名

```python
>>> king = Writer(name='Stephen King')
>>> carrie = Book(name='Carrie')
>>> it = Book(name='It')
>>> db.session.add(king)
>>> db.session.add(carrie)
>>> db.session.add(it)
>>> db.session.commit()

>>> carrie.writer = king
>>> carrie.writer
<Writer 1>
>>> king.books
[<Book 1>]
>>> it.writer=king
>>> king.books
[<Book 1>, <Book 2>]

```

建立双向关系后，除了通过集合属性books来操作关系，我们也可以使用标量属性writer来进行关系操作。



##### **使用backref简化关系定义**

关系函数中的backref参数可以简化双向关系定义。backref参数用来自动为关系另一侧添加关系属性，作为反向引用，赋予的值会作为关系另一侧的关系属性名称。

```python
class Singer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    songs = db.relationship('Song', backref='singer')

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    singer_id = db.Column(db.Integer, db.ForeignKey('singer.id'))  
```



#### **一对一**

我们用国家和首都来演示一对一关系

```python
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    capital = db.relationship('Capital', back_populates='country', uselist=False)

class Capital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country', back_populates='capital')
```

一对一实际上是通过建立双向一对多关系的基础上转化而来。**要确保关系的两侧都是标量属性**，都只返回单个值，所以定义集合属性的关系函数将uselist参数设置为False。

“多”这一侧的本身就是标量关系属性，所以不用改动。

```python
>>> china = Country(name='China')
>>> beijing = Capital(name='Beijing')
>>> china.capital
>>> china.capital = beijing
>>> db.session.add(china)
>>> db.session.add(beijing)
>>> db.session.commit()
>>> china.capital
<Capital 1>
>>> beijing.country
<Country 1>
>>> tokyo = Capital(name='Tokyo')
>>> china.capital.append(tokyo)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'Capital' object has no attribute 'append'
```



#### **多对多**

我们用老师和学生的例子来演示多对多关系

```python
association_table = db.Table(
    'association',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'))
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    grade = db.Column(db.String(20))
    teachers = db.relationship('Teacher', secondary=association_table, back_populates='students')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    office = db.Column(db.String(20))
    students = db.relationship('Student', secondary=association_table, back_populates='teachers')
```

多对多需要创建一个关联表，关联表不存储数据，只用来存储关系两侧模型的外键对应关系

关联表使用db.Table类定义，第一个参数为关联表的名称。我们在关联表中定义两个外键字段，分别存储Student类的主键和Teacher类的主键

在定义关系函数时，多对多需要添加一个secondary参数，值为关联表对象。



### **更新数据库表**

当我们在源代码中修改或新增了模型类时，我们就需要更新数据库

#### **重新生成表**

重新调用`create_all()`方法并不能起到更新表或重新创建表的作用。**如果你并不在意表中的数据**，可以直接使用`drop_all()`方法删除表以及其中的数据，然后再使用`create_all()`方法重新创建

```python
>>> db.drop_all()
>>> db.create_all()
```

为了方便，我们可以自定义命令

```python
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables')
    db.create_all()
    click.echo('Initialized database.')
```



#### **使用Flask-Migrate 迁移数据库**

扩展Flask-Migrate 集成了Alembic，提供了一些flask命令来简化迁移工作

安装：`pipenv install flask-migrate`

**初始化操作：**

```python
from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

1. 创建迁移环境
   `flask db init`

   执行命令后，会在项目根目录下创建一个migrations文件夹，其中包含自动生成的配置文件和迁移版本文件夹

2. 生成迁移脚本

   `flask db migrate -m "add note timestamp"`
   -m 选项用来添加迁移配置信息

3. 更新数据库
   `flask db upgrade`

   如果想回滚迁移，可以使用downgrade命令，它会撤销最后一次迁移在数据库中的改动。`flask db downgrade`



### **数据库进阶实践**

#### **级联操作**

操作某一个对象时，相关的对象也执行某些操作。我们以Post模型和Comment模型为例

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    comments = db.relationship('Comment', back_populates='post', cascade='save-update, merge, delete')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post',back_populates='comments')
```

通过关系函数的`cascade`参数来设置级联行为。设置cascade参数的一侧将被视为父对象。

cascade通常使用多个组合值，级联值之间用逗号分隔

常用的配置组合有一下几种

- save-update、merge（默认值）
- save-update、merge、delete
- all
- all、delete-orphan

没有设置cascade参数时，会使用默认值save-update、merge。

1. **save-update**

   `db.session.add()`方法将Post对象添加到数据库会话时，与Post对象关联的Comment对象也将被添加到数据库会话中。

   ```python
   >>> post1 = Post()
   >>> comment1 = Comment()
   >>> comment2 = Comment()
   >>> db.session.add(post1)
   
   >>> post1 in db.session
   True
   >>> comment1 in db.session
   False
   >>> comment2 in db.session
   False
   
   >>> post1.comments.append(comment1)
   >>> post1.comments.append(comment2)
   >>> comment1 in db.session
   True
   >>> comment2 in db.session
   True
   
   ```

2. **delete**

   cascade参数为delete时，Post对象删除时，与之相关联的Comment对象也一并删除。当需要设置delete级联时，我们将级联值设置为all或save-update、merge、delete

   ```python
   class Post(db.Model):
       # ......
       comments = db.relationship('Comment', back_populates='post', cascade='all')
   ```

   ```python
   >>> post2 = Post()
   >>> comment3 = Comment()
   >>> comment4 = Comment()
   >>> post2.comments.append(comment3)
   >>> post2.comments.append(comment4)
   >>> db.session.add(post2)
   >>> db.session.commit()
   
   >>> Post.query.all()
   [<Post 1>]
   >>> Comment.query.all()
   [<Comment 1>, <Comment 2>]
   >>> post2 = Post.query.get(1)
   >>> db.session.delete(post2)
   >>> db.session.commit()
   >>> Post.query.all()
   []
   >>> Comment.query.all()
   []
   ```

3. **delete-orphan**
   这个模式基于delete级联，必须和delete一起用，通常会设为all、delete-orphan。因为all包含delete，因此cascade参数设置为delete-orphan，它首先会包含delete级联的行为，除此之外，**当某个Post对象与某个Comment对象解除关系时，也会删除该Comment对象**

   ```python
   >>> post3 = Post()
   >>> comment5 = Comment()
   >>> comment6 = Comment()
   >>> post3.comments.append(comment5)
   >>> post3.comments.append(comment6)
   >>> db.session.add(post3)
   >>> db.session.commit()
   
   >>> Post.query.all()
   [<Post 1>]
   >>> Comment.query.all()
   [<Comment 1>, <Comment 2>]
   
   >>> post3.comments.remove(comment5)
   >>> post3.comments.remove(comment6)
   >>> db.session.commit()
   >>> Comment.query.all()
   []
   
   ```

   

#### **事件监听**

SQLALchemy提供了一个**`listens_for()`**装饰器，用来注册事件回调函数

`listens_for()`装饰器主要接收两个参数，target表示监听对象，这个对象可以是模型类、类实例、类属性等。identifier参数表示被监听事件标识符，比如set、append、remove、init_scalar、init_collection等

下面的演示，body字段被修改，edit_time字段就加一

```python
class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    edit_time = db.Column(db.Integer, default=0)

# 事件监听函数
@db.event.listens_for(Draft.body, 'set')
def increment_edit_time(target, value, oldvalue, initiator):
    if target.edit_time is not None:
        target.edit_time += 1

```

```python
>>> draft = Draft(body='init')
>>> db.session.add(draft)
>>> db.session.commit()
>>> draft.edit_time
0
>>> draft.body = 'edited again'
>>> draft.edit_time
1
>>> draft.body = 'edited again'
>>> draft.edit_time
2
```



## **Flask 发送电子邮件**

扩展Flask-Mail 包安装了Python标准库中的smtplib包，简化了在Flask程序中发送电子邮件的过程

安装：`pipenv install flask-mail`

**初始化：**

```python
from flask import Flask
from flask_mail import Mail, Message
app = Flask(__name__)
# ......
mail = Mail(app)
```



### **配置Flask-Mail**

**Flask-Mail常用配置：**

| 配置                | 默认值      | 说明                                                |
| ------------------- | ----------- | --------------------------------------------------- |
| MAIL_SERVER         | localhost   | 电子邮件服务器的主机名或ip地址                      |
| MAIL_PORT           | 25          | 电子邮件服务器的端口                                |
| MAIL_USE_TLS        | False       | 启用传输层安全（Transport Layer Security, TLS）协议 |
| MAIL_USE_SSL        | False       | 启用安全套阶层（Secure Sockets Layer, SSL）协议     |
| MAIL_USERNAME       | None        | 邮件账户的用户名                                    |
| MAIL_PASSWORD       | None        | 邮件账户的密码                                      |
| MAIL_DEBUG          | app.debug   | 是否开启DEBUG                                       |
| MAIL_DEFAULT_SENDER | None        | 邮件发件人，也可在Message对象里指定                 |
| MAIL_MAX_EMAILS     | None        | 邮件批量发送个数上限                                |
| MAIL_SUPPRESS_SEND  | app.testing | 如果为True，则不会真的发送邮件，供测试用            |



如果要对邮件进行加密：

- SSL/TLS加密

  ```python
  MAIL_USE_SSL = True
  MAIL_PORT = 465
  ```

- STARTTLS加密

  ```python
  MAIL_USE_TLS = True
  MAIL_PORT = 587
  ```

> 当不对邮件进行加密时，邮件服务器的端口使用默认的25端口

随着配置逐渐增多，我们改用app.config对象的update() 方法来加载配置

```python
import os
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('Grey Li', os.getenv('MAIL_SERVER'))
)
mail = Mail(app)
```

> 一定要在加载配置之后再实例化Mail类



### **构建邮件数据**

一个邮件至少要包含主题、收件人、正文、发信人这几个元素。发信人已经通过MAIL_DEFAULT_SENDER配置指定了，剩下的通过Message类的构造方法中的subject、recipients、body等关键字传入

```python
from flask import Flask
from flask_mail import Mail, Message
# ......
message = Message(subject, recipients=[Zorn <'Zorn@example.com'>], body='mail text')
mail.sent(message) # 发送邮件
```

发送邮件通过mail对象调用send()方法。



### **电子邮件进阶实践**

#### **提供HTML正文**

一封邮件应该包含纯文本正文和HTML格式正文。HTML格式的正文将被优先读取，如果无法读取HTML格式则会读取纯文本格式

但是大多数主流的邮箱客户端对HTML邮件有各种各样的限制。对于HTML邮件正文的编写，下面是一些常见的“最佳实践”

- 使用Table布局，而不是Div布局
- 使用行内（inline）样式定义
- 尽量使用比较基础的CSS属性，避免使用快捷属性和定位属性
- 邮件正文的宽度不应超过600px
- 避免使用JavaScript代码
- 避免使用背景图片

使用Message类实例来构建邮件时可以在实例化时传入html参数。

```python
message = Message(..., body='纯文本正文', html='<h1>HTML正文</h1>')
```

或者通过类属性message.html指定

```python
message.body = '纯文本正文'
message.html = '<h1>HTML正文</h1>'
```



使用Jinja2模板组织邮件正文
如果邮件中的正文含有动态部分，那么可以用模板来组织邮件

**纯文本邮件模板：**

```html
Hello {{name}},
Thank you for subscribing Flask Weekly!
Enjoy the reading :)

Visit this link to unsubscribe: {{ url_for('unsubscribe', _external=True)}}

```

**HTML邮件模板：**

```html
<div style="width: 580px; padding: 20px;">
    <h3>Hello {{ name }}</h3>
    <p>Thank you for subscribing Flask Weekly!</p>
    <p>Enjoy the reading :)</p>
    <small style="color: #868e96;">
        Click here to <a href="{{ url_for('unsubscribe', _external=True) }}">unsubscribe</a>
    </small>
</div>
```

在视图函数中使用`render_template()`渲染模板

```python
 message.body = render_template('emails/subscribe.txt', name)
 message.html = render_template('emails/subscribe.html', name)
```



#### **异步发送邮件**

我们使用`mail.send()`函数发送邮件时程序会阻塞在那，直到`send_mail()`函数调用完毕。我们可以将发信函数放入后台线程异步执行

```python
from threading import Thread
# ...
def send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

def send_smtp_mail(subject, to, **kwargs):
    message = Message(subject, recipients=[to], sender='Flask Weekly <%s>' % os.getenv('MAIL_USERNAME'))
    message.body = render_template('emails/subscribe.txt', **kwargs)
    message.html = render_template('emails/subscribe.html', **kwargs)
    thr = Thread(target=send_async_mail, args=[app, message])
    thr.start()
    return thr
```

`send()`方法内部使用了current_app变量，而这个变量只在激活的程序上下文中才存在，所以要调用`app.app_context()`手动激活程序上下文



----



最后，下面是将整个发信过程包装成函数后的全部代码

```python
import os
from threading import Thread
from flask import Flask, flash, url_for, redirect, render_template
from flask_mail import Mail, Message
from form import SubscribeForm

app = Flask(__name__)
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('Grey Li', os.getenv('MAIL_SERVER'))
)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
mail = Mail(app)

@app.shell_context_processor
def conten_shell():
    return dict(
        mail=mail,
        Message=Message
    )

def send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

def send_smtp_mail(subject, to, **kwargs):
    message = Message(subject, recipients=[to], sender='Flask Weekly <%s>' % os.getenv('MAIL_USERNAME'))
    message.body = render_template('emails/subscribe.txt', **kwargs)
    message.html = render_template('emails/subscribe.html', **kwargs)
    thr = Thread(target=send_async_mail, args=[app, message])
    thr.start()
    return thr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        flash('Welcome on board')
        send_smtp_mail('Subscribe Success', email, name=name)
        return redirect(url_for('subscribe'))
    return render_template('subscribe.html', form=form)

@app.route('/unsubscribe')
def unsubscribe():
    flash('Want to unsubscrib? No way...')
    return redirect(url_for('subscribe'))
```



## **Flask的一些常用扩展**

### **Bootstrap-Flask**

官方文档：https://bootstrap-flask.readthedocs.io/en/latest

这个东西内置了可以快速渲染Bootstrap样式HTML组件的宏，并提供了内置的Bootstrap资源

安装：`pipenv install bootstrap-flask`

**初始化：**

```python
from flask import Flask
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
bootstrap = Bootstrap(app)
```



#### **加载资源文件**

Bootstrap-Flask在模板中提供了一个bootstrap对象，该对象有两个方法来生成资源引用代码

- 加载CSS文件
  `bootstrap.load_css()`
- 加载Javascript文件（Bootstrap、jQuery、Popper.js）
  `bootstrap.load_js()`

默认从CDN加载，可以将将配置变量`BOOTSTRAP_SERVE_LOCAL`设置为True，当FLASK_ENV环境变量设为development时，Bootstrap-Flask自动使用本地资源

**示例：**

```jinja2
<head>
{{ bootstrap.load_css() }}
</head>
<body>
...
{{ bootstrap.load_js()}}
</body>
```



#### **快捷渲染表单**

Bootstrap-Flask内置了两个用于渲染WTForms表单类的宏

- `form_field()`渲染单个字段，用法跟flask表单文章中自己写的渲染表单的宏一样的
- `render_field()`渲染整个表单

这两个宏都会自动渲染错误消息，渲染表单的验证状态样式。从内置的 bootstrap/form.html模板导入

```jinja2
{% extends 'base.html' %}
{% from 'bootstrap/form.html' import render_form %}

{% block content %}
<div>
	{{ render_form(form) }}
</div>
{% endblock %}
```

它会自动创建form标签，然后依次渲染包括CSRF令牌在内的所有字段。

**render_form()宏常用参数：**

| 参数          | 默认值  | 说明                                                    |
| ------------- | ------- | ------------------------------------------------------- |
| method        | 'post'  | 表单method属性                                          |
| extra_classes | None    | 额外添加的类属性                                        |
| role          | ‘form’  | 表单的role属性                                          |
| form_type     | ‘basic’ | 表单的样式<br />可以是basic、inline或horizontal         |
| button_style  | ‘’      | 设置 SubmitField 的按钮样式。                           |
| render_kw     | {}      | 一个字典，为 \<form> 标签指定自定义属性                 |
| button_map    | {}      | 一个字典，将按钮字段名称映射到 Bootstrap 按钮样式名称。 |
| id            | ''      | 表单的id属性                                            |
| action        | ‘’      | 表单提交的目标URL                                       |



**BootStrap-Flask 内置常用宏：**

![](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/20190508095536193.png)



### **Flask-Moment**

使用Flask-Moment可以本地化日期和时间，这需要服务器提供纯正的时间（naive time），我们可以使用`datetime.utcnow()`方法来生成UTC时间

安装：`pipenv install flask-moment`

**初始化：**

```python
from flask_moment import Moment
app = Flask('__name__')
# ......
moment = Moment(app)
```



#### **使用Flask-Moment集成Moment.js**

Moment.js（https://momentjs.com）是一个用于处理时间和日期的开源Javascript库，它可以对时间和日期进行各种方式的处理。

为了使用Moment.js，我们需要在模板中加载Moment.js资源。

- `moment.include_moment()` 加载Moment.js的Javascript资源
- `moment.include_jquery()`用来加载jQuery

> 可以通过local_js参数传入本地资源的URL，不传则默认使用CDN

```jinja2
{{ moment.include_moment(local_js=url_for('static', filename='js/moment-with-locales.min.js')) }}
```

Moment.js官网提供的文件中moment.min.js仅包含英文语言的时间日期字符，如果需要使用其他语言，需要下载moment-with-locales.min.js。

设置语言为简体中文

```jinja2
{{ moment.locale('zh-cn') }}
```

自动探测客户端语言设置并选择合适区域

```jinja2
{{ moment.locale(auto_detect=True) }}
```



#### **渲染时间日期**

```jinja2
{{ moment(message.timestamp).format('格式字符串') }}
```



**Moment.js 内置格式化字符串：**

<table><thead><tr><th>格式代码</th><th>说明</th><th>返回值例子</th></tr></thead><tbody><tr><td>M</td><td>数字表示的月份，没有前导零</td><td>1到12</td></tr><tr><td>MM</td><td>数字表示的月份，有前导零</td><td>01到12</td></tr><tr><td>MMM</td><td>三个字母缩写表示的月份</td><td>Jan到Dec</td></tr><tr><td>MMMM</td><td>月份，完整的文本格式</td><td>January到December</td></tr><tr><td>Q</td><td>季度</td><td>1到4</td></tr><tr><td>D</td><td>月份中的第几天，没有前导零</td><td>1到31</td></tr><tr><td>DD</td><td>月份中的第几天，有前导零</td><td>01到31</td></tr><tr><td>d</td><td>星期中的第几天，数字表示</td><td>0到6，0表示周日，6表示周六</td></tr><tr><td>ddd</td><td>三个字母表示星期中的第几天</td><td>Sun到Sat</td></tr><tr><td>dddd</td><td>星期几，完整的星期文本</td><td>从Sunday到Saturday</td></tr><tr><td>w</td><td>年份中的第几周</td><td>如42：表示第42周</td></tr><tr><td>YYYY</td><td>四位数字完整表示的年份</td><td>如：2014 或 2000</td></tr><tr><td>YY</td><td>两位数字表示的年份</td><td>如：14 或 98</td></tr><tr><td>A</td><td>大写的AM PM</td><td>AM PM</td></tr><tr><td>a</td><td>小写的am pm</td><td>am pm</td></tr><tr><td>HH</td><td>小时，24小时制，有前导零</td><td>00到23</td></tr><tr><td>H</td><td>小时，24小时制，无前导零</td><td>0到23</td></tr><tr><td>hh</td><td>小时，12小时制，有前导零</td><td>00到12</td></tr><tr><td>h</td><td>小时，12小时制，无前导零</td><td>0到12</td></tr><tr><td>m</td><td>没有前导零的分钟数</td><td>0到59</td></tr><tr><td>mm</td><td>有前导零的分钟数</td><td>00到59</td></tr><tr><td>s</td><td>没有前导零的秒数</td><td>1到59</td></tr><tr><td>ss</td><td>有前导零的描述</td><td>01到59</td></tr><tr><td>X</td><td>Unix时间戳</td><td>1411572969</td></tr></tbody></table>

官方文档：https://momentjs.com/docs/#/displaying/to/

Moments.js还支持输出相对时间，如三分钟前等。这通过`fromNow()`实现，refresh设为True表示不刷新页面的情况下自动更新时间。

```jinja2
{{ moment(message.timestamp).fromNow(refresh=True) }}
```



### **Faker**

Faker用来生成虚拟数据

安装：`pipenv install faker`

**使用：**

```python
>>> from faker import Faker
>>> fake = Faker()
>>> fake.name()
'Blake Sanders'
>>> fake.address()
'330 Carlos Ville\nJamieside, LA 14439'
>>> fake.text()
'Opportunity point pretty send we general course. Property agent music energy. Likely office throw book.'
```

更多用法参考：https://faker.readthedocs.io/en/master/providers.html

在实例化Faker类时可以传入区域字符作为第一个参数（locale）来指定

```python
>>> fake = Faker('zh_CN')
>>> fake.name()
'杜强'
>>> fake.address()
'吉林省上海县城东淮安街X座 728539'
>>>
```



#### **使用Faker实现生成虚拟数据命令**

```python
@app.cli.command()
@click.option('--count', default=20, help='QUantity of messages, default is 20.')
def forge(count):
    '''Generate fake messages.'''
    from faker import Faker
    db.drop_all()
    db.create_all()

    fake = Faker('zh_CN')
    click.echo('Working...')

    for i in range(count):
        message = Message(
            name = fake.name(),
            body = fake.sentence(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(message)

    db.session.commit()
    click.echo('Created %d fake messages' % count)
```



### **Flask-DebugToolbar**

Flask-DebugToolbar提供了一些了调试功能，可以用来看sql语句、配置项选项、资源加载情况等。

安装：`pipenv install flask-debugtoolbar`

**初始化：**

```python
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
toolbar = DebugToolbarExtension(app)
```

Flask-DebugToolbar会拦截重定向请求，`DEBUG_TB_INTERCEPT_REDIRECTS = False`可以关闭这个特性

![image-20220115132236952](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20220115132236952.png)



## **Flask 大型项目结构**

### **使用蓝本模块化程序**

实例化Flask提供的Blueprint类就创建一个蓝本实例。像程序实例一样，我们可以为蓝本实例注册路由、错误处理函数、上下文处理函数、请求处理函数，甚至可以是单独的静态文件文件夹和模板文件夹。蓝本实例同样拥有一个route()装饰器可以用来注册路由。

使用蓝本可以将程序模块化，我们将程序按照功能分离成不同的组件，然后使用蓝本来组织这些组件



1. 创建蓝本

   ```python
   from flask import Blueprint
   auth_bp = Blueprint('blog', __name__)
   ```

   构造方法的第一个参数是蓝本的名称；第2个参数是包或模块的名称，我们可以使用\__name__变量

2. 装配蓝本

   - 视图函数

     ```python
     from flask import Blueprint
     
     auth_bp = Blueprint('auth', __name__)
     
     @auth_bp.route('/loging')
     def login():
         ...
         
     @auth_bp.route('/logout')
     def logout():
         ...
     ```

   - 错误处理函数
     使用蓝本实例的`error_handler()`装饰器可以把错误处理器注册到蓝本上，这些错误处理器只会捕捉访问该蓝本中的路由发生的错误；使用蓝本实例的`app_errorhandler()`装饰器则可以注册一个全局的错误处理器

   - 模板上下文处理函数
     蓝本实例可以使用`context_processor`装饰器注册蓝本特有的模板上下文处理器；使用`app_context_processor`装饰器则会注册程序全局的模板上下文处理器。

     也可以使用`app_template_global()`、`app_template_filter()`和`app_template_test()`来注册全局的模板全局函数、模板过滤器、模板测试器。

3. 注册蓝本

   ```python
   from bluelog.blueprints.auth import auth_bp
   # ...
   app.register_blueprint(auth_bp)
   ```

   使用`Flask.register_blueprint()`方法注册传入的参数是我们创建的蓝本对象。**`url_prefix`**参数为蓝本所有视图URL附加一个URL前缀；

   ```python
   app.register_blueprint(auth_bp, url_prefix='/auth')
   ```

   这时，auth蓝本下的所有视图URL前都会添加一个/auth前缀，例如login视图的URL规则变为/auth/login；

   **`subdomain`**参数为路由设置子域名

   ```python
   app.register_blueprint(auth_bp, subdomain='auth')
   ```

   设置子域名后类似auth.example.com/login的URL才会触发对于视图

4. 蓝本的路由端点

   使用`app.add_url_rule()`方法也可以注册路由

   ```python
   app.add_url_rule('/hello', 'say_hello', say_hello)
   ```

   第一个参数为路由，第2个参数为端点，第三个参数为视图函数对象

   蓝本视图的端点值会变为 `蓝本名.视图函数名`的形式。如生成auth蓝本下的login视图的URL时需要写成`url_for('auth.login')`

5. 蓝本资源
   蓝本可以定义独有的静态文件和模板。这时我们需要把蓝本模块升级为包，在构造文件中创建蓝本实例，并在蓝本包中创建静态文件文件夹static和模板文件夹templates

   要使用蓝本独有的静态文件，需要在定义蓝本时使用static_folder关键字指定版本的静态文件文件夹的路径，参数的值可以是绝对路径或相对于蓝本所在文件夹的相对路径。

   ```python
   auth_bp = Blueprint('auth', __name__, static_folder='static', static_url_path='/auth/static')
   ```

   因为蓝本内置的static路由的URL规则和程序的static路由的URL规则相同，都是/static为了避免冲突我们使用可选的static_url_path参数为蓝本下的static指定了新的URL规则

   > 如果注册蓝本时定义了URL前缀，那么则可以省略static_url_path参数静，态文件路径会自动设为/蓝本前缀/static

   下面的调用会返回“admin/static/style.css”

   ```python
   url_for('admin.static', filename='style.css')
   ```



### **使用类组织配置**

```python
import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
    
    
clas BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15
    # ('theme name', 'display name')
    BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    BLUELOG_SLOW_QUERY_THRESHOLD = 1

    BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
   

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
```

我们把不同的配置划分为不同的配置类，它们都继承自基本配置类

**导入配置：**

```python
from bluebog.settings import config
app = Flask('bluebog')
config_name = os.getenv('FLASK_CONFIG', 'development')
app.config.from_object(config[config_name])
```

我们把配置类型写在.flaskenv文件中，如果没有获取到则使用默认值的development



### **使用工厂函数创建程序实例**

```python
from flask import Flask
from bluelog.settings import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
        
    app = Flask('bluelog')
    app.config.from_object(config[config_name])
    
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(admin_bp, url_prefix='/auth')
    return app
```



#### **初始化扩展**

我们将扩展类的实例化工作集中到 extensions.py 脚本中

**扩展类实例化：**

```python
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
```

我们需要在程序中使用扩展对象时直接从extension时模块导入即可，在工厂函数中我们导入所有扩展对象并调用其`init_app()`方法

```python
from bluelog.extensions import bootstrap, db, moment, mail

def create_app(config_name=None):
    app = Flask('bluelog')
    ...
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    ...
    return app
```



#### **组织工厂函数**

除了扩展初始化操作，还有很多处理函数要注册到程序上，比如错误处理函数、上下文处理函数等等。为了避免把工厂函数弄得太长太复杂，我们可以根据类别把这些代码分离成多个函数，函数接收程序实例app作为参数

```python
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
        
    app = Flask('bluelog')
    app.config.from_object(config[config_name])
    
    register_logging(app)	# 注册日志处理函数
    register_extensions(app)	# 注册扩展（扩展初始化）
    register_bluprints(app)		# 注册蓝本
   	register_commands(app)		# 注册自定义shell命令
    register_errors(app)		# 注册错误处理函数
    register_shell_context(app)	# 注册shell上下文处理函数
    register_template_context(app)	# 注册模板上下文处理函数
    return app


def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    
def register_bluprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)
    
def register_template_context(app):
    pass

def register_errors(app):
     @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400
    # ...
    
def register_commands(app):
    pass
```

> 使用工厂函数时，因为扩展初始化操作分离db.create_all()依赖于程序上下文才能正常执行。**当在其他脚本直接调用db.create_all()或在普通的Python Shell中调用时需要手动激活上下文**





## **Flask 分页、存储密码、Flask-Login、使用CSRFProtect**

### **分页**

使用Bootsstrap-Flask的宏来渲染分页导航部件，SQLALchemy查询对象的paginate方法来实现分页

```python
@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('BLUELOG_POST_PER_PAGE')
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts= pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)
```

page参数代表当前请求页数，per_page为每页返回的记录数

> 如果没有指定page和per_page参数，page默认值为1，per_page默认值为20

**Pagination对象常用属性**

- items 当前页面中的所有记录(比如当前页上有5条记录，items就是以列表形式组织这5个记录)
- query 当前页的query对象(通过query对象调用paginate方法获得的Pagination对象)
- page 当前页码(比如当前页是第5页，返回5)
- prev_num 上一页页码
- next_num 下一页页码
- has_next 是否有下一页 True/False
- has_prev 是否有上一页 True/False
- pages 查询得到的总页数 per_page 每页显示的记录条数
- total 总的记录条数

**常用方法有：**

- prev() 上一页的分页对象Pagination
- next() 下一页的分页对象Pagination
- iter_pages(left_edge=2,left_current=2,right_current=5,right_edge=2)
- iter_pages 用来获得针对当前页的应显示的分页页码列表。



**在模板中渲染：**

使用render_pagination()宏渲染

```jinja2
{% from 'bootstrap4/pagination.html' import render_pagination %}
...
{{ render_pagination(pagination) }}
```

render_pagination()宏常用参数

| 参数       | 默认值 | 说明                                                         |
| ---------- | ------ | ------------------------------------------------------------ |
| pagination | 无     | 分页实例，既Pagination对象                                   |
| endpoint   | None   | 构建分页按钮URL的端点值，默认使用当前请求端点，添加page参数额外地参数将传入url_for()函数 |
| prev       | <<     | 用于“上一页”按钮的符号/文本。如果没有，按钮将被隐藏。        |
| next       | >>     | 用于“下一页”按钮的符号/文本。如果没有，按钮将被隐藏。        |
| ellipses   | ...    | 用于指示页面已被跳过的符号/文本。如果为 None，则不会打印任何指示符。 |
| size       | None   | 可以是“sm”或“lg”，用渲染与小尺寸/大尺寸的分页案例            |
| align      | None   | 分页的对齐方式。可以是“left”、“center”或“right”，默认为“left”。 |
| fragment   | None   | 将 URL 片段添加到链接中，例如#comment。                      |

![image-20220128222600582](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20220128222600582.png)



### **安全存储密码**

```python
>>> from werkzeug.security import generate_password_hash, check_password_hash
>>> password_hash = generate_password_hash('cat')
>>> password_hash
'pbkdf2:sha256:260000$AKdKsybP8Qxm57Gg$5337d4913a45fdf5216158cbb618528ff3910cc23cf336b1254a7ba9f94b8bf0'
>>> check_password_hash(password_hash, 'dog')
False
>>> check_password_hash(password_hash, 'cat')
True
```

Werkzeug在security模块中提供了一个`generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)`函数用于为给定的密码生成散列值，参数method指定计算散列的方法，salt_lengrh参数用来指定盐（salt）的长度，`check_password_hash(pwhash, password)`函数接收散列值和密码作为参数，用来检查密码散列值与密码是否相应。

`generate_password_hash()`函数生成的密码散列的格式：method\$salt$hash

我们可以在存储账号密码的模型中这样写：

```python
from werkzeug.security import generate_password_hash, check_password_hash
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(30))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
```



### **Flask-Login**

官方文档：https://flask-login.readthedocs.io/en/latest/

中文文档：https://flask-login-cn.readthedocs.io/zh/latest/

Flask-login要求表示用户的类必须实现一下这几种属性和方法，以便用来判断用户的认证状态

| 属性/方法        | 说明                                                    |
| ---------------- | ------------------------------------------------------- |
| is_authenticated | 如果用户已经通过认证，返回True，否则返回False           |
| is_active        | 如果允许用户登录，返回True，否则返回False               |
| is_anonymous     | 如果当前用户未登录（匿名用户），返回True，否则返回False |
| get_id()         | 以Unicode形式返回用户的唯一标识符                       |

Flask-Login提供了用户基类UserMixin，它包含了这些方法的属性和默认实现，我们可以让表示用户的类继承至这个类

```python
from flask_login import UserMixin
class Admin(db.Model, UserMixin):
    ...
```

Flask-login支持记住登录状态，通过login_user()中将remember参数设置为True即可实现。这时浏览器会创建一个remember_token的cookie，remember_token cookie默认过期时间为365天，可以通过修改配置变量REMEMBER_COOKIE_DURATION进行设置，设为datetime.timedelta对象即可。



#### **获取当前用户**

我们可以通过Flask-Login提供的current_user对象来判断用户认证状态，它类似于current_app。调用时会返回与当前用户对应的用户模型类对象，因为session中只会存储登录用户的ID，所以为了让它返回对应的用户对象，我们还需要设置一个用户加载函数。这个函数需要使用login_manager.user_loader装饰器，它接收用户id作为参数，返回对应的用户对象

```python
from flask_login import LoginManager
@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin	# 对应用户模型类
    user = Admin.query.get(int(user_id))
    return user
```



#### **登入用户**

```python
from flask_login import login_user, current_user, logout_user, login_required
...
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember) # 登录用户
                return redirect_back()

            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')

    return render_template('auth/login.html', form=form)
```

调用`login_user()`方法登录用户，传入用户对象和remember字段的值作为参数



#### **登出用户**

```python
from flask_login import login_user, current_user, logout_user, login_required
...
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user() # 用户登出
    flash('Logout success', 'info')
    return redirect_back()
```

使用logout_user()函数就可以登出用户，这会清除session中存储的用户id和“记住我”的值



#### **视图保护**

视图保护要求用户登录后才能操作，我们使用`login_required`装饰器在需要登录才能访问的视图前附加这个装饰器，如登出用户功能（用户登录之后才能登出）

```python
from flask_login import login_user, current_user, logout_user, login_required
...
@auth_bp.route('/logout')
@login_required  # 视图保护
def logout():
    logout_user()
    flash('Logout success', 'info')
    return redirect_back()
```

> 当视图函数有多个装饰器时，route()装饰器应该设置于最外层

访问使用了`login_required`的装饰器的视图时程序会自动重定向到登录视图并闪现一个消息提示，在此之前我们需要对`login_view`属性设置登录视图的端点值

```python
login_manager = LoginManager()
...
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'	# 设置消息类别，默认为message
login_manager.login_message_category = '请先登录'	 # 设置提示消息，默认为“please log in to access this page”	
```



### **使用CSRFProtect实现CSRF保护**

一些操作中我们需要考虑到CSRF攻击，这时我们需要将请求通过post方法提交，同时在请求的表单中添加CSRF令牌

```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
# ...
def register_extensions(app):
	csrf.init_app(app)
```

CSRFProtect在模板中提供给了一个`csrf_token()`函数，用来生成CSRF令牌值，我们直接在表单中隐藏这个字段，将这个字段的name值设为csrf_token。

```html
<form action="{{ url_for('admin.delete_post', post_id=post.id, next=request.full_path) }}" method="post">
	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
	<button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('Are you sure?');">Delete</button>
</form>
```



在对应的视图中，CSRFProtect会自动获取并验证CSRF令牌

```python
@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()
```

