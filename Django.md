# Django

## 基本操作

1. 命令行操作

   - 创建django项目

     > django-admin startproject 	项目名

   - 启动django项目

     > 切换到项目目录下
     >
     > python3 manage.py runserver

   - 创建应用

     > python manage.py startapp 	app名

2. 注意事项

   > **<font color=red>创建的应用一定要去配置文件中注册</font>**
   > INSTALLED_APPS = [
   >     'django.contrib.admin',
   >     'django.contrib.auth',
   >     'django.contrib.contenttypes',
   >     'django.contrib.sessions',
   >     'django.contrib.messages',
   >     'django.contrib.staticfiles',
   >     'app01.apps.App01Config',  # 全写
   >   	'app01',			 # 简写
   > ]

   > 如果是命令行创建的项目需要在配置文件中的DIRS加上下面的那句话

   > templates文件夹还需要去配置文件中配置路径
   > 'DIRS': [os.path.join(BASE_DIR, 'templates')]

   

   

## 主要文件介绍

- mysite项目文件夹
  - mysite文件夹
  - settings.py     配置文件
  - urls.py            路由与视图函数对应关系
  - wsgi.py           wsgiref模块
- manage.py            django的入口文件
- db.sqlite3              django自带的sqlite3数据库
- app01文件夹
  - admin.py        django的后台管理
  - apps.py           注册使用
  - migrations文件夹      数据库迁移记录
  - models.py       数据库相关的模型类（orm）
  - tests.py            测试文件
  - views.py           视图



## django三板斧

**urls.urlpatterns:**

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('library/',views.library),
    path('jump/',views.jump),
    path('home/',views.home)
]
```



1. HttpResonse	返回字符串类型

   ```python
   def index(request):
       return HttpResponse('你好啊')
   ```

2. render               返回html文件的

   ```python
   def library(request):
       return render(request,'图书管理系统.html')
   ```

3. redirect             重定向

   ```python
   def jump(requst):
       return redirect('/home/')
   
   def home(requst):
       return HttpResponse('i am home')
   ```

   

## 静态文件配置

> 我们将html文件默认都放在templates文件夹下
> 我们将网站所使用的静态文件默认都放在static文件夹下
>
> 静态文件
> 	前端已经写好了的 能够直接调用使用的文件
> 		网站写好的js文件
> 		网站写好的css文件
> 		网站用到的图片文件
> 		第三方前端框架
> 		...
> 		拿来就可以直接使用的
>
> django默认是不会自动帮你创建static文件夹 需要你自己手动创建

一般情况下我们在static文件夹内还会做进一步的划分处理

> - static
>   - js
>   - css
>   - img
>   - 其他第三方文件

**在浏览器中输入url能够看到对应的资源**
**是因为后端提前开设了该资源的借口**
**如果访问不到资源 说明后端没有开设该资源的借口**

### 文件配置

**在项目目录下的setting.py文件下**

STATIC_URL = '/ooo/'  # 类似于访问静态文件的令牌
如果你想要访问静态文件 你就必须以static开头

/static/bootstrap-3.3.7-dist/js/bootstrap.min.js

/static/令牌
取列表里面从上往下依次查找
    bootstrap-3.3.7-dist/js/bootstrap.min.js
    都没有才会报错

> STATICFILES_DIRS = [
>     os.path.join(BASE_DIR,'static'),
>     os.path.join(BASE_DIR,'static1'),
>     os.path.join(BASE_DIR,'static2'),
> ]

### 静态文件动态解析

> {% load static %}
>  &lt;link rel="stylesheet" href="{% static 'bootstrap-3.3.7-dist/css/bootstrap.min.css' %}"&gt;
>  &lt;script src="{% static 'bootstrap-3.3.7-dist/js/bootstrap.min.js' %}"&gt;&lt;/script&gt;



### 配置用户上传的文件存储位置

> `MEDIA_ROOT = os.path.join(BASE_DIR,'media') ` # 文件名 随你 自己
> 	会自动创建多级目录
>
> 如何开设后端指定文件夹资源
> 	首先你需要自己去urls.py书写固定的代码
> 	`from django.views.static import serve`
> 	`from BBS14 import settings`
>
> 暴露后端指定文件夹资源
>   `re_path(r'^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT})`

 

## request对象方法初始(以登录界面为例)

### 登录界面form表单

form表单默认是get请求数据

form表单action参数

1. 不写 默认朝当前所在的url提交数据
2. 全写 指名道姓
3. 只写后缀 /login/

#### html页面

```html
<body>
<div class="container">
    <div class="row">
        <div class="col-md-8 col-xs-8 col-md-offset-2 col-xs-offset-2">
            <h2 class="text-center">登录</h2>
            <form action="/login/" method="post">
                <p>username:<input type="text" class="form-control" name="username"></p>
                <p>password<input type="password" class="form-control" name="password"></p>
                <input type="submit" value="登录" class="btn btn-success btn-block">
            </form>
        </div>
    </div>
</div>
</body>
```

**在前期我们使用django提交post请求的时候 需要在setting.py中注释掉一行代码**

```python
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### request对象方法

- request.method

  返回请求方式 并且全是大写的字符串形式 <class 'str'>

- request.POST

  获取用户post请求提交的普通数据不包含文件

  - request.POST.get()

    只获取列表最后一个元素

  - request.POST.getlist()

    直接将列表取出

- request.GET

  获取用户提交的get请求数据

  - request.GET.get()

    只获取列表最后一个元素

  - request.GET.getlist() 

    直接将列表取出

#### login函数代码

```python
def login(request):
    if request.method == 'POST':
        temp = request.POST
        temp_get = request.POST.get('username')
        temp_get_list = request.POST.getlist('password')
        print(temp,type(temp))
        print(temp_get,type(temp_get))
        print(temp_get_list,type(temp_get_list))
        return HttpResponse('收到了 宝贝')
    return render(request,'login.html')

'''
<QueryDict: {'username': ['eimago'], 'password': ['123456']}> <class 'django.http.request.QueryDict'>
eimago <class 'str'>
['123456'] <class 'list'>
'''
```



## django连接数据库(MySQL)

**setting.py文件下：**

```python
# 默认用的是sqkite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


#改为

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'day60',
        'USER':'root',
        'PASSWORD':'admin123',
        'HOST':'127.0.0.1',
        'PORT':3306,
        'CHARSET':'utf8'
    }
}

#代码声明
django默认用的是mysqldb模块链接MySQL
    但是该模块的兼容性不好 需要手动改为用pymysql链接
    
    你需要告诉django不要用默认的mysqldb还是用pymysql
    # 在项目名下的init或者任意的应用名下的init文件中书写以下代码都可以
    import pymysql
	pymysql.version_info = (1, 4, 13, "final", 0)
	pymysql.install_as_MySQLdb()
```



## Django ORM

### ORM

对象关系映射，通过python的面向对象代码简单快捷的操作数据库

缺点：封装程度太高，有时sql语句效率偏低 需要你自己些sql语句

> 类  -------------》 表
>
> 对象------------》 记录
>
> 对象属性------》 记录某个字段对应值

### 具体操作方法

在应用下的models.py中书写一个类

```python
class User(models.Model):
    #id int primary_key auto_increment
    id = models.AutoField(primary_key=True, verbose_name='主键')
    
    #username varchar(32)
    username = models.charField(max_length=32, verbose_naem='用户名')
    
    #password int
    password = models.IntegerField(verbose_name='密码')  
```

CharField必须要指定max_length参数，不指定会直接报错

verbose_name该参数是所有字段都有的 就是对该字段的解释



```python
class Author(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField()
```

一张表中必须要有一个主键字段 并且一般情况下都叫id字段，所以orm当你不定义主键字段的时候 orm会自动帮你创建一个名为id的主键字段



**数据库迁移命令：**

- python manage.py makemigrations

  ​	将操作记录记录到小本本上(migrations文件夹)

- python manage.py migrate

  ​	将操作真正的同步到数据库中

**只要修改了models.py中跟数据库相关的代码 就必须重新执行上述两条命令**



## Django操作数据库

### 字段的增删改查

1. 字段的增加

   在models.py文件的对应类中直接添加

   如果表内已经存在数据

   - 将该字段设为空

     ```python
     info = models.CharField(max_length=32,verbose_name='个人简介',null=True)
     ```

   - 直接给字段设置默认值

     ```python
      hobby = models.CharField(max_length=32,verbose_name='兴趣爱好',default='study')
     ```

   - 在终端中给出默认值

2. 字段的修改

   直接修改代码然后执行数据库迁移的两条命令

3. 字段的删除

   直接注释对应代码然后执行数据库迁移的两条命令

### 数据的增删改查

- 查

  ```python
  #有筛选条件
  res = models.User.objects.filter(username=username)
  ```

  返回值你先看成是列表套数据对象的格式
  它也支持索引取值 切片操作 但是不支持负数索引
  它也不推荐你使用索引的方式取值

  ```python
  user_obj = models.User.objects.filter(username=username).first()
  ```

  filter括号内可以携带多个参数 参数与参数之间默认是and关系 你可以把filter联想成where记忆

  ```python
  #查询表里面的全部数据
  # 方式1
  data = models.User.objects.filter()
  print(data)
  # 方式2
  user_queryset = models.User.objects.all()
  ```

  **将数据库数据展示到前端**

  ```python
   def userlist(request):
      user_queryset = models.User.objects.all()
      return render(request,'userlist.html',locals())
  ```

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
  <div class="container">
      <h1 class="text-center">用户数据</h1>
      <div class="row">
          <div class="col-md-8 col-md-offset-2">
              <table class="table table-striped table-hover">
                  <thead>
                      <tr>
                          <th>id</th>
                          <th>user</th>
                          <th>password</th>
                          <th class="text-center">action</th>
                      </tr>
                  </thead>
                  <tbody>
                  {% for user_obj in user_queryset %}
                  <tr>
                  <td>{{ user_obj.id }}</td>
                  <td>{{ user_obj.username }}</td>
                  <td>{{ user_obj.password }}</td>
                  <td class="text-center">
                      <a href="" class="btn btn-success btn-xs">编辑</a>
                      <a href="" class="btn btn-danger btn-xs">删除</a>
                  </td>
                  </tr>
                  {% endfor %}
                  </tbody>
              </table>
          </div>
      </div>
  </div>
  </body>
  </html>
  ```

  

- 增

  ```python
  res = models.User.objects.create(username=username,password=password)
  #返回值就是当期被创建的对象本身
  
  user_obj = models.User(username=username,password=password)
  user_obj.save()
  ```

- 改

  - 方式1：

    ```python
    models.User.object.filter(id=edit_id).update(username=username,password=password)
    ```

    批量更新操作
    将filter查询出来的列表中的所有对象全部更新一遍

  - 方式二：

    ```python
    edit_obj.username = username
    edit_obj.username = password
    edit_obj.save()
    ```

    该方法当字段较多时效率低，无论字段是否更新，都将从头到尾修改一遍

- 删

  ```python
  models.User.objects.filter(id=delet_id).delete()
  ```

  

### 创建表关系

- **models.ForeignKey()**

  ```python
  class Book(models.Model):
      title = models.CharField(max_length=32)
      price = models.DecimalField(max_digits=8,decimal_places=2)
      # 总共八位 小数点后面占两位
      """
      图书和出版社是一对多 并且书是多的一方 所以外键字段放在书表里面
      """
      publish = models.ForeignKey(to='Publish', on_delete=models.CASCADE)
  ```

  如果字段对应的是ForeignKey 那么会orm会自动在字段的后面加_id

- **models.ManyToManyField()**

  ```python
  class Book(models.Model):
      title = models.CharField(max_length=32)
      price = models.DecimalField(max_digits=8,decimal_places=2)
      # 总共八位 小数点后面占两位
   
      publish = models.ForeignKey(to='Publish', on_delete=models.CASCADE)  
      """
      图书和作者是多对多的关系 外键字段建在任意一方均可 但是推荐你建在查询频率较高的一方
      """
      authors = models.ManyToManyField(to='Author')
      '''
    authors是一个虚拟字段 主要是用来告诉orm 书籍表和作者表是多对多关系
      让orm自动帮你创建第三张关系表
      '''
  ```

- **models.OneToOneField()**

  ```python
  class Author(models.Model):
      name = models.CharField(max_length=32)
      age = models.IntegerField()
      """
      作者与作者详情是一对一的关系 外键字段建在任意一方都可以 但是推荐你建在查询频率较高的表中
      """
      author_detail = models.OneToOneField(to='AuthorDetail', on_delete=models.CASCADE)
      """
      OneToOneField也会自动给字段加_id后缀
      所以你也不要自作聪明的自己加_id
      """
  ```

  

## django请求生命周期流程图

![图片未加载！](D:\亿图\保存文件\django请求生命周期流程图.png)



## 路由层

### 路由匹配

**urls.py是url分发器，路由配置文件。在这里面我们会构建起网站的目录，简单来说我们要做的事就是告诉Django，对于某段url该调用哪段代码。**

> 你在输入url的时候会默认加斜杠
>
> django内部帮你做到重定向
> 一次匹配不行
> url后面加斜杠再来一次
>
> APPEND_SLASH = False/True	# 默认是自动加斜杠的

####  path()方法函数定义

path 函数在 Django中的的定义如下所示：

path(route,view,kwargs,name)

它可以接收 4 个参数，其中前两个是必填参数后两个为可选参数。参数解析如下：

1. **route**
   route 是一个匹配 URL 的准则（类似正则表达式）。当 Django 响应一个请求时，它会从 urlpatterns 的第一项开始，按顺序依次匹配列表中的项，直到找到匹配的项，然后执行该项映射的视图函数或者 include 函数分发的下级路由，因此，url 路由的编写在 Django中十分的重要！
2.  **view**
   view 指的是处理当前 url 请求的视图函数。当 Django 匹配到某个路由条目时，自动将封装的 HttpRequest 对象作为第一个参数，被“捕获”的参数以关键字参数的形式，传递给该条目指定的视图函数。
3. **kwargs**
   kwargs 指使用字典关键字传参的形式给关联的目标视图函数传递参数。
4. **name**
   name 给 URL 起个别名，常用于 url 的反向解析，避免在模板中适应硬编码的方式使用嵌入 url。



当使用 path 方法关联视图函数时与 url 方法相比更为简化，也更容易让初学者理解，path 方法引入了类型转化器（converter type）的概念，以此省去了较为复杂的正则表达式匹配路由的方法，实例说明如下：

```python
#1.x url方法
url(r'^test/(?P<year>[0-9]{4})/$', views.year_test),
#2.x path方法
path('test/<int:year>/', views.year_test),
```

> int 支持整数类型的转化，在上述的例子中， year_test 函数接收到的 year 参数就变成整数而不是字符串，从而避免在视图中使用 year=int(year)。

path 函数定义的 &lt;int:year&gt; 规则会捕获到 URL 中的值，映射给视图中的同名参数 year ，并根据转换器将参数值转换为指定的类型，这里对应 int 大于等于 0 的整数。之所以使用转化器，有以下两个原因：

- 第一是可以将捕获到的字符值转换为对应的类型；
- 第二是对 URL 中传值的一种限制，避免视图处理出错

#### path方法类型转化器

Django 默认支持 5 个类型转换器，在大多数情况下，绝对可以满足我们的正常业务需求，如果不能，Django 同样提供了自定义转换器。下面介绍 Django 默认支持的转换器，如下所示：

- str，匹配除了路径分隔符（/）之外的非空字符串，这是默认的形式；
- int，匹配正整数，包含0；
- slug，匹配字母、数字以及横杠、下划线组成的字符串；
- uuid，匹配格式化的 uuid，如 075194d3-6885-417e-a8a8-6c931e272f00；
- path，匹配任何非空字符串，包含了路径分隔符。

#### re_path正则表达式匹配

如果上述的 paths 和 converters 还是无法满足需求，Django 2.x 也支持我们使用正则表达式来捕获值，在这里需要使用 re_path()，而不是前面介绍的 path()。我们使用带命名的正则表达式分组，语法如下：

(?P&lt;name&gt;pattern) 

其中，尖括号里的name为分组名，pattern为正则表达式。re_path()同样包含于`django.urls`模块中，所以同样使用如下方式进行导入。示例如下：

```python
from django.urls import path, re_path  #导入re_path
from . import views
urlpatterns = [    
    re_path('test/(?P<year>[0-9]{4})/', views.year_test),
    re_path('test/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.month_test),
    re_path('test/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[^/]+)/', views.article_test),
```

re_path 其实相当于 Django 1.x 中的 url 方法。它们两的用法是一致的，所以在这里就不多加赘述了。

#### 无名分组

分组:就是给某一段正则表达式用小括号扩起来

```python
re_path(r'^test/(\d+)/',views.test)

def test(request,xx):
    print(xx)
    return HttpResponse('test')
```

无名分组就是将括号内正则表达式匹配到的内容当作位置参数传递给后面的视图函数

#### 有名分组

可以给正则表达式起一个别名

```python
re_path(r'^testadd/(?P<year>\d+)',views.testadd)

def testadd(request,year):
    print(year)
    return HttpResponse('testadd')
```

有名分组就是将括号内正则表达式匹配到的内容当作关键字参数传递给后面的视图函数

**ps: 有名分组和无名分组不能混用 但是同一个分组可以使用N多次**



### 反向解析

<font color='red'>通过一些方法得到一个结果 该结果可以直接访问对应的url触发视图函数</font>

先给路由与视图函数起一个别名

```python
path(r'func_kkk/',views.func,name='my_name')
```

##### 前端反向解析：

```html
<a href="{% url 'my_name' %}">111</a>
```

##### 后端反向解析：

```python
from django.shortcuts import reverse
reverse('my_name')
```

##### 无名分组反向解析：

```python
# 无名分组反向解析
re_path(r'^index/(\d+)/',views.index,name='xxx')

# 前端
	{% url 'xxx' 123 %}
# 后端
	reverse('xxx', args=(1,))
```

##### 有名分组反向解析

```python
 path(r'^func/(?P<year>\d+)/',views.func,name='ooo')
# 前端
	<a href="{% url 'ooo' year=123 %}">111</a>  #了解
	<a href="{% url 'ooo' 123 %}">222</a>  	#记忆

# 后端	
	# 有名分组反向解析 写法1  了解
   print(reverse('ooo',kwargs={'year':123}))
   # 简便的写法  减少脑容量消耗 记跟无名一样的操作即可
   print(reverse('ooo',args=(111,)))
```

**分组反向解析这个数字写代码的时候应该放什么？**
<font color='red'>**数字一般情况下放的是数据的主键值  数据的编辑和删除**</font>



### 路由分发

> django的每一个应用都可以有自己的templates文件urls.py static文件夹
>
> 正是基于上述的特点 django能够非常好的做到分组开发（每一个人只写自己的app）
>
> 作为组长 只需要将手下书写的app全部拷贝到一个新的django项目中 然后在配置文件里面注册所有的app再利用路由分发的特点将所有的app整合起来
>
> 当一个django项目中的url特别多的时候 总路由urls.py代码非常冗余不好维护
> 这个时候也可以利用路由分发来减轻总路由的压力
>
> 利用路由分发之后 总路由不再干路由与视图函数的直接对应关系
> 而是做一个分发处理
> 	识别当前url是属于哪个应用下的 直接分发给对应的应用去处理

#### 具体步骤

1. 在不同的app目录下创建urls.py文件，将根目录下的urls.py内容拷贝到app目录下的urls.py文件下，再写该app的路由匹配

   - app01

     ```python
     from django.urls import path,re_path
     from app01 import views
     
     urlpatterns = [
         path('reg/',views.reg)
     ]
     ```

   - app02

     ```python
     from django.urls import path,re_path
     from app01 import views
     
     urlpatterns = [
         path('reg/',views.reg)
     ]
     ```

2. 在根目录下的urls.py文件下进行路由分发

   ```python
   from django.contrib import admin
   from django.urls import path,re_path,include
   from app01 import urls as app01_urls
   from app02 import urls as app02_urls
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       # 1.路由分发
       path('app01/',include(app01_urls)),  # 只要url前缀是app01开头 全部交给app01处理
       path('app02/',include(app02_urls))   # 只要url前缀是app02开头 全部交给app02处理
   
       # 2.终极写法  推荐使用
       path('app01/',include('app01.urls')),
       path('app02/',include('app02.urls'))
   ]
   ```

3. 最后别忘了在根目录下的setting.py下注册app

注意：总路由里面的如果使用re_path进行路由匹配，千万不能加$结尾



### 名称空间

当多个应用出现了相同的别名 我们研究反向解析会不会自动识别应用前缀

正常情况下的反向解析是没有办法自动识别前缀的

- 总路由

  ```python
  path('app01/',include('app01.urls')),
  path('app02/',include('app02.urls'))
  ```

- 解析的时候

  ```python
  # app01
  app_name = 'app01'
  urlpatterns = [
      path('reg/',views.reg,name='reg')
  ]
  
  # app02
  app_name = 'app02'
  urlpatterns = [
      path('reg/',views.reg,name='reg')
  ]
  
  reverse('app01:reg')
  reverse('app02:reg')
  
  {% url 'app01:reg' %}
  {% url 'app02:reg' %}
  ```
  
  

## 视图层

### 三板斧

- HttpResponse
  返回字符串类型
- render
  返回html页面 并且在返回给浏览器之前还可以给html文件值
- redirect
  重定向

视图函数必须要返回一个HttpResponse对象



**render简单内部原理**

```python
from django.template import Template,Context
res = Template('<h1>{{ user }}</h1>')
con = Context({'user':{'username':'jason','password':123}})
ret = res.render(con)
print(ret)
return HttpResponse(ret)
```



### JsonResponse

```python
from django.http import JsonResponse
def ab_json(request):
    user_dict = {'username':'jason好帅哦,我好喜欢!','password':'123','hobby':'girl'}

    l = [111,222,333,444,555]
    # 先转成json格式字符串
    # json_str = json.dumps(user_dict,ensure_ascii=False)
    # 将该字符串返回
    # return HttpResponse(json_str)
    # 读源码掌握用法
    #return JsonResponse(user_dict,json_dumps_params={'ensure_ascii':False})
    return JsonResponse(l,safe=False)  
    # 默认只能序列化字典 序列化其他需要加safe参数	
```



### 文件上传

**form表单上传文件类型的数据**

1. **method必须指定成post**
2. **enctype必须换成formdata**

```python
def ab_file(request):
    if request.method == 'POST':
        # print(request.POST)  # 只能获取普通的简直对数据 文件不行
        print(request.FILES)  # 获取文件数据
        # <MultiValueDict: {'file': [<InMemoryUploadedFile: u=1288812541,1979816195&fm=26&gp=0.jpg (image/jpeg)>]}>
        file_obj = request.FILES.get('file')  # 文件对象
        print(file_obj.name)
        with open(file_obj.name,'wb') as f:
            for line in file_obj.chunks():  # 推荐加上chunks方法 其实跟不加是一样的都是一行行的读取
                f.write(line)

    return render(request,'form.html')
```



### request对象方法

|          方法           |                 作用                  |
| :---------------------: | :-----------------------------------: |
|     request.method      |          获取form表单的方法           |
|       request.GET       |           获取get请求的数据           |
|      request.POST       |          获取post请求的数据           |
|      request.FILES      |          获取form表单的文件           |
|      request.body       |    原生的浏览器发过来的二进制数据     |
|      request.path       |                获取url                |
|    request.path_info    |                获取url                |
| request.get_full_path() |     获取完整的url及问号后面的参数     |
|    request.is_ajax()    | 判断当前请求是否是ajax请求 返回布尔值 |



### CBV与FBV

视图函数既可以是函数也可以是类

**python代码**

```python
# CBV路由
path('login/',views.MyLogin.as_view())


CBV类
from django.views import View

class MyLogin(View):
    def get(self,request):
        return render(request,'form.html')

    def post(self,request):
        return HttpResponse('post方法')
```



## 模板层

模板语法可以向前端传递后端的python数据

### 传值

{{}}	变量相关

{%%}	逻辑相关

对象被展示到html页面上 就类似于执行了打印操作会触发\__str__方法

传递函数名会自动加括号调用 但是模版语法不支持给函数传额外的参数:{{ func }}

传类名的时候也会自动加括号调用(实例化){{ MyClass }}

内部能够自动判断出当前的变量名是否可以加括号调用 如果可以就会自动执行  针对的是函数名和类名

 django模版语法的取值 是固定的格式 只能采用“句点符” .	

```html
<p>{{ d.username }}</p>
<p>{{ l.0 }}</p>
<p>{{ d.hobby.3.info }}</p>
```



### 过滤器

过滤器类似于python的内置函数，用来把视图传入的变量值加以修饰后再显示，具体语法如下

> {{ 变量名|过滤器名:传给过滤器的参数 }}

**常用内置过滤器：**

1. default

   如果一个变量值是False或者为空，使用default后指定的默认值，否则，使用变量本身的值，如果value为NULL则输出“nothing”

   ```django
   {{ value|default:"nothing" }}
   ```

2. length

   返回值的长度。它对字符串、列表、字典等容器类型都起作用，如果value是 ['a', 'b', 'c', 'd']，那么输出是4

   ```django
   {{ value|length }}
   ```

3. filesizeformat

   将值的格式化为一个"人类可读的"文件尺寸(如13KB、4.1 MB、102bytes等等），如果 value 是 12312312321，输出将会是 11.5 GB

   ```django
   {{ value|filesizeformat }}
   ```

4. date

   将日期按照指定的格式输出，如果value=datetime.datetime.now(),按照格式Y-m-d则输出2019-02-02

   ```django
   {{ value|date:"Y-m-d" }}　
   ```

5. slice

   对输出的字符串进行切片操作，顾头不顾尾,如果value=“egon“，则输出"eg"

   ```python
   {{ value|slice:"0:2" }}　
   ```

6. truncatechars

   如果字符串字符多于指定的字符数量，那么会被截断。截断的字符串将以可翻译的省略号序列（“...”）结尾，如果value=”hello world egon 嘎嘎“，则输出"hello...",注意8个字符也包含末尾的3个点

   ```django
   {{ value|truncatechars:8 }}
   ```

7. truncatewords

   同truncatechars，但truncatewords是按照单词截断，注意末尾的3个点不算作单词，如果value=”hello world egon 嘎嘎“，则输出"hello world ..."

   ```django
   {{ value|truncatewords:2 }}
   ```

8. safe

   出于安全考虑，Django的模板会对HTML标签、JS等语法标签进行自动转义,例如value="&lt;script>alert(123)&lt;/script>"，模板变量{{ value }}会被渲染成&lt;script&gt;alert(123)&lt;/script&gt;交给浏览器后会被解析成普通字符”&lt;script>alert(123)&lt;/script>“，失去了js代码的语法意义，但如果我们就想让模板变量{{ value }}被渲染的结果又语法意义，那么就用到了过滤器safe，比如value='<a href="https://www.baidu.com">点我啊</a>'，在被safe过滤器处理后就成为了真正的超链接，不加safe过滤器则会当做普通字符显示’<a href="https://www.baidu.com">点我啊</a>‘

   ```django
   {{ value|safe }}
   ```



### 标签

#### for标签:

```django
{% for person in person_list %}
<p>
    {{person.name}}
</p>
{% endfor %}
```

1. **遍历字典：**

   ```django
   {% for key,val in dic.items %}
   	<p>
           {{key}}:{{val}}
   </p>
   {% endfor %}
   ```

2. **循环序号可以通过{{ forloop }}显示**　

   - forloop.counter		当前循环的索引值（从1开始）
   - forloop.counter0      当前循环的索引值（从0开始）
   - forloop.revcounter         当前循环的倒序索引值（从1开始） 
   - forloop.revcounter0        当前循环的倒序索引值（从0开始）
   - forloop.first              当前循环是第一次循环则返回True，否则返回False 
   - forloop.last               当前循环是最后一次循环则返回True，否则返回False
   -  forloop.parentloop         本层循环的外层循环 

3. **for标签可以带有一个可选的{% empty %},可迭代对象为空时执行empty子句**

   ```django
   {% for person in person_list %}
       <p>{{ person.name }}</p>
   
   {% empty %}
       <p>sorry,no person here</p>
   {% endfor %}
   ```

#### if标签：

条件为真时if的子句才会生效，条件也可以是一个变量，if会对变量进行求值，在变量值为空、或者视图没有为其传值的情况下均为False

```django
{% if num > 100 or num < 0 %}
    <p>无效</p>
{% elif num > 80 and num < 100 %}
    <p>优秀</p>
{% else %}
    <p>凑活吧</p>
{% endif %}

if语句支持 and 、or、==、>、<、!=、<=、>=、in、not in、is、is not判断。
```

if语句支持 and 、or、==、>、<、!=、<=、>=、in、not in、is、is not判断。

#### with标签

with标签用来为一个复杂的变量名起别名

```django
{% with li.1.upper as v %}
    {{ v }}
{% endwith %}
```

#### csrf_token标签

当用form表单提交POST请求时必须加上标签{% csrf_token%}，该标签用于防止跨站伪造请求

```django
<form action="" method="POST">
    {% csrf_token %}
    <p>用户名：<input type="text" name="name"></p>
    <p>密码：<input type="password" name="pwd"></p>
    <p><input type="submit" value="提交"></p>
</form>
```

具体工作原理为：

1. 在GET请求到form表单时，标签{% csrf_token%}会被渲染成一个隐藏的input标签，该标签包含了由服务端生成的一串随机字符串,如&lt;input type="hidden" name="csrfmiddlewaretoken" value="dmje28mFo...OvnZ5"&gt;

2. 在使用form表单提交POST请求时，会提交上述随机字符串，服务端在接收到该POST请求时会对比该随机字符串，对比成功则处理该POST请求，否则拒绝，以此来确定客户端的身份



### 自定义过滤器、标签、inclusion_tag

**三步走：**

1. 在应用下创建一个名字**必须**为**templatetags**文件夹

2. 在该文件夹内创建任意名称的py     eg:mytage.py

3. 在该py文件内**必须**先书写下面两句话

   ```python
   from django import template
   register = template.Library()
   ```

#### 自定义过滤器

```python
@register.filter(name='baby')
def my_sum(v1,v2):	#参数最多只能有两个
    return v1 + v2

# 使用
{% load mytage %}
<p>{{ n|baby:666 }}</p>
```

#### 自定义标签

```python
@register.simple_tag(name='plus')
def index(a,b,c,d):
    return '%s-%s-%s-%s'%(a,b,c,d)

#使用
<p>{% plus 'eimago' 123 123 123 %}</p>
```

#### 自定义标签扩展之mark_safe

我们可以用内置的标签safe来让标签内容有语法意义，如果我们想让自定义标签处理的结果也有语法意义，则不能使用内置标签safe了，需要使用mark_safe，可以实现与内置标签safe同样的功能

```python
from django.utils.safestring import mark_safe

@register.simple_tag(name='inp')
def my_input_tag(id, name):
    res = "<input type='text' id='%s' name='%s' />" % (id, name)
    return mark_safe(res)

<p>{% inp 123 'eimago' %}</p>
```



#### 自定义inclusion_tag

**内部原理：**

> 先定义一个方法 
> 在页面上调用该方法 并且可以传值
> 该方法会生成一些数据然后传递给一个html页面
> 之后将渲染好的结果放到调用的位置

```python
@register.inclusion_tag('left_menu.html')
def left(n):
    data = ['第{}项'.format(i) for i in range(n)]
    return locals() # 将data传递给left_menu.html
	
    # return {'data':data}  # 将data传递给left_menu.html

#使用
{% left 5 %}
```

**使用场景：**当html页面某一个地方的页面需要传参数才能够动态的渲染出来，并且在多个页面上都需要使用到该局部 那么就考虑将该局部页面做成inclusion_tag形式。



### 模板的继承

你自己先选好一个你要想继承的模版页面

```django
{% extends 'home.html' %}
```

继承了之后子页面跟模版页面长的是一模一样的 你需要在模版页面上提前划定可以被修改的区域

```django
{% block content %}
	模版内容
{% endblock %}
```

子页面就可以声明想要修改哪块划定了的区域

```django
{% block content %}
	子页面内容	
{% endblock %}
```

一般情况下模版页面上应该至少有三块可以被修改的区域

1. css区域
2. html区域
3. js区域

```django
{% block css %}

{% endblock %}


{% block content %}

{% endblock %}


{% block js %}

{% endblock %}
```

每一个子页面就都可以有自己独有的css代码 html代码 js代码



### 模板的导入

将页面的某一个局部当成模块的形式，哪个地方需要就可以直接导入使用即可

```django
{% include 'wasai.html' %}
```



### 模板字符串

> 在前端中使用js中的变量`userName` `conTent`

```django
let temp = `
<li class="list-group-item">                     <span>${userName}</span>&nbsp;
<div style="margin-top: 10px">
${conTent}
</div>
</li>
`
```

``是tab上面的反引号



## 模型层

### 测试脚本

当你只是想测试django中的某一个py文件内容 那么你可以不用书写前后端交互的形式，而是直接写一个测试脚本即可

**测试环境的准备：**

去manage.py中拷贝前四行代码 然后自己写两行

```python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "day64.settings")
    import django
    django.setup()
    # 在这个代码块的下面就可以测试django里面的单个py文件了
```

### 必知必会13条

1. all()    查询所有数据

2. filter()    带有过滤条件的查询

3. get()    直接拿数据对象但是条件不存在直接报错

4. first()    拿queryset里面的第一个元素

   ```python
   res = models.User.objects.all().first()
   ```

5. last()    拿最后一条元素

   ```python
   res = models.User.objects.all().last()
   ```

6. values()    可以指定获取数据字典(列表套字典)

   ```python
   res = models.User.objects.values('name','register_time')
   print(res)
   
   '''
   <QuerySet [{'name': 'eimago', 'register_time': datetime.date(2021, 8, 10)}, {'name': 'eimago', 'register_time': datetime.date(2021, 8, 10)}, {'name': 'jason', 'register_time': datetime.date(2021, 8, 10)}, {'name': 'obito', 'register_time': datetime.date(2021, 8, 19)}, {'name': 'hataki', 'register_time': datetime.date(2021, 8, 18)}]>
   '''
   ```

7. values_list()    可以指定获取数据字典(列表套元组)

   ```python
   res = models.User.objects.values_list('name','register_time')
   print(res)
   
   '''
   <QuerySet [('eimago', datetime.date(2021, 8, 10)), ('eimago', datetime.date(2021, 8, 10)), ('jason', datetime.date(2021, 8, 10)), ('obito', datetime.date(2021, 8, 19)), ('hataki', datetime.date(2021, 8, 18))]>
   
   '''
   ```

8. distinct()    去重

   ```python
   res = models.User.objects.values('name','age').distinct()
   print(res)
   
   '''
   <QuerySet [{'name': 'eimago', 'age': 18}, {'name': 'jason', 'age': 20}, {'name': 'obito', 'age': 30}, {'name': 'hataki', 'age': 21}]>
   
   '''
   ```

   **去重一定要是一模一样的数据**
   **如果带有主键那么肯定不一样 你在往后的查询中一定不要忽略主键**

9. order_by()    排序，默认升序

   ```python
   res = models.User.objects.order_by('age')
   
   #降序
   res = models.User.objects.order_by('-age')
   ```

10. reverse()    反转，**前提是数据已经排过序列了**

    ```python
    res = models.User.objects.order_by('age').reverse()
    ```

11. count()    统计当前数据的个数

    ```python
    res = models.User.objects.count()
    ```

12. exclude()    排出在外

    ```python
    res = models.User.objects.exclude(age='18')
    ```

13. exists()    判断数据是否存在，返回值为布尔值

    基本用不到因为数据本身就自带布尔值  返回的是布尔值



### 双下划线查询

1. __gt    大于

   ```python
   models.User.objects.filter(age__gt=35)
   # 年龄大于35岁的数据
   ```

2. __lt    小于

   ```python
   res = models.User.objects.filter(age__lt=35)
   # 年龄小于35岁的数据
   ```

3. __gte    大于等于

   ```python
   models.User.objects.filter(age__gte=32)
   # 年龄大于等于32岁的数据
   ```

4. __lte    小于等于

   ```python
   models.User.objects.filter(age__lte=32)
   # 年龄小于等于32岁的数据
   ```

5. __in    包含

   ````python
   models.User.objects.filter(age__in=[18,32,40])
   # 年龄是18 或者 32 或者40
   ````

6. __range    范围

   ```python
   models.User.objects.filter(age__range=[18,40])
   # 年龄在18到40岁之间的  闭区间
   ```

7. __contains    模糊查询

   ```python
   models.User.objects.filter(name__contains='s')
   # 查询出名字里面含有s的数据  模糊查询
   
   # 忽略大小写
   models.User.objects.filter(name__icontains='p')
   ```

8. __startwith    以特定字符开头

   ```python
   models.User.objects.filter(name__startswith='j')
   ```

9. __endwith    以特定字符结尾

   ```python
   models.User.objects.filter(name__endswith='j')
   ```

10. 日期查询

    ```python
     # 查询出注册时间是 2020 1月
    res = models.User.objects.filter(register_time__month='1')
    
    res = models.User.objects.filter(register_time__year='2020')
    ```

    

### 外键的增删改

#### 一对多

- 增

  ```python
  publish_obj = models.Publish.objects.filter(pk='2').first()
  models.Book.objects.create(name='三国演义',price=128.23,publish_id=1)
  ```

- 删

  ```python
  models.Publish.objects.filter(pk=1).delete()
  ```

- 改

  ```python
  publish_obj = models.Publish.objects.filter(pk='2').first()
  
  # 传对象
  models.Book.objects.filter(pk=2).update(publish=publish_obj)
  
  # 传主键
  models.Book.objects.filter(pk=2).update(publis_id=2)
  ```

#### 多对多

- 增

  ```python
  book_obj = models.Book.objects.filter(pk=2).first()
  
  # 书籍id为1的书籍绑定一个主键为1 的作者
  book_obj.author.add(1) # 就类似于你已经到了第三张关系表了
  
  # 也可以一次绑定多个
  book_obj.author.add(1,2,3) 
  
  # 通过传对象修改
  author_obj = models.Author.objects.filter(pk=3).first()
  author_obj1 = models.Author.objects.filter(pk=2).first()
  book_obj.author.add(author_obj,author_obj1)
  ```

  add给第三张关系表添加数据
  括号内既可以传数字也可以传对象 并且都支持多个

- 删

  ```python
  book_obj = models.Book.objects.filter(pk=1).first()
  book_obj.authors.remove(2)
  book_obj.authors.remove(1,3)
  
  author_obj = models.Author.objects.filter(pk=2).first()
  author_obj1 = models.Author.objects.filter(pk=3).first() 
  book_obj.authors.remove(author_obj,author_obj1)
  ```

  remove括号内既可以传数字也可以传对象 并且都支持多个

- 改

  ```python
  book_obj = models.Book.objects.filter(pk=1).first()
  book_obj.authors.set([1,2])
  book_obj.authors.set([3])
  ```

  括号内必须给一个可迭代对象

- 清空

  ```python
  book_obj = models.Book.objects.filter(pk=1).first()
  book_obj.authors.clear()
  ```

  在第三张关系表中清空某个书籍与作者的绑定关系

### 多表查询

#### 正反向的概念

> 外键字段在我手上那么，我查你就是正向
> 外键字段如果不在手上，我查你就是反向
>
> book >>>外键字段在书那儿(正向)>>> publish
> publish	>>>外键字段在书那儿(反向)>>>book
>
> 一对一和多对多正反向的判断也是如此
>
> 正向查询按字段
> 反向查询按表名小写_set

#### 子查询(基于对象的跨表查询)

1. 查询数据主键为1的出版社

   ```python
   book_obj = models.Book.objects.filter(pk=1).first()
   res = book_obj.publish
   print(res)
   print(res.name)
   print(res.addr)
   ```

2. 查询书籍主键为2的作者

   ```python
   book_obj = models.Book.objects.filter(pk=2).first()
   res = book_obj.authors.all() 
   print(res)
   ```

3. 查询作者jason的电话号码

   ```python
   author_obj = models.Author.objects.filter(name='jason').first()
   res = author_obj.author_detail
   print(res)
   print(res.phone)
   print(res.addr)
   ```

4. 查询出版社时东方出版社的书

   ```python
   publish_obj = models.Publish.objects.filter(name='东方出版社').first()
   res = publish_obj.book_set.all()
   print(res)
   ```

5. 查询作者是jason写过的书

   ```python
   author_obj = models.Author.objects.filter(name='jason').first()
   res = author_obj.book_set.all()
   print(res)
   ```

6. 查询手机号是110的作者姓名

   ```python
   author_detail_obj = models.AuthorDetail.objects.filter(phone=110).first()
   res = author_detail_obj.author
   print(res.name)
   ```

**正向什么时候需要加.all()?**

> 当你的结果可能有多个的时候就需要加.all()
> 如果是一个则直接拿到数据对象
> book_obj.publish
> book_obj.authors.all()
> author_obj.author_detail

**反向什么时候加__set?**

>当你的查询结果可以有多个的时候 就必须加\__set.all()
>当你的结果只有一个的时候 不需要加\__set.all()



#### 联表查询(基于双下划线的跨表查询)

1. 查询jason的手机号和作者姓名

   ```python
   res = models.Author.objects.filter(name='jason').values('author_detail__phone','name')
   
   # 反向
   res = models.AuthorDetail.objects.filter(author__name='jason').values('phone','author__name')
   ```

2. 查询书籍主键为1的出版社名称和书的名称

   ```python
   res = models.Book.objects.filter(pk=1).values('title','publish__name')
   
   # 反向
   res = models.Publish.objects.filter(book__id=1).values('name','book__title')
   ```

3. 查询书籍主键为1的作者姓名

   ```python
   res = models.Book.objects.filter(pk=1).values('authors__name')
   
   # 反向
   res = models.Author.objects.filter(book__id=1).values('name')
   ```

4. 查询书籍主键是1的作者的手机号

   ```python
   res = models.Book.objects.filter(pk=1).values('authors__author_detail__phone')
   ```




### 聚合查询

aggregate

聚合查询通常情况下都是配合分组一起使用的
只要是跟数据库相关的模块 
基本上都在django.db.models里面
如果上述没有那么应该在django.db里面

```python
from app01 import models
from django.db.models import Max,Min,Sum,Count,Avg
# 1 所有书的平均价格
# res = models.Book.objects.aggregate(Avg('price'))
# print(res)
# 2.上述方法一次性使用
res = models.Book.objects.aggregate(Max('price'),Min('price'),Sum('price'),Count('pk'),Avg('price'))
print(res)
```



### 分组查询

annotate

```python
# 1.统计每一本书的作者个数
 print(   models.Book.objects.annotate(author_num=Count('author__id')).values('name','author_num')
)

# 2.统计每个出版社卖的最便宜的书的价格
print(
models.Publish.objects.annotate(price_min=Min('book__price')).values('name','price_min')
)

# 3.统计不止一个作者的图书
print(
models.Book.objects.annotate(author_num=Count('author')).filter(author_num__gt=1).values('name','author_num')
)

# 4.查询每个作者出的书的总价格
print(
models.Author.objects.annotate(price_sum=Sum('book__price')).values('name','price_sum')
)
```



### F查询

能够帮助你直接获取到表中某个字段对应的数据

```python
from django.db.models import F
res = models.Book.objects.filter(maichu__gt=F('kucun'))
print(res)


# 2.将所有书籍的价格提升500块
models.Book.objects.update(price=F('price') + 500)


# 3.将所有书的名称后面加上爆款两个字
"""
在操作字符类型的数据的时候 F不能够直接做到字符串的拼接
"""
from django.db.models.functions import Concat
from django.db.models import Value
models.Book.objects.update(title=Concat(F('title'), Value('爆款')))

models.Book.objects.update(title=F('title') + '爆款')  # 所有的名称会全部变成空白
```

### Q查询

```python
# 1.查询卖出数大于100或者价格小于600的书籍
res = models.Book.objects.filter(maichu__gt=100,price__lt=600)
"""filter括号内多个参数是and关系"""

from django.db.models import Q
res = models.Book.objects.filter(Q(maichu__gt=100),Q(price__lt=600))  # Q包裹逗号分割 还是and关系

res = models.Book.objects.filter(Q(maichu__gt=100)|Q(price__lt=600))  # | or关系

res = models.Book.objects.filter(~Q(maichu__gt=100)|Q(price__lt=600))  # ~ not关系
```

**高阶用法:**将查询条件的左边也变成字符串的形式

```python
q = Q()
q.connector = 'or' # 默认为and关系，改为or关系
q.children.append(('maichu__gt',100))
q.children.append(('price__lt',600))
res = models.Book.objects.filter(q)  
print(res)
```



### django中如何开启事务

**ACID：**

1. 原子性    不可分割的最小单位
2. 一致性    跟原子性是相辅相成
3. 隔离性    事务之间互相不干扰
4. 持久性    事务一旦确认永久生效

```python
# 目前你只需要掌握Django中如何简单的开启事务
# 事务
from django.db import transaction
try:
    with transaction.atomic():
        # sql1
        # sql2
        ...
        # 在with代码快内书写的所有orm操作都是属于同一个事务
except Exception as e:
	print(e)
print('执行其他操作')
```



### orm常用字段及参数

| 字段                | 参数                                                         | 对应mysql数据类型                                            |
| ------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ |
| AutoField           | 主键字段 primary_key=True                                    | 无                                                           |
| CharField           | verbose_name	字段的注释<br /> max_length		长度      | varchar                                                      |
| IntegerField        |                                                              | int                                                          |
| BigIntegerField     |                                                              | bigint                                                       |
| DecimalField        | max_digits=8<br/>decimal_places=2                            | float(8,2)                                                   |
| EmailFiled          |                                                              | varchar(254)                                                 |
| DateField           |                                                              | date                                                         |
| DateTimeField       | auto_now:每次修改数据的时候都会自动更新当前时间<br/>auto_now_add:只在创建数据的时候记录创建时间后续不会自动修改了 | datetime                                                     |
| BooleanField(Field) | 该字段传布尔值(False/True)                                   | 布尔值类型<br />数据库里面存0/1                              |
| TextField(Field)    |                                                              | 该字段可以用来存大段内容(文章、博客...)  没有字数限制        |
| FileField(Field)    | upload_to = "/data"                                          | 给该字段传一个文件对象，会自动将文件保存到/data目录下然后将文件路径保存到数据库中<br/>/data/a.txt |



### 自定义字段的使用

```python
class MyCharField(models.Field):
    def __init__(self,max_length,*args,**kwargs):
        self.max_length = max_length
        # 调用父类的init方法
        super().__init__(max_length=max_length,*args,**kwargs)  # 一定要是关键字的形式传入

    def db_type(self, connection):
        """
        返回真正的数据类型及各种约束条件
        :param connection:
        :return:
        """
        return 'char(%s)'%self.max_length

        # 自定义字段使用
myfield = MyCharField(max_length=16,null=True)
```

### 数据库查询优化

orm语句的特点:
	惰性查询
	如果你仅仅只是书写了orm语句 在后面根本没有用到该语句所查询出来的参数
	那么orm会自动识别 直接不执行

#### only与defer	

```python
res = models.Book.objects.all()
print(res)  # 要用数据了才会走数据库

# 想要获取书籍表中所有书的名字
res = models.Book.objects.values('title')
for d in res:
	print(d.get('title'))
# 你给我实现获取到的是一个数据对象 然后点title就能够拿到书名 并且没有其他字段

res = models.Book.objects.only('title')
res = models.Book.objects.all()
print(res)  
# <QuerySet [<Book: 三国演义爆款>, <Book: 红楼梦爆款>, <Book: 论语爆款>, <Book: 聊斋爆款>, <Book: 老子爆款>]>
for i in res:
	print(i.title)  # 点击only括号内的字段 不会走数据库
	print(i.price)  # 点击only括号内没有的字段 会重新走数据库查询而all不需要走了

res = models.Book.objects.defer('title')  # 对象除了没有title属性之外其他的都有
for i in res:
    print(i.price)
    """
    defer与only刚好相反
        defer括号内放的字段不在查询出来的对象里面 查询该字段需要重新走数据
        而如果查询的是非括号内的字段 则不需要走数据库了

    """
```

#### select_related与prefetch_related

跟跨表操作有关

```python
res = models.Book.objects.all()
for i in res:
	print(i.publish.name)  # 每循环一次就要走一次数据库查询
    
res = models.Book.objects.select_related('authors')  # INNER JOIN

"""
    select_related内部直接先将book与publish连起来 然后一次性将大表里面的所有数据
    全部封装给查询出来的对象
        这个时候对象无论是点击book表的数据还是publish的数据都无需再走数据库查询了

    select_related括号内只能放外键字段  如一对多 一对一
        多对多不行！！
"""

res = models.Book.objects.prefetch_related('publish')  # 子查询
    """
    prefetch_related该方法内部其实就是子查询
        将子查询查询出来的所有结果也给你封装到对象中
        给你的感觉好像也是一次性搞定的
    """
for i in res:
    print(i.publish.name)
```



更多的参考[https://www.cnblogs.com/Dominic-Ji/p/9203990.html]

没有的自己上网查



### choices参数(数据库字段设计常见)

> 用户表	
> 	性别
> 	学历
> 	工作经验
> 	是否结婚
> 	是否生子
> 	客户来源
>
> 针对某个可以列举完全的可能性字段，我们应该如何存储
>
> 只要某个字段的可能性是可以列举完全的，那么一般情况下都会采用choices参数

```python
class User(models.Model):
    username = models.CharField(max_length=32)
    age = models.IntegerField()
    # 性别
    gender_choices = (
        (1,'男'),
        (2,'女'),
        (3,'其他'),
    )
    gender = models.IntegerField(choices=gender_choices)
    
    score_choices = (
        ('A','优秀'),
        ('B','良好'),
        ('C','及格'),
        ('D','不合格'),
    )
    # 保证字段类型跟列举出来的元祖第一个数据类型一致即可
    score = models.CharField(choices=score_choices,null=True)
    
    """
    该gender字段存的还是数字 但是如果存的数字在上面元祖列举的范围之内
    那么可以非常轻松的获取到数字对应的真正的内容
    
    1.gender字段存的数字不在上述元祖列举的范围内容
    2.如果在 如何获取对应的中文信息
    """
    
models.User.objects.create(username='jason',age=18,gender=1)

models.User.objects.create(username='egon',age=85,gender=2)

models.User.objects.create(username='tank',age=40,gender=3)
# 存的时候 没有列举出来的数字也能存（范围还是按照字段类型决定）

models.User.objects.create(username='tony',age=45,gender=4)

# 取
user_obj = models.User.objects.filter(pk=1).first()
print(user_obj.gender)
# 只要是choices参数的字段 如果你想要获取对应信息 固定写法 get_字段名_display()
print(user_obj.get_gender_display())

user_obj = models.User.objects.filter(pk=4).first()

# 如果没有对应关系 那么字段是什么还是展示什么
print(user_obj.get_gender_display()) 
```



### 多对多三种创建方式

- 全自动:利用orm自动帮我们创建第三张关系表

  ```python
  class Book(models.Model):
      name = models.CharField(max_length=32)
      authors = models.ManyToManyField(to='Author')
  class Author(models.Model):
      name = models.CharField(max_length=32)
  ```

  - 优点:代码不需要你写 非常的方便 还支持orm提供操作第三张关系表的方法
  - 不足之处:第三张关系表的扩展性极差(没有办法额外添加字段...)

- 纯手动

  ```python
  class Book(models.Model):
      name = models.CharField(max_length=32)
      
  class Author(models.Model):
      name = models.CharField(max_length=32)
    
  class Book2Author(models.Model):
      book_id = models.ForeignKey(to='Book')
      author_id = models.ForeignKey(to='Author')
  ```

  - 优点:第三张表完全取决于你自己进行额外的扩展
  - 不足之处:需要写的代码较多，不能够再使用orm提供的简单的方法

- 半自动

  ```python
  class Book(models.Model):
      name = models.CharField(max_length=32)
      authors = models.ManyToManyField(to='Author',
                                       through='Book2Author',
                                       through_fields=('book','author')
  class Author(models.Model):
          name = models.CharField(max_length=32)
          # books = models.ManyToManyField(to='Book',
          #                                  through='Book2Author',
          #                                  through_fields=('author','book')
          #                                  )
  class Book2Author(models.Model):
          book = models.ForeignKey(to='Book')
          author = models.ForeignKey(to='Author')
  ```

  > through_fields字段先后顺序
  >     判断的本质：
  >         通过第三张表查询对应的表 需要用到哪个字段就把哪个字段放前面
  >     你也可以简化判断
  >         当前表是谁 就把对应的关联字段放前面

  - 可以使用orm的正反向查询 但是没法使用add,set,remove,clear这四个方法



### django自带的序列化组件

需求:在前端给我获取到后端用户表里面所有的数据 并且要是列表套字典

```python
from django.core import serializers
def ab_ser(request):
    user_queryset = models.User.objects.all()
    # [{},{},{},{},{}]
    # user_list = []
    # for user_obj in user_queryset:
    #     tmp = {
    #         'pk':user_obj.pk,
    #         'username':user_obj.username,
    #         'age':user_obj.age,
    #         'gender':user_obj.get_gender_display()
    #     }
    #     user_list.append(tmp)
    # return JsonResponse(user_list,safe=False)
    # return render(request,'ab_ser.html',locals())

    # 序列化
    res = serializers.serialize('json',user_queryset)
    """会自动帮你将数据变成json格式的字符串 并且内部非常的全面"""
    return HttpResponse(res)
```



### 批量插入

**bulk_create**

```python
def ab_pl(request):
    # 先给Book插入一万条数据
    # for i in range(10000):
    #     models.Book.objects.create(title='第%s本书'%i)
    # # 再将所有的数据查询并展示到前端页面
    book_queryset = models.Book.objects.all()

    # 批量插入
    # book_list = []
    # for i in range(100000):
    #     book_obj = models.Book(title='第%s本书'%i)
    #     book_list.append(book_obj)
    # models.Book.objects.bulk_create(book_list)
    """
    当你想要批量插入数据的时候 使用orm给你提供的bulk_create能够大大的减少操作时间
    :param request: 
    :return: 
    """
    return render(request,'ab_pl.html',locals())
```



## 分页器

#### 推导过程

```python
"""
总数据100 每页展示10 需要10
总数据101 每页展示10 需要11
总数据99 每页展示10  需要10

如何通过代码动态的计算出到底需要多少页？


在制作页码个数的时候 一般情况下都是奇数个		符合中国人对称美的标准
"""
# 分页
    book_list = models.Book.objects.all()

    # 想访问哪一页
    current_page = request.GET.get('page',1)  # 如果获取不到当前页码 就展示第一页
    # 数据类型转换
    try:
        current_page = int(current_page)
    except Exception:
        current_page = 1
    # 每页展示多少条
    per_page_num = 10
    # 起始位置
    start_page = (current_page - 1) * per_page_num
    # 终止位置
    end_page = current_page * per_page_num

    # 计算出到底需要多少页
    all_count = book_list.count()

    page_count, more = divmod(all_count, per_page_num)
    if more:
        page_count += 1

    page_html = ''
    xxx = current_page
    if current_page < 6:
        current_page = 6
    for i in range(current_page-5,current_page+6):
        if xxx == i:
            page_html += '<li class="active"><a href="?page=%s">%s</a></li>'%(i,i)
        else:
            page_html += '<li><a href="?page=%s">%s</a></li>'%(i,i)



    book_queryset =  book_list[start_page:end_page]
    
"""
django中有自带的分页器模块 但是书写起来很麻烦并且功能太简单
所以我们自己想法和设法的写自定义分页器

上述推导代码你无需掌握 只需要知道内部逻辑即可

我们基于上述的思路 已经封装好了我们自己的自定义分页器 
之后需要使用直接拷贝即可
"""
```

### 自定义分页器的拷贝及使用

> 当我们需要使用到非django内置的第三方功能或者组件代码的时候
> 我们一般情况下会创建一个名为utils文件夹 在该文件夹内对模块进行功能性划分
> 	utils可以在每个应用下创建 具体结合实际情况
>
> 我们到了后期封装代码的时候 不再局限于函数
> 还是尽量朝面向对象去封装
>
> 我们自定义的分页器是基于bootstrap样式来的 所以你需要提前导入bootstrap
> 	bootstrap 版本 v3
> 	jQuery		版本 v3

#### 拷贝代码：

```python
class Pagination(object):
    def __init__(self, current_page, all_count, per_page_num=10, pager_count=11):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        page_html_list.append('''
                    <nav aria-label='Page navigation>'
                    <ul class='pagination'>
                ''')
        first_page = '<li><a href="?page=%s">首页</a></li>' % (1)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            prev_page = '<li><a href="?page=%s">上一页</a></li>' % (self.current_page - 1,)

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = '<li class="active"><a href="?page=%s">%s</a></li>' % (i, i,)
            else:
                temp = '<li><a href="?page=%s">%s</a></li>' % (i, i,)
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?page=%s">下一页</a></li>' % (self.current_page + 1,)
        page_html_list.append(next_page)

        last_page = '<li><a href="?page=%s">尾页</a></li>' % (self.all_pager,)
        page_html_list.append(last_page)
        # 尾部添加标签
        page_html_list.append('''
                                           </nav>
                                           </ul>
                                       ''')
        return ''.join(page_html_list)
```



#### **后端：**

```python
book_queryset = models.Book.objects.all()
current_page = request.GET.get('page',1)
all_count = book_queryset.count()

# 1 传值生成对象
page_obj = Pagination(current_page=current_page,all_count=all_count)
# 2 直接对总数据进行切片操作
page_queryset = book_queryset[page_obj.start:page_obj.end]
# 3 将page_queryset传递到页面 替换之前的book_queryset
```

#### **前端：**

```django
{% for book_obj in page_queryset %}
    <p>{{ book_obj.title }}</p>
    <nav aria-label="Page navigation">
</nav>
{% endfor %}
{#利用自定义分页器直接显示分页器样式#}
{{ page_obj.page_html|safe }}
```



## forms组件

### 前戏

> 写一个注册功能
> 	获取用户名和密码 利用form表单提交数据
> 	在后端判断用户名和密码是否符合一定的条件
> 		用户名中不能含有金瓶梅
> 		密码不能少于三位
> 	如何符合条件需要你将提示信息展示到前端页面

#### 前端：

```html
<form action="" method="post">
    <p>username:
        <input type="text" name="username">
        <span style="color: red">{{ back_dic.username }}</span>
    </p>
    <p>password:
        <input type="text" name="password">
        <span style="color: red">{{ back_dic.password }}</span>
    </p>
    <input type="submit" class="btn btn-info">
</form>
```



#### 后端：

```python
def ab_form(request):
    back_dic = {'username':'','password':''}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if '金瓶梅' in username:
            back_dic['username'] = '不符合社会主义核心价值观'
        if len(password) < 3:
            back_dic['password'] = '不能太短 不好!'
    """
    无论是post请求还是get请求
    页面都能够获取到字典 只不过get请求来的时候 字典值都是空的
    而post请求来之后 字典可能有值
    """
    return render(request,'ab_form.html',locals())
```

> forms组件
> 	能够完成的事情
> 			1.渲染html代码
> 			2.校验数据
> 			3.展示提示信息
>
> 为什么数据校验非要去后端 不能在前端利用js直接完成呢？
> 	数据校验前端可有可无
> 	但是后端必须要有!!!
> 	
>
> 因为前端的校验是弱不禁风的 你可以直接修改
> 或者利用爬虫程序绕过前端页面直接朝后端提交数据
>
> 购物网站	
> 	选取了货物之后 会计算一个价格发送给后端 如果后端不做价格的校验
> 	
>
> 实际是获取到用户选择的所有商品的主键值
> 然后在后端查询出所有商品的价格 再次计算一遍
> 如果跟前端一致 那么完成支付如果不一致直接拒绝

### 基本使用

```python
from django import forms

class MyForm(forms.Form):
    # username字符串类型最小3位最大8位
    username = forms.CharField(min_length=3,max_length=8)
    # password字符串类型最小3位最大8位
    password = forms.CharField(min_length=3,max_length=8)
    # email字段必须符合邮箱格式  xxx@xx.com
    email = forms.EmailField()
```

### 校验数据

1. 将带校验的数据组织成字典的形式传入即可

   ```python
   form_obj = views.MyForm({'username':'jason','password':'123','email':'123'})
   ```

2. 判断数据是否合法		

   注意该方法只有在所有的数据**全部合法**的情况下才会返回True

   ```python
   form_obj.is_valid()
   False
   ```

3. 查看所有校验通过的数据

   ```python
   form_obj.cleaned_data
   {'username': 'jason', 'password': '123'}
   ```

4. 查看所有不符合校验规则以及不符合的原因

   ```python
   form_obj.errors
   {
     'email': ['Enter a valid email address.']
   }
   ```

5. 校验数据只校验类中出现的字段 多传不影响 多传的字段直接忽略

   ```python
   form_obj = views.MyForm({'username':'jason','password':'123','email':'123@qq.com','hobby':'study'})
   form_obj.is_valid()
   True
   ```

6. 校验数据 默认情况下 类里面所有的字段都必须传值

   ```python
   form_obj = views.MyForm({'username':'jason','password':'123'})
   form_obj.is_valid()
   False
   ```

### 渲染标签

> forms组件只会自动帮你渲染获取用户输入的标签(input select radio checkbox)
> 不能帮你渲染提交按钮

#### 后端

```python
def index(request):
    # 1 先产生一个空对象
    form_obj = MyForm()
    # 2 直接将该空对象传递给html页面
    return render(request,'index.html',locals())
```

#### 渲染的三种方式

1. 代码书写极少，封装程度太高 不便于后续的扩展 一般情况下只在本地测试使用

   ```django
   {{ form_obj.as_p }}
   {{ form_obj.as_ul }}
   {{ form_obj.as_table }}
   ```

2. 可扩展性很强 但是需要书写的代码太多  一般情况下不用

   ```django
   <p>{{ form_obj.username.label }}:{{ form_obj.username }}</p>
   <p>{{ form_obj.password.label }}:{{ form_obj.password }}</p>
   <p>{{ form_obj.email.label }}:{{ form_obj.email }}</p>
   ```

3. 代码书写简单 并且扩展性也高(推荐使用)

   ```django
   {% for form in form_obj %}
   	<p>{{ form.label }}:{{ form }}</p>
   {% endfor %}
   ```

> label属性默认展示的是类中定义的字段首字母大写的形式
> 也可以自己修改 直接给字段对象加label属性即可
> username = forms.CharField(min_length=3,max_length=8,label='用户名')

### 展示提示信息

#### 后端

```python
def index(request):
    # 1 先产生一个空对象
    form_obj = MyForm()
    if request.method == 'POST':
        # 获取用户数据并且校验
        """
        1.数据获取繁琐
        2.校验数据需要构造成字典的格式传入才行
        ps:但是request.POST可以看成就是一个字典
        """
        # 3.校验数据
        form_obj = MyForm(request.POST)
        # 4.判断数据是否合法
        if form_obj.is_valid():
            # 5.如果合法 操作数据库存储数据
            return HttpResponse('OK')
        # 5.不合法 有错误
    # 2 直接将该空对象传递给html页面
    return render(request,'index.html',locals())

'''
1.必备的条件 get请求和post传给html页面对象变量名必须一样
2.forms组件当你的数据不合法的情况下 会保存你上次的数据 让你基于之前的结果进行修改
更加的人性化
'''
```

#### 前端

```django
{% for form in form_obj %}
        <p>
            {{ form.label }}:{{ form }}
            <span style="color: red">{{ form.errors.0 }}</span>
        </p>
{% endfor %}
```

> 浏览器会自动帮你校验数据 但是前端的校验弱不禁风
> 如何让浏览器不做校验
> 	`<form action="" method="post" novalidate>`

#### 针对错误的提示信息还可以自己自定制

```python
class MyForm(forms.Form):
    # username字符串类型最小3位最大8位
    username = forms.CharField(min_length=3,max_length=8,label='用户名',
                               error_messages={
                                   'min_length':'用户名最少3位',
                                   'max_length':'用户名最大8位',
                                   'required':"用户名不能为空"
                               }
                               )
    # password字符串类型最小3位最大8位
    password = forms.CharField(min_length=3,max_length=8,label='密码',
                               error_messages={
                                   'min_length': '密码最少3位',
                                   'max_length': '密码最大8位',
                                   'required': "密码不能为空"
                               }
                               )
    # email字段必须符合邮箱格式  xxx@xx.com
    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'invalid':'邮箱格式不正确',
                                 'required': "邮箱不能为空"
                             }
                             )
```

### 钩子函数(HOOK)

> 在特定的节点自动触发完成响应操作
>
> 钩子函数在forms组件中就类似于第二道关卡，能够让我们自定义校验规则
>
> 在forms组件中有两类钩子
> 	1.局部钩子
> 		当你需要给单个字段增加校验规则的时候可以使用
> 	2.全局钩子
>   	当你需要给多个字段增加校验规则的时候可以使用

#### 实际案例

> 1.校验用户名中不能含有666				只是校验username字段  局部钩子
>
> 2.校验密码和确认密码是否一致			password confirm两个字段	全局钩子

<font color='red'>钩子函数  在**类里面**书写方法即可</font>

####  局部钩子

```python
# 钩子函数  在类里面书写方法即可
    def clean_username(self):
        # 获取到用户名
        username = self.cleaned_data.get('username')
        if '666' in username:
            # 提示前端展示错误信息
            self.add_error('username','光喊666是不行滴～')
        # 将钩子函数钩去出来数据再放回去
        return username

    
```

#### 全局钩子

```python
	def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not confirm_password == password:
            self.add_error('confirm_password','两次密码不一致')
        # 将钩子函数钩出来数据再放回去
        return self.cleaned_data
```



### forms组件其他参数及补充知识点

#### 字段

- label		字段名
- error_messages   自定义报错信息
- initial  默认值
- required  控制字段是否必填

#### 添加样式

```python
class MyForm(forms.Form):
    username = forms.CharField(min_length=3,max_length=8)
    
    # 这里input框的type属性为passwor所以widget参数我们写的就是PasswordInput
    # 同样的还有
    	#TextInput
		#DateInput
		#RadioInput
		#CheckboxInput
    password = forms.CharField(min_length=3,max_length=8,
                              widget=forms.widgets.PasswordInput(attrs={'class':'form-control c1 c2'}))
    confirm_password = forms.CharField(min_length=3,max_length=8)
    email = forms.EmailField()

# 多个属性值的话 直接空格隔开即可
```

#### 其他类型渲染

```python
# radio
    gender = forms.ChoiceField(
        choices=((1, "男"), (2, "女"), (3, "保密")),
        label="性别",
        initial=3,
        widget=forms.widgets.RadioSelect()
    )
    # select
    hobby = forms.ChoiceField(
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
        label="爱好",
        initial=3,
        widget=forms.widgets.Select()
    )
    # 多选
    hobby1 = forms.MultipleChoiceField(
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
        label="爱好",
        initial=[1, 3],
        widget=forms.widgets.SelectMultiple()
    )
    # 单选checkbox
    keep = forms.ChoiceField(
        label="是否记住密码",
        initial="checked",
        widget=forms.widgets.CheckboxInput()
    )
    # 多选checkbox
    hobby2 = forms.MultipleChoiceField(
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
        label="爱好",
        initial=[1, 3],
        widget=forms.widgets.CheckboxSelectMultiple()
    )
```

[更详细的笔记请点击这里](https://www.cnblogs.com/Dominic-Ji/p/9240365.html)



## cookie与session

> 发展史
> 	1.网站都没有保存用户功能的需求 所有用户访问返回的结果都是一样的
> 		eg:新闻、博客、文章...
> 	
>
> 2.出现了一些需要保存用户信息的网站
> 	eg:淘宝、支付宝、京东...
> 	以登陆功能为例:如果不保存用户登陆状态 也就意味着用户每次访问网站都需要重复的输入用户名和密码(你觉得这样的网站你还想用吗？)
> 当用户第一次登陆成功之后 将用户的用户名密码返回给用户浏览器 让用户浏览器保存在本地，之后访问网站的时候浏览器自动将保存在浏览器上的用户名和密码发送给服务端，服务端获取之后自动验证
> 早起这种方式具有非常大的安全隐患
>
>
> ​		
>
> 优化:
> 		当用户登陆成功之后，服务端产生一个随机字符串(在服务端保存数据,用kv键值对的形式)，交由客户端浏览器保存
> 		随机字符串1:用户1相关信息
> 		随机字符串2:用户2相关信息
> 		随机字符串3:用户3相关信息
> 		之后访问服务端的时候，都带着该随机字符串，服务端去数据库中比对是否有对应的随机字符串从而获取到对应的用户信息
>
>
> ​	
>
> 但是如果你拿到了截获到了该随机字符串，那么你就可以冒充当前用户 其实还是有安全隐患的
>
> 你要知道在web领域没有绝对的安全也没有绝对的不安全
>
> cookie
> 	服务端保存在客户端浏览器上的信息都可以称之为cookie
>   它的表现形式一般都是k:v键值对(可以有多个)
> session
> 	数据是保存在服务端的并且它的表现形式一般也是k:v键值对(可以有多个)
>     
>
>
> token
> 	session虽然数据是保存在服务端的 但是禁不住数据量大
>   服务端不再保存数据
>   	登陆成功之后 将一段用户信息进行加密处理(加密算法之后你公司开发知道)
>     将加密之后的结果拼接在信息后面 整体返回给浏览器保存 
>     浏览器下次访问的时候带着该信息 服务端自动切去前面一段信息再次使用自己的加密算法
>     跟浏览器尾部的密文进行比对
> jwt认证
> 	三段信息
>   (后期会讲 结合django一起使用) 
> 	
>
> 总结:
>     1.cookie就是保存在客户端浏览器上的信息
>     2.session就是保存在服务端上的信息
>     3.session是基于cookie工作的(其实大部分的保存用户状态的操作都需要使用到cookie)



### Cookie操作

> 虽然cookie是服务端告诉客户端浏览器需要保存内容
>
> 但是客户端浏览器可以选择拒绝保存 如果禁止了 那么 只要是需要记录用户状态的网站登陆功能都无法使用了
>
> 视图函数的返回值
>
> `return HttpResponse()
> return render()
> return redirect()`
>
> `obj1 = HttpResponse()`
>
> `return obj1`
>
> 
>
> `obj2 = render()`
>
> `return obj2`
>
> 
>
> `obj3 = redirect()`
>
> `return obj3`
>
> 如果你想要操作cookie，你就不得不利用obj对象

- 设置cookie

  `obj.set_cookie(key,value)`

- 获取cookie

  `request.COOKIES.get(key)`

- 在设置cookie的时候可以添加一个超时时间

  `obj.set_cookie('username', 'jason666',max_age=3,expires=3)`

  ​	max_age
  ​	expires

  ​	两者都是设置超时时间的 并且都是以秒为单位
  ​	需要注意的是 针对IE浏览器需要使用expires
  主动删除cookie(注销功能)

#### 案例:登录功能

```python
def login_auth(func):
    def inner(request,*args,**kwargs):
        if request.COOKIES.get('username'):
            return func(request,*args,**kwargs)
        else:
            return redirect('/login/?next=%s'%request.get_full_path())
    return inner

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'root' and password == '123':
            target_url = request.GET.get('next')
            if target_url:
                obj = redirect(target_url)
            else:
                obj = redirect('/home/')
            obj.set_cookie('username','root')
            return obj
    return render(request,'login.html')

@login_auth
def home(request):
    return HttpResponse('i am home,only login user can enter this page')

@login_auth
def index(request):
    return  HttpResponse('i am index ,only login user can enter this page')

```

### session操作

> session数据是保存在服务端的(存？)，给客户端返回的是一个随机字符串
> 	sessionid:随机字符串
>
> .在默认情况下操作session的时候需要django默认的一张django_session表
> 	数据库迁移命令
> 		django会自己创建很多表	django_session就是其中的一张
>
> django默认session的过期时间是**14天**
> 	但是你也可以人为的修改它

- 设置session

  `request.session['key'] = value`

- 获取session

  `request.session.get('key')`

- 设置过期时间

  `request.session.set_expiry()`

  括号内可以放四种类型的参数

  - 1.整数						多少秒
  - 2.日期对象			   到指定日期就失效
  - 3.0								一旦当前浏览器窗口关闭立刻失效
  - 4.不写						失效时间就取决于django内部全局session默认的失效时间

- 清除session	

  - `request.session.delete()`     只删服务端的 客户端的不删
  - `request.session.flush()`    浏览器和服务端都清空(推荐使用)

> session是保存在服务端的 但是session的保存位置可以有多种选择
>
> 1. MySQL
> 2. 文件
> 3. redis
> 4. memcache
>
> jango_session表中的数据条数是取决于浏览器的
> 	同一个计算机上(IP地址)同一个浏览器只会有一条数据生效
> 	(当session过期的时候可能会出现多条数据对应一个浏览器，但是该现象不会持续很久，内部会自动识别过期的数据清除 你也可以通过代码清除)

### CBV如何添加装饰器

```python
from django.views import View
from django.utils.decorators import method_decorator
"""
CBV中django不建议你直接给类的方法加装饰器
无论该装饰器能都正常给你 都不建议直接加
"""

# 方式2(可以添加多个针对不同的方法加不同的装饰器)
@method_decorator(login_auth,name='get')  
@method_decorator(login_auth,name='post')
class MyLogin(View):
    @method_decorator(login_auth)  # 方式3:它会直接作用于当前类里面的所有的方法
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    @method_decorator(login_auth)  # 方式1:指名道姓
    def get(self,request):
        return HttpResponse("get请求")

    def post(self,request):
        return HttpResponse('post请求')
```



## django中间件

> django中间件是django的门户
> 1.请求来的时候需要先经过中间件才能到达真正的django后端
> 2.响应走的时候最后也需要经过中间件才能发送出去
>
> django自带七个中间件

```python
MIDDLEWARE = [
  	'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 如何自定义中间件

1. 在项目名或者应用名下创建一个任意名称的文件夹

2. 在该文件夹内创建一个任意名称的py文件

3. 在该py文件内需要书写类(这个类必须继承MiddlewareMixin)
   	然后在这个类里面就可以自定义五个方法了
   	(这五个方法并不是全部都需要书写，用几个写几个)

   - **`process_request `**
   - **`process_response`**
   - `process_view`
   - `process_template_response`
   - `process_exception`

4. 需要将类的路径以字符串的形式注册到配置文件中才能生效

   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
       '你自己写的中间件的路径1',
       '你自己写的中间件的路径2',
       '你自己写的中间件的路径3',
   ]
   ```

#### 自定义中间件代码

```python
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class MyMiddleware1(MiddlewareMixin):
    def process_request(self,request):
        print('我是第一个自定义中间件里面的process_request方法')
        # return HttpResponse('haha')

    def process_response(self,request,response):
        print('我是第一个自定义中间件里面的process_response方法')
        return response
    
    def process_view(self,request,view_name,*args,**kwargs):
        print(view_name,args,kwargs)
        print('我是第一个自定义中间件里面的process_view')

    def process_template_response(self,request,response):
        print('我是第一个自定义中间件里面的process_template_response')
        return response

    def process_exception(self,request,exception):
        print('我是第一个中间件里面的process_exception')
        print(exception)


class MyMiddleware2(MiddlewareMixin):
    def process_request(self,request):
        print('我是第二个自定义中间件里面的process_request方法')
        # return HttpResponse('hei hei ')

    def process_response(self,request,response):
        print('我是第二个自定义中间件里面的process_response方法')
        return response
    
    def process_view(self,request,view_name,*args,**kwargs):
        print(view_name,args,kwargs)
        print('我是第二个自定义中间件里面的process_view')

    def process_template_response(self,request,response):
        print('我是第二个自定义中间件里面的process_template_response')
        return response

    def process_exception(self,request,exception):
        print('我是第二个中间件里面的process_exception')
        print(exception)
```



### 中间件方法

- **process_request** 

  > 1. 请求来的时候需要经过每一个中间件里面的process_request方法结果的顺序是按照配置文件中注册的中间件从上往下的顺序依次执行
  > 2. 如果中间件里面没有定义该方法，那么直接跳过执行下一个中间件
  > 3. 如果该方法返回了HttpResponse对象，那么请求将不再继续往后执行而是直接原路返回(校验失败不允许访问...)
  > 4. process_request方法就是用来做全局相关的所有限制功能

- **process_response**

  > 1. 响应走的时候需要经过每一个中间件里面的process_response方法,该方法有两个额外的参数request,response
  > 2. 该方法必须返回一个HttpResponse对象
  >    1. 默认返回的就是形参**response**
  >    2. 你也可以自己返回自己的
  >    3. 顺序是按照配置文件中注册了的中间件从下往上依次经过如果你没有定义的话 直接跳过执行下一个
  >       		
  >
  > 如果在第一个process_request方法就已经返回了HttpResponse对象，那么响应走的时候会直接走同级别的process_reponse返回
  > 	
  >
  > flask框架也有一个中间件但是它的规律
  > 	只要返回数据了就必须经过所有中间件里面的类似于process_reponse方法

- process_view

  > 路由匹配成功之后执行视图函数之前，会自动执行中间件里面的该放法
  > 顺序是按照配置文件中注册的中间件从上往下的顺序依次执行

- process_template_response

  > 返回的HttpResponse对象有render属性的时候才会触发
  > 顺序是按照配置文件中注册了的中间件从下往上依次经过

- process_exception

  > 当视图函数中出现异常的情况下触发
  > 顺序是按照配置文件中注册了的中间件从下往上依次经过



### csrf跨站请求伪造

> csrf跨站请求伪造校验
> 		网站在给用户返回一个具有提交数据功能页面的时候会给这个页面加一个唯一标识
> 		当这个页面朝后端发送post请求的时候 我的后端会先校验唯一标识，如果唯一标识不对直接拒绝(403 forbbiden)如果成功则正常执行	

#### 如何符合校验:

##### form表单如何符合校验:

```html
<form action="" method="post">
    {% csrf_token %}
    <p>username:<input type="text" name="username"></p>
    <p>target_user:<input type="text" name="target_user"></p>
    <p>money:<input type="text" name="money"></p>
    <input type="submit">
</form>
```

##### ajax如何符合校验:

```html
<script>
    $('#d1').click(function () {
        $.ajax({
            url:'',
            type:'post',
            // 第一种 利用标签查找获取页面上的随机字符串
            {#data:{"username":'jason','csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()},#}
            // 第二种 利用模版语法提供的快捷书写
            {#data:{"username":'jason','csrfmiddlewaretoken':'{{ csrf_token }}'},#}
            // 第三种 通用方式直接拷贝js代码并应用到自己的html页面上即可
            data:{"username":'jason'},
            success:function () {

            }
        })
    })
```

##### 拷贝代码:

```js
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
```

> 通用方式直接拷贝js代码并应用到自己的html页面上即可



### csrf相关装饰器

> 两种需求：
>
> 1. 网站整体都不校验csrf，就单单几个视图函数需要校
> 2. 网站整体都校验csrf，就单单几个视图函数不校验

- `csrf_protect `需要校验

  针对csrf_protect符合我们之前所学的CBV装饰器的三种玩法

- `csrf_exempt`忽视校验

  针对csrf_exempt只能给CBV中的dispatch方法加才有效

##### 用法：

```python
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.utils.decorators import method_decorator

# @csrf_exempt
# @csrf_protect
def transfer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        target_user = request.POST.get('target_user')
        money = request.POST.get('money')
        print('%s给%s转了%s元'%(username,target_user,money))
    return render(request,'transfer.html')


# CBV
from django.views import View

# @method_decorator(csrf_protect,name='post')  # 针对csrf_protect 第二种方式可以
# @method_decorator(csrf_exempt,name='post')  # 针对csrf_exempt 第二种方式不可以
@method_decorator(csrf_exempt,name='dispatch')
class MyCsrfToken(View):
    # @method_decorator(csrf_protect)  # 针对csrf_protect 第三种方式可以
    # @method_decorator(csrf_exempt)  # 针对csrf_exempt 第三种方式可以
    def dispatch(self, request, *args, **kwargs):
        return super(MyCsrfToken, self).dispatch(request,*args,**kwargs)

    def get(self,request):
        return HttpResponse('get')

    # @method_decorator(csrf_protect)  # 针对csrf_protect 第一种方式可以
    # @method_decorator(csrf_exempt)  # 针对csrf_exempt 第一种方式不可以
    def post(self,request):
        return HttpResponse('post')
```



## Auth模块

> **Auth模块是Django自带的用户认证模块**
>
> 我们在开发一个网站的时候，无可避免的需要设计实现网站的用户系统。此时我们需要实现包括用户注册、用户登录、用户认证、注销、修改密码等功能，这还真是个麻烦的事情呢。
>
> Django作为一个完美主义者的终极框架，当然也会想到用户的这些痛点。它内置了强大的用户认证系统--auth，它默认使用 auth_user 表来存储用户数据。



###  auth模块常用方法

```python
from django.contrib import auth
```

#### authenticate()

> 提供了用户认证功能，即验证用户名以及密码是否正确，一般需要username 、password两个关键字参数。
>
> 如果认证成功（用户名和密码正确有效），便会返回一个 User 对象。
>
> authenticate()会在该 User 对象上设置一个属性来标识后端已经认证了该用户，且该信息在后续的登录过程中是需要的。

用法：

```python
user = authenticate(username='usernamer',password='password')
```



#### login(HttpRequest, user)

> 该函数接受一个HttpRequest对象，以及一个经过认证的User对象。
>
> 该函数实现一个用户登录的功能。它本质上会在后端为该用户生成相关session数据。

用法：

```python
from django.contrib.auth import authenticate, login
   
def my_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(request,username=username, password=password)
  if user is not None:
    login(request, user)
    # Redirect to a success page.
    ...
  else:
    # Return an 'invalid login' error message.
    ...
```



#### **logout(request)**

> 该函数接受一个HttpRequest对象，无返回值。
>
> 当调用该函数时，当前请求的session信息会全部清除。该用户即使没有登录，使用该函数也不会报错。

用法：

```python
from django.contrib.auth import logout
   
def logout_view(request):
  logout(request)
  # Redirect to a success page.
```



#### is_authenticated()

> 用来判断当前请求是否通过了认证。

用法：

```python
def my_view(request):
  if not request.user.is_authenticated():
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
```



#### **login_requierd()**

> auth 给我们提供的一个装饰器工具，用来快捷的给某个视图添加登录校验。

用法：

```pythono
from django.contrib.auth.decorators import login_required
      
@login_required
def my_view(request):
  ...
```



#### create_user()

> auth 提供的一个创建新用户的方法，需要提供必要参数（username、password）等。

用法：

```python
from django.contrib.auth.models import User
user = User.objects.create_user(username='用户名',password='密码',email='邮箱',...)
```



#### create_superuser()

> auth 提供的一个创建新的超级用户的方法，需要提供必要参数（username、password）等。

用法：

```python
from django.contrib.auth.models import User
user = User.objects.create_superuser(username='用户名',password='密码',email='邮箱',...)
```



#### check_password(password)

> auth 提供的一个检查密码是否正确的方法，需要提供当前请求用户的密码。
>
> 密码正确返回True，否则返回False。

用法：

```python
ok = user.check_password('密码')
```



#### set_password(password)

> auth 提供的一个修改密码的方法，接收 要设置的新密码 作为参数。
>
> 注意：设置完一定要调用用户对象的save方法！！！

用法：

```python
user.set_password('密码')
user.save()
```

修改密码小例子：

```
@login_required
def set_password(request):
    user = request.user
    err_msg = ''
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        # 检查旧密码是否正确
        if user.check_password(old_password):
            if not new_password:
                err_msg = '新密码不能为空'
            elif new_password != repeat_password:
                err_msg = '两次密码不一致'
            else:
                user.set_password(new_password)
                user.save()
                return redirect("/login/")
        else:
            err_msg = '原密码输入错误'
    content = {
        'err_msg': err_msg,
    }
    return render(request, 'set_password.html', content)
```



#### User对象的属性

User对象属性：username， password

is_staff ： 用户是否拥有网站的管理权限.

is_active ： 是否允许用户登录, 设置为 False，可以在不删除用户的前提下禁止用户登录。



### 如何扩展auth_user表

#### 第一种:一对一关系  不推荐

```python
from django.db import models
from django.contrib.auth.models import User,AbstractUser
# Create your models here.

class UserDetail(models.Model):
    phone = models.BigIntegerField()
	user = models.OneToOneField(to='User')

```

#### 第二种:面向对象的继承

>  如果继承了AbstractUser
>     那么在执行数据库迁移命令的时候auth_user表就不会再创建出来了
>     而UserInfo表中会出现auth_user所有的字段外加自己扩展的字段
>     这么做的好处在于你能够直接点击你自己的表更加快速的完成操作及扩展

```python
class UserInfo(AbstractUser):
    
    phone = models.BigIntegerField()
    
    
"""
你如果自己写表替代了auth_user那么
auth模块的功能还是照常使用，参考的表页由原来的auth_user变成了UserInfo


我们bbs作业用户表就是用的上述方式
"""
```

> 前提:
>         1.在继承之前没有**执行过数据库迁移命令**
>             auth_user**没有被创建**，如果当前库已经创建了那么你就重新换一个库
>         2.继承的类里面**不要覆盖AbstractUser里面的字段名**表里面有的字段都不要动，只扩展额外字段即可
>         3.需要在配置文件中告诉django你要用UserInfo替代auth_user()
>             **AUTH_USER_MODEL = 'app01.UserInfo.应用名.表名**



## admin后台管理

> django给你提供了一个可视化的界面用来让你方便的对你的模型表
> 进行数据的增删改查操作
>
> 如果你先想要使用amdin后台管理操作模型表
> 你需要先注册你的模型表告诉admin你需要操作哪些表

```python
去你的应用下的admin.py中注册你的模型表
from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.UpAndDown)
admin.site.register(models.Comment)
```





# Ajax

> 异步提交
> 局部刷新
> 例子:github注册
> 	动态获取用户名实时的跟后端确认并实时展示的前端(局部刷新)

**发送请求的方式:**

1. 浏览器地址栏直接输入url回车

   GET请求

2. a标签href属性	

   GET请求

3. form表单

    GET请求/POST请求

4. ajax

   GET请求/POST请求

> AJAX 不是新的编程语言，而是一种使用现有标准的新方法(比较装饰器)
>
> AJAX 最大的优点是在不重新加载整个页面的情况下，可以与服务器交换数据并更新部分网页内容。（这一特点给用户的感受是在不知不觉中完成请求和响应过程）
>
> 只学习**jQuery封装之后**的版本(不学原生的 原生的复杂并且在实际项目中也一般不用)



## 初识ajax

> 页面上有三个input框
> 	在前两个框中输入数字 点击按钮 朝后端发送ajax请求
> 	后端计算出结果 再返回给前端动态展示的到第三个input框中
> 	(整个过程页面不准有刷新,也不能在前端计算)

```js
$('#btn').click(function () {
        // 朝后端发送ajax请求
        $.ajax({
            // 1.指定朝哪个后端发送ajax请求
            url:'', // 不写就是朝当前地址提交
            // 2.请求方式
            type:'post',  // 不指定默认就是get 都是小写
            // 3.数据
            {#data:{'username':'jason','password':123},#}
            data:{'i1':$('#d1').val(),'i2':$('#d2').val()},
            // 4.回调函数:当后端给你返回结果的时候会自动触发 args接受后端的返回结果
            success:function (args) {
                {#alert(args)  // 通过DOM操作动态渲染到第三个input里面#}
                {#$('#d3').val(args)#}
                console.log(typeof args)

            }
        })
    })
              
```

> 针对后端如果是用HttpResponse返回的数据 回调函数不会自动帮你反序列化
> 如果后端直接用的是JsonResponse返回的数据 回调函数会自动帮你反序列化



## 前后端传输数据的编码格式(contentType)

> 主要研究post请求数据的编码格式
>
> get请求数据就是直接放在url后面的
> url?username=jason&password=123

#### **可以朝后端发送post请求的方式:**

> 1. form表单
> 2. ajax请求

#### **前后端传输数据的编码格式:**

> 1. urlencoded
> 2. formdata
> 3. json

#### **研究form表单：**

> **默认**的数据编码格式是**:urlencoded**
> 数据格式:username=jason&password=123
>
> django后端针对符合urlencoded编码格式的数据都会自动帮你解析封装到**request.POST**中
>
>  如果你把编码格式改成formdata，那么针对**普通的键值对**不是解析到**request.POST**中而将**文件**解析到**request.FILES**中
>
> form表单是没有办法发送json格式数据的

#### 研究ajax:

> **默认**的编码格式也是**urlencoded**
> 数据格式:username=jason&age=20
>
> django后端针对符合**urlencoded**编码格式的数据都会自动帮你解析封装到**request.POST**中



## ajax发送json格式数据

> 前后端传输数据的时候一定要确保编码格式跟数据真正的格式是一致的

```html
<script>
    $('#d1').click(function () {
        $.ajax({
            url:'',
            type:'post',
            data:JSON.stringify({'username':'jason','age':25}),
            contentType:'application/json',  // 指定编码格式
            success:function () {

            }
        })
    })
</script>
```

```python
json_bytes = request.body
json_str = json_bytes.decode('utf-8')
json_dict = json.loads(json_str)

# json.loads括号内如果传入了一个二进制格式的数据那么内部自动解码再反序列化
json_dict = json.loads(json_bytes)
```

> ajax发送json格式数据需要注意点
> 	1.contentType参数指定成:application/json
> 	2.数据是真正的json格式数据
> 	3.django后端不会帮你处理json格式数据需要你自己去request.body获取并处理



## ajax发送文件

ajax发送文件需要借助于js内置对象FormData

```html
<script>
    // 点击按钮朝后端发送普通键值对和文件数据
    $('#d4').on('click',function () {
        // 1 需要先利用FormData内置对象
        let formDateObj = new FormData();
        // 2 添加普通的键值对
        formDateObj.append('username',$('#d1').val());
        formDateObj.append('password',$('#d2').val());
        // 3 添加文件对象
        formDateObj.append('myfile',$('#d3')[0].files[0])
        // 4 将对象基于ajax发送给后端
        $.ajax({
            url:'',
            type:'post',
            data:formDateObj,  // 直接将对象放在data后面即可

            // ajax发送文件必须要指定的两个参数
            contentType:false,  // 不需使用任何编码 django后端能够自动识别formdata对象
            processData:false,  // 告诉你的浏览器不要对你的数据进行任何处理

            success:function (args) {
            }
        })


    })
</script>
```

```python
def ab_file(request):
    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
            print(request.FILES)
    return render(request,'ab_file.html')
```

> 总结:
>
> 1. 需要利用内置对象FormData
>
> 2. 添加普通的键值对
>
>    `formDateObj.append('username',$('#d1').val());`
>    `formDateObj.append('password',$('#d2').val());`
>
> 3. 添加文件对象
>
>     `formDateObj.append('myfile',$('#d3')[0].files[0])`
>
> **需要指定两个关键性的参数**:
>
> - `contentType:false`
>
>   不需使用任何编码 django后端能够自动识别formdata对象
>
> - `processData:false`
>
>   告诉你的浏览器不要对你的数据进行任何处理
>
>   
>
> django后端能够直接识别到**formdata对象**并且能够将内部的**普通键值**自动解析并封装到**request.POST**中 **文件数据**自动解析并封装到**request.FILES**中



## ajax结合sweetalert

```html
"""
自己要学会如何拷贝
学会基于别人的基础之上做修改
研究各个参数表示的意思 然后找葫芦画瓢
"""
<script>
    $('.del').on('click',function () {
        // 先将当前标签对象存储起来
        let currentBtn = $(this);
        // 二次确认弹框
        swal({
          title: "你确定要删吗?",
          text: "你可要考虑清除哦，可能需要拎包跑路哦!",
          type: "warning",
          showCancelButton: true,
          confirmButtonClass: "btn-danger",
          confirmButtonText: "是的，老子就要删!",
          cancelButtonText: "算了,算了!",
          closeOnConfirm: false,
          closeOnCancel: false,
          showLoaderOnConfirm: true
        },
        function(isConfirm) {
          if (isConfirm) {
                // 朝后端发送ajax请求删除数据之后 再弹下面的提示框
                $.ajax({
                    {#url:'/delete/user/' + currentBtn.attr('delete_id'),  // 1 传递主键值方式1#}
                    url:'/delete/user/',  // 2 放在请求体里面
                    type:'post',
                    data:{'delete_id':currentBtn.attr('delete_id')},
                    success:function (args) {  // args = {'code':'','msg':''}
                        // 判断响应状态码 然后做不同的处理
                        if(args.code === 1000){
                            swal("删了!", args.msg, "success");
                            // 1.lowb版本 直接刷新当前页面
                            {#window.location.reload()#}
                            // 2.利用DOM操作 动态刷新
                            currentBtn.parent().parent().remove()
                        }else{
                            swal('完了','出现了位置的错误','info')
                        }
                    }

                })

          } else {
            swal("怂逼", "不要说我认识你", "error");
          }
        });
    })

</script>
```

**解决字体中文动画覆盖问题：**

```html
div.sweet-alert h2 {
    padding-top: 10px;
}
```





> 知耻而后勇
> 		任重道远！
>
> ​				——*佳猪*

