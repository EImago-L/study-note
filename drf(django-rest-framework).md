#  drf(django-rest-framework)

## API接口

> 通过网络，规定了前后台信息交互规则的url链接，也就是前后台信息交互的媒介

- url：长得像返回数据的url链接

  - https://api.map.baidu.com/place/v2/search

  

- 请求方式

  - get、post、put、patch、delete

  

- 请求参数

  - json或xm格式的key-value类型数据

  - ak：6E823f587c95f0148c19993539b99295

  - region：上海

  - query：肯德基

  - output：json

    

- 响应结果

  - 上方请求参数的output参数值决定了响应数据的格式

  - 数据

    ```
    # xml格式
    https://api.map.baidu.com/place/v2/search?ak=6E823f587c95f0148c19993539b99295&region=%E4%B8%8A%E6%B5%B7&query=%E8%82%AF%E5%BE%B7%E5%9F%BA&output=xml
    #json格式
    https://api.map.baidu.com/place/v2/search?ak=6E823f587c95f0148c19993539b99295&region=%E4%B8%8A%E6%B5%B7&query=%E8%82%AF%E5%BE%B7%E5%9F%BA&output=json
    {
        "status":0,
      	"message":"ok",
        "results":[
            {
                "name":"肯德基(罗餐厅)",
                "location":{
                    "lat":31.415354,
                    "lng":121.357339
                },
                "address":"月罗路2380号",
                "province":"上海市",
                "city":"上海市",
                "area":"宝山区",
                "street_id":"339ed41ae1d6dc320a5cb37c",
                "telephone":"(021)56761006",
                "detail":1,
                "uid":"339ed41ae1d6dc320a5cb37c"
            }
          	...
    		]
    }
    ```

    

## restful规范

> REST全称是Representational State Transfer，中文意思是表述（编者注：通常译为表征性状态转移）。 它首次出现在2000年Roy Fielding的博士论文中。
>
> RESTful是一种定义Web API接口的设计风格，尤其适用于前后端分离的应用模式中。
>
> 这种风格的理念认为后端开发任务就是提供数据的，对外提供的是数据资源的访问接口，所以在定义接口时，客户端访问的URL路径就表示这种要操作的数据资源。
>
> 事实上，我们可以使用任何一个框架都可以实现符合restful规范的API接口。

1. #### 数据的安全保障

   - url链接一般都采用https协议进行传输

   

2. #### 接口特征表现

   - 用api关键字标识接口url

     - [https://api.baidu.com](https://api.baidu.com/)
     - https://www.baidu.com/api

     注：看到api字眼，就代表该请求url链接是完成前后台数据交互的

     

3. #### 多数据版本共存

   - 在url链接中标识数据版本

     - https://api.baidu.com/v1
     - https://api.baidu.com/v2

     注：url链接中的v1、v2就是不同数据版本的体现（只有在一种数据资源有多版本情况下）

     

4. #### 数据即是资源，均使用名词（可复数）

   - 接口一般都是完成前后台数据的交互，交互的数据我们称之为资源

     - https://api.baidu.com/users
     - https://api.baidu.com/books
     - https://api.baidu.com/book

     注：一般提倡用资源的复数形式，在url链接中不要出现操作资源的动词，错误示范：https://api.baidu.com/delete-user

   - 特殊的接口可以出现动词，因为这些接口一般没有一个明确的资源，或是动词就是接口的核心含义

     - https://api.baidu.com/place/search
     - https://api.baidu.com/login

     

5. #### 资源操作由请求方式决定（method）

   - 操作资源一般都会涉及到增删改查，我们提供请求方式来标识增删改查动作

     - https://api.baidu.com/books - get请求：获取所有书
     - https://api.baidu.com/books/1 - get请求：获取主键为1的书
     - https://api.baidu.com/books - post请求：新增一本书书
     - https://api.baidu.com/books/1 - put请求：整体修改主键为1的书
     - https://api.baidu.com/books/1 - patch请求：局部修改主键为1的书
     - https://api.baidu.com/books/1 - delete请求：删除主键为1的书

     

6. ####  过滤，通过在url上传参的形式传递搜索条件

   - https://api.example.com/v1/zoos?limit=10：指定返回记录的数量
   - https://api.example.com/v1/zoos?offset=10：指定返回记录的开始位置
   - https://api.example.com/v1/zoos?page=2&per_page=100：指定第几页，以及每页的记录数
   - https://api.example.com/v1/zoos?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序
   - https://api.example.com/v1/zoos?animal_type_id=1：指定筛选条件

   

7. ####  响应状态码

   7 .1正常响应

   - 响应状态码2xx
     - 200：常规请求
     - 201：创建成功

   7.2 重定向响应

   - 响应状态码3xx
     - 301：永久重定向
     - 302：暂时重定向

   7.3 客户端异常

   - 响应状态码4xx
     - 403：请求无权限
     - 404：请求路径不存在
     - 405：请求方法不存在

   7.4 服务器异常

   - 响应状态码5xx

     - 500：服务器异常

     

8. ####  错误处理，应返回错误信息，error当做key

   ```json
   {
       error: "无权限操作"
   }
   ```

9. #### 返回结果，针对不同操作，服务器向用户返回的结果应该符合以下规范

   > GET /collection：返回资源对象的列表（数组）
   > GET /collection/resource：返回单个资源对象
   > POST /collection：返回新生成的资源对象
   > PUT /collection/resource：返回完整的资源对象
   > PATCH /collection/resource：返回完整的资源对象
   > DELETE /collection/resource：返回一个空文档

   

10. #### 需要url请求的资源需要访问资源的请求链接

    ```json
    # Hypermedia API，RESTful API最好做到Hypermedia，即返回结果中提供链接，连向其他API方法，使得用户不查文档，也知道下一步应该做什么
    {
      	"status": 0,
      	"msg": "ok",
      	"results":[
            {
                "name":"肯德基(罗餐厅)",
                "img": "https://image.baidu.com/kfc/001.png"
            }
          	...
    		]
    }
    ```

    比较好的接口返回

    ```json
    # 响应数据要有状态码、状态信息以及数据本身
    {
      	"status": 0,
      	"msg": "ok",
      	"results":[
            {
                "name":"肯德基(罗餐厅)",
                "location":{
                    "lat":31.415354,
                    "lng":121.357339
                },
                "address":"月罗路2380号",
                "province":"上海市",
                "city":"上海市",
                "area":"宝山区",
                "street_id":"339ed41ae1d6dc320a5cb37c",
                "telephone":"(021)56761006",
                "detail":1,
                "uid":"339ed41ae1d6dc320a5cb37c"
            }
          	...
    		]
    }
    ```

    

## drf的简单使用

### 1.创建django项目

> `cd ~/Desktop`
> `django-admin startproject drfdemo`
>
> 或者直接在pycharm中创建项目
>
> 这个随便你

### 2.添加rest_framework应用

在**settings.py**的**INSTALLED_APPS**中添加’rest_framework’。

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    'rest_framework',
]
```

接下来就可以使用DRF提供的功能进行api接口开发了。在项目中如果使用rest_framework框架实现API接口，主要有以下三个步骤：

- 将请求的数据（如JSON格式）转换为模型类对象
- 操作数据库
- 将模型类对象转换为响应的数据（如JSON格式）

### 3.创建数据库和模型操作类

> 具体过程这里就不再赘述了

### 4.创建序列化器

在创建的应用目录中新建serializers.py用于保存该应用的序列化器。

创建一个StudentModelSerializer用于序列化与反序列化。

```python
# 创建序列化器类，回头会在试图中被调用
from rest_framework.serializers import ModelSerializer
from app01 import models
class BookdModelSerializer(ModelSerializer):
    class Meta:
        model = models.Books
        fields = "__all__"

```

- **model** 指明该序列化器处理的数据字段从模型类BookInfo参考生成
- **fields** 指明该序列化器包含模型类中的哪些字段，’**all**‘指明包含所有字段

### 5.编写视图

在创建的应用的views.py中创建视图StudentViewSet，这是一个视图集合。

```python
from rest_framework.viewsets import ModelViewSet
from .models import Books
from .serializers import BookdModelSerializer
# Create your views here.
class StudentViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookdModelSerializer
```

- **queryset** 指明该视图集在查询数据时使用的查询集
- **serializer_class** 指明该视图在进行序列化或反序列化时使用的序列化器

### 6.定义路由

在创建应用的urls.py中定义路由信息。

```python
from . import views
from rest_framework.routers import DefaultRouter

# 路由列表
urlpatterns = []

router = DefaultRouter()  # 可以处理视图的路由器
router.register('books\', views.BooksViewSet)  # 向路由器中注册视图集

urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
```

最后把子应用中的路由文件加载到总路由文件中.

```python
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("stu/",include("students.urls")),
]
```



## 序列化组件

> 序列化：将python对象转换成json格式字符串
>
> 反序列化：将json格式字符串转换为python对象

### 简单使用：

1. 在创建的应用下创建serializers.py文件(文件名随意)
2. 在类中写要序列化的字段，想序列化哪个字段就在类中写哪个字段
3. 在视图类中使用，导入serializers.py文件，实例化得到序列化类的对象，把要序列化的对象传入
4. 序列化类.data    是一个字典
5. 把字典返回，如果不适用rest_framework提供的Response，就得使用JsonResponse



#### serializers.py

```python
from rest_framework import serializers

# 想序列化哪个字段就在类中写哪个字段
class BookSerializer(serializers.Serializers):
    id = serializers.CharField()
    name = serializers.CharField()
    price = serializers.CharField()
    author = serializers.CharField()
```

#### views.py

```python
from rest_framework.views import APIView
from app01.Models import Book
from app01.serializers import BookSerializer
from rest_framework.response import Response

class BookView(APIView):
    def get(self,request,pk):
        book = Book.objects.filter(pk=pk).first()
        # 用一个类，毫无疑问要实例化
        # 要序列化谁，就把谁传过来
        book_ser = BookSerializer(book)
        return Response(book_ser.data)
```

#### urls.py

```python
re_path('books/(?P<pk>\d+)', views.BookView.as_view()),
```



### 序列化类的字段类型

|          字段           | 字段构造方式                                                 |
| :---------------------: | :----------------------------------------------------------- |
|    **BooleanField**     | BooleanField()                                               |
|  **NullBooleanField**   | NullBooleanField()                                           |
|      **CharField**      | CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True) |
|     **EmailField**      | EmailField(max_length=None, min_length=None, allow_blank=False) |
|     **RegexField**      | RegexField(regex, max_length=None, min_length=None, allow_blank=False) |
|      **SlugField**      | SlugField(max*length=50, min_length=None, allow_blank=False) 正则字段，验证正则模式 [a-zA-Z0-9*-]+ |
|      **URLField**       | URLField(max_length=200, min_length=None, allow_blank=False) |
|      **UUIDField**      | UUIDField(format=’hex_verbose’) format: 1) `'hex_verbose'` 如`"5ce0e9a5-5ffa-654b-cee0-1238041fb31a"` 2） `'hex'` 如 `"5ce0e9a55ffa654bcee01238041fb31a"` 3）`'int'` - 如: `"123456789012312313134124512351145145114"` 4）`'urn'` 如: `"urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"` |
|   **IPAddressField**    | IPAddressField(protocol=’both’, unpack_ipv4=False, **options) |
|    **IntegerField**     | IntegerField(max_value=None, min_value=None)                 |
|     **FloatField**      | FloatField(max_value=None, min_value=None)                   |
|    **DecimalField**     | DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None) max_digits: 最多位数 decimal_palces: 小数点位置 |
|    **DateTimeField**    | DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None) |
|      **DateField**      | DateField(format=api_settings.DATE_FORMAT, input_formats=None) |
|      **TimeField**      | TimeField(format=api_settings.TIME_FORMAT, input_formats=None) |
|    **DurationField**    | DurationField()                                              |
|     **ChoiceField**     | ChoiceField(choices) choices与Django的用法相同               |
| **MultipleChoiceField** | MultipleChoiceField(choices)                                 |
|      **FileField**      | FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL) |
|     **ImageField**      | ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL) |
|      **ListField**      | ListField(child=, min_length=None, max_length=None)          |



### 序列化字段的选项参数

| 参数名称            | 作用             |
| :------------------ | ---------------- |
| **max_length**      | 最大长度         |
| **min_lenght**      | 最小长度         |
| **allow_blank**     | 是否允许为空     |
| **trim_whitespace** | 是否截断空白字符 |
| **max_value**       | 最小值           |

**通用参数：**

| 参数名称           | 说明                                     |
| ------------------ | ---------------------------------------- |
| **read_only**      | 表明该字段仅用于序列化输出，默认False    |
| **write_only**     | 表明该字段仅用于反序列化输入，默认False  |
| **required**       | 表明该字段在反序列化时必须输入，默认True |
| **default**        | 反序列化时使用的默认值                   |
| **allow_null**     | 表明该字段是否允许传入None，默认False    |
| **validators**     | 该字段使用的验证器                       |
| **error_messages** | 包含错误编号与错误信息的字典             |
| **label**          | 用于HTML展示API页面时，显示的字段名称    |



### 钩子函数

> 在特定的节点自动触发完成响应操作
>
> 功能跟django中的form组件类似

#### 局部钩子

> validate_字段名

```python
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class BookSerializer(serializers.Serializer):
    # id=serializers.CharField()
    name=serializers.CharField(max_length=16,min_length=4)
    # price=serializers.DecimalField()
    price=serializers.CharField()
    author=serializers.CharField(validators=[check_author])  # validators=[] 列表中写函数内存地址
	
    def validate_price(self,data):
        #如果价格小于10，就校验不通过
        if float(data) > 10:
            return data
        else:
            #校验失败，抛异常
            raise ValidationError("价格太低")
```

#### 全局钩子

> validate(self,validate_data)
>
> validated_data是校验后的数据

```python
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class BookSerializer(serializers.Serializer):
    # id=serializers.CharField()
    name=serializers.CharField(max_length=16,min_length=4)
    # price=serializers.DecimalField()
    price=serializers.CharField()
    author=serializers.CharField(validators=[check_author])  # validators=[] 列表中写函数内存地址
    
    def validate(self,validate_data):
        author = validate_data.get('author')
        publish=validate_data.get('publish')
        if author == publish:
            raise ValidationError('作者名字跟出版社一样')
        else:
            return validate_data
```



### 具体案例

#### serializers.py（序列化器）

```python
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app01 import models

class BookSerializer(serializers.Serializer):
    # 需要序列化的字段 具体参数的使用上文中有提到
    # id = serializers.CharField()
    title = serializers.CharField(min_length=2)
    price = serializers.CharField()
    author = serializers.CharField()
    publish = serializers.CharField()
	
    # 重写update方法
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.author = validated_data.get('author')
        instance.price = validated_data.get('price')
        instance.publish = validated_data.get('publish')
        instance.save()
        return instance
	
    # 重写create方法
    def create(self,validated_data):
        instance = models.Books.objects.create(**validated_data)
        return instance
	
    # 局部钩子
    def validate_price(self, data):
        if float(data) > 10:
            return data
        else:
            raise ValidationError("价格太低")
	
    # 全局钩子
    def validate(self, validated_data):
        author = validated_data.get("author")
        publish = validated_data.get("publish")
        if author == publish:
            raise ValidationError("作者名字跟出版社一样")
        else:
            return validated_data

```

#### views.py（视图函数）

```python
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from app01 import models
from app01.serializers import BookSerializer
from rest_framework.response import Response
# Create your views here.

class BookView(APIView):
    # get方法只获取一条数据
    def get(self,request,pk):
        book_obj = models.Books.objects.filter(pk=pk).first()
        book_ser = BookSerializer(book_obj)
        return Response(book_ser.data)
	
    # put方法修改单条数据 需要在序列化器中重写update方法
    def put(self,request,pk):
        response_dict = {
            "status":100,
            "msg":"成功",
        }
        book_obj = models.Books.objects.filter(pk=pk).first()
        print(book_obj.title)
        book_ser = BookSerializer(instance=book_obj,data=request.data)

        if book_ser.is_valid():
            book_ser.save()
            response_dict["data"] = book_ser.data
        else:
            response_dict["status"] = 101
            response_dict["msg"] = "数据校验失败"
            response_dict["data"] = book_ser.errors
        return Response(response_dict)
    
    def delete(self,request,pk):
        response_dict = {
            "status":100,
            "msg":"成功",
        }
        ret=Book.objects.filter(pk=pk).delete()
        return Response(response_dict)


class BooksView(APIView):
    # get方法获取所有数据
    def get(self,request):
        response_msg = {
            'status':100,
            'msg':'成功'
        }
        book_obj = models.Books.objects.all()
        book_ser = BookSerializer(book_obj,many=True) # 序列化多条需要加上many=True
        response_msg['data'] = book_ser.data

        return Response(response_msg)
	
    # post提交新的数据 需要重写需要在序列化器中重写create方法
    def post(self,request):
        response_msg = {
            'status':100,
            'msg':'成功'
        }
        book_ser = BookSerializer(data=request.data)
        if book_ser.is_valid():
            book_ser.save()
            response_msg['data'] = book_ser.data
        else:
            response_msg['status'] = 102
            response_msg['msg'] = '数据校验失败'
            response_msg['data'] = book_ser.errors

        return Response(response_msg)

```

#### urls.py

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('books/(?P<pk>\d+)',views.BookView.as_view()),
    path('books/',views.BooksView.as_view())
]
```



### 模型类序列化器

#### serializers.py

```python
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app01 import models

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Books # 对应models.py中的模型
        fields = '__all__'
        # fields = ('price','author') # 只序列化指定字段
        # exclude = ('id','price') # 除了元组或列表中的字段不返回，其他的都返回（不能跟fields一起用）
        # read_only_fields = ('id',) # 只读字段，该字段只序列化输出
        # write_only_fields = ('title',) # 只写字段,该字段只反序列化输入

        # 在django3.0以上的版本中更推荐一下方式
        extra_kwargs = {
            'price':{'write_only':True},
            'id':{'read_only':True}
        }
```

#### views.py

```python
from rest_framework.views import APIView
from app01.serializers import BookSerializer,BookModelSerializer
from rest_framework.response import Response
from app01.utils import MyResponse

class BookView2(APIView):
    def get(self,request):
        response = MyResponse()
        book_obj = models.Books.objects.all()
        book_ser = BookModelSerializer(book_obj,many=True)
        response.data = book_ser.data
        return Response(response.get_dict)
```



### Serializer高级用法

#### source的使用

1. 可以改字段名字

   ```python
   class BookSerializer(serializers.Serializer):
       titlexxx = serializers.CharField(source='title') # 前面字段名可以更改，source的值要是表模型中的字段
   ```

2. 可以.跨表

   ```python
   class BookSerializer(serializers.Serializer)
       publish = serializers.CharField(source='publish.email') # email就是book表中外键关联的publish的字段
   ```

3. 可以执行方法

   ```python
   pub_date=serializers.CharField(source='test') #test是Book表模型中的方法
   ```

#### SerializerMethodField()的使用

> 它需要一个配套方法，get_字段名，返回值就是要显示的东西

```python
class BookSerializer(serializers.Serializer):
    authors = serializers.SerializerMethodField()
    def get_authors(self,instance): 
        '''
        instance参数就是在视图函数实例化BookSerializer类时传入的modles中的orm对象
        book_obj = models.Books.objects.all()
        book_ser = BookSerializer(book_obj,many=True)
        '''
        authors = instance.authors.all()
        ret_list = []
        for author in authors:
            ret_list.append(
                {"name":author.name,"age":author.age}
            )
        return ret_list
```



## 请求和响应

### Request

> REST framework 传入视图的request对象不再是Django默认的HttpRequest对象，而是REST framework提供的扩展了HttpRequest类的**Request**类的对象。
>
> REST framework 提供了**Parser**解析器，在接收到请求后会自动根据Content-Type指明的请求数据类型（如JSON、表单等）将请求数据进行parse解析，解析为类字典[QueryDict]对象保存到**Request**对象中。
>
> **Request对象的数据是自动根据前端发送数据的格式进行解析之后的结果。**
>
> 无论前端发送的哪种格式的数据，我们都可以以统一的方式读取数据。

#### 常用属性

1. data

   > `request.data`返回解析后的请求体数据。类似于django中标准的`request.POST`和`request.FILES`属性，但提供一下特性
   >
   > - 包含了解析后的文件和非文件数据
   > - 包含了post、put、patch请求方式解析后的数据
   > - 利用了REST framework和parsers解析器，不仅支持表单类型。也支持JSON数据

2. query_params

   > `request.query_params`与Django标准的`request.GET`相同，只是更换了正确的名称而已

```python
# 请求对象
# from rest_framework.request import Request
    def __init__(self, request, parsers=None, authenticators=None,
                 negotiator=None, parser_context=None):
        # 二次封装request，将原生request作为drf request对象的 _request 属性
        self._request = request
    def __getattr__（self，item）：
    	return getattr(self._request,item)
```



### Response

```python
rest_framework.response.Response
```

>REST framework提供了一个响应类`Response`，使用该类构造响应对象时，响应的具体数据内容会被转换（render渲染）成符合前端需求的类型。
>
>REST framework提供了`Renderer` 渲染器，用来根据请求头中的`Accept`（接收数据类型声明）来自动转换响应数据到对应格式。如果前端请求中未进行Accept声明，则会采用默认方式处理响应数据，我们可以通过配置来修改默认响应格式。
>
>可以在**rest_framework.settings**查找所有的drf默认配置项
>
>```python
>REST_FRAMEWORK = {
>    'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
>        'rest_framework.renderers.JSONRenderer',  # json渲染器
>        'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览API渲染器
>    )
>}
>```

#### 构造方式

```python
 def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
```

> `data`数据不要是render处理之后的数据，只需传递python的内建类型数据即可，REST framework会使用`renderer`渲染器处理`data`。
>
> `data`不能是复杂结构的数据，如Django的模型类对象，对于这样的数据我们可以使用`Serializer`序列化器序列化处理后（转为了Python字典类型）再传递给`data`参数。

##### 参数说明

- `data`:为响应准备序列化后的数据
- `status`:状态码：默认200
- `template_name`：模板名称，如果使用HTMLRenderer时需指明
- `headers`：用存放响应头信息的字典
- `content_type`：响应数据的Content-type，通常此参数无需传递，REST framework会根据前端所需类型数据来设置改参数



#### 常用属性

1. data

   传给response对象的序列化后，但尚未render处理的数据

2. status_code

   状态码的数字

3. content

   经过render处理后的响应数据



#### 状态码

为了方便设置状态码，REST framewrok在`rest_framework.status`模块中提供了常用状态码常量。

1. 信息告知 - 1xx

   ```python
   HTTP_100_CONTINUE
   HTTP_101_SWITCHING_PROTOCOLS
   ```

2. 成功 - 2xx

   ```python
   HTTP_200_OK
   HTTP_201_CREATED
   HTTP_202_ACCEPTED
   HTTP_203_NON_AUTHORITATIVE_INFORMATION
   HTTP_204_NO_CONTENT
   HTTP_205_RESET_CONTENT
   HTTP_206_PARTIAL_CONTENT
   HTTP_207_MULTI_STATUS
   ```

3. 重定向 - 3xx

   ```python
   HTTP_300_MULTIPLE_CHOICES
   HTTP_301_MOVED_PERMANENTLY
   HTTP_302_FOUND
   HTTP_303_SEE_OTHER
   HTTP_304_NOT_MODIFIED
   HTTP_305_USE_PROXY
   HTTP_306_RESERVED
   HTTP_307_TEMPORARY_REDIRECT
   ```

4. 客户端错误 - 4xx

   ```python
   HTTP_400_BAD_REQUEST
   HTTP_401_UNAUTHORIZED
   HTTP_402_PAYMENT_REQUIRED
   HTTP_403_FORBIDDEN
   HTTP_404_NOT_FOUND
   HTTP_405_METHOD_NOT_ALLOWED
   HTTP_406_NOT_ACCEPTABLE
   HTTP_407_PROXY_AUTHENTICATION_REQUIRED
   HTTP_408_REQUEST_TIMEOUT
   HTTP_409_CONFLICT
   HTTP_410_GONE
   HTTP_411_LENGTH_REQUIRED
   HTTP_412_PRECONDITION_FAILED
   HTTP_413_REQUEST_ENTITY_TOO_LARGE
   HTTP_414_REQUEST_URI_TOO_LONG
   HTTP_415_UNSUPPORTED_MEDIA_TYPE
   HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
   HTTP_417_EXPECTATION_FAILED
   HTTP_422_UNPROCESSABLE_ENTITY
   HTTP_423_LOCKED
   HTTP_424_FAILED_DEPENDENCY
   HTTP_428_PRECONDITION_REQUIRED
   HTTP_429_TOO_MANY_REQUESTS
   HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
   HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
   ```

5. 服务器错误 - 5xx

   ```python
   HTTP_500_INTERNAL_SERVER_ERROR
   HTTP_501_NOT_IMPLEMENTED
   HTTP_502_BAD_GATEWAY
   HTTP_503_SERVICE_UNAVAILABLE
   HTTP_504_GATEWAY_TIMEOUT
   HTTP_505_HTTP_VERSION_NOT_SUPPORTED
   HTTP_507_INSUFFICIENT_STORAGE
   HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
   ```

   

## 视图

### APIView

```
rest_framework.views.APIView
```

`APIView`是REST framework提供的所有视图的基类，继承自Django的`View`父类。

**`APIView`与`View`的不同之处在于：**

- 传入到视图方法中的是REST framework的`Request`对象，而不是Django的`HttpRequeset`对象；
- 视图方法可以返回REST framework的`Response`对象，视图会为响应数据设置（render）符合前端要求的格式；
- 任何`APIException`异常都会被捕获到，并且处理成合适的响应信息；
- 在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制。

**支持定义的类属性**

- **authentication_classes** 列表或元祖，身份认证类
- **permissoin_classes** 列表或元祖，权限检查类
- **throttle_classes** 列表或元祖，流量控制类



在`APIView`中仍以常规的类视图定义方法来实现get() 、post() 或者其他请求方式的方法。

```python
from rest_framework.views import APIView
from rest_framework.response import Response

# url(r'^students/$', views.StudentsAPIView.as_view()),
class StudentsAPIView(APIView):
  	
    def get(self, request):
        data_list = Student.objects.all()
        serializer = StudentModelSerializer(instance=data_list, many=True)
        return Response(serializer.data)
```



### GenericAPIView[通用视图类]

```
rest_framework.generics.GenericAPIView
```

提供的关于序列化器使用的属性与方法

- 属性：

  - **serializer_class** 指明视图使用的序列化器

- 方法：

  - **get_serializer_class(self)**

    当出现一个视图类中调用多个序列化器时,那么可以通过条件判断在get_serializer_class方法中通过返回不同的序列化器类名就可以让视图方法执行不同的序列化器对象了。

    返回序列化器类，默认返回`serializer_class`，可以重写，例如：

    ```python
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullAccountSerializer
        return BasicAccountSerializer
    ```

  - ##### get_serializer(self, *args, **kwargs)

    返回序列化器对象，主要用来提供给Mixin扩展类使用，如果我们在视图中想要获取序列化器对象，也可以直接调用此方法。

    **注意，该方法在提供序列化器对象的时候，会向序列化器对象的context属性补充三个数据：request、format、view，这三个数据对象可以在定义序列化器时使用。**

    - **request** 当前视图的请求对象
    - **view** 当前请求的类视图对象
    - format 当前请求期望返回的数据格式

提供的关于数据库查询的属性与方法

- 属性：

  - **queryset** 指明使用的数据查询集

- 方法：

  - **get_queryset(self)**

    返回视图使用的查询集，主要用来提供给Mixin扩展类使用，是列表视图与详情视图获取数据的基础，默认返回`queryset`属性，可以重写，例如：

    ```python
    def get_queryset(self):
        user = self.request.user
        return user.accounts.all()
    ```

  - **get_object(self)**

    返回详情视图所需的模型类数据对象，主要用来提供给Mixin扩展类使用。

    在试图中可以调用该方法获取详情信息的模型类对象。

    **若详情访问的模型类对象不存在，会返回404。**

    该方法会默认使用APIView提供的check_object_permissions方法检查当前对象是否有权限被访问。

    举例：

    ```python
    # url(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view()),
    class BookDetailView(GenericAPIView):
        queryset = BookInfo.objects.all()
        serializer_class = BookInfoSerializer
    
        def get(self, request, pk):
            book = self.get_object() # get_object()方法根据pk参数查找queryset中的数据对象
            serializer = self.get_serializer(book)
            return Response(serializer.data)
    ```

其他可以设置的属性

- **pagination_class** 指明分页控制类
- **filter_backends** 指明过滤控制后端

为了方便学习上面的GenericAPIView通用视图类，我们新建一个子应用。

```
python manage.py startapp gen
```

代码：

```python
from rest_framework.generics import GenericAPIView

from students.models import Student
from .serializers import StudentModelSerializer, StudentModel2Serializer
from rest_framework.response import Response

class StudentsGenericAPIView(GenericAPIView):
    # 本次视图类中要操作的数据[必填]
    queryset = Student.objects.all()
    # 本次视图类中要调用的默认序列化器[选填]
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有学生信息"""
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)

        return Response(serializer.data)

    def post(self,request):

        data = request.data

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        serializer = self.get_serializer(instance=instance)

        return Response(serializer.data)


class StudentGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()

    serializer_class = StudentModelSerializer

    def get_serializer_class(self):
        """重写获取序列化器类的方法"""
        if self.request.method == "GET":
            return StudentModel2Serializer
        else:
            return StudentModelSerializer

    # 在使用GenericAPIView视图获取或操作单个数据时,视图方法中的代表主键的参数最好是pk
    def get(self,request,pk):
        """获取一条数据"""
        serializer = self.get_serializer(instance=self.get_object())

        return Response(serializer.data)

    def put(self,request,pk):

        data = request.data

        serializer = self.get_serializer(instance=self.get_object(),data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        serializer = self.get_serializer(instance=self.get_object())

        return Response(serializer.data)
```

序列化器类：

```python
from rest_framework import serializers

from students.models import Student

class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields = "__all__"


class StudentModel2Serializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields = ("name","class_null")
```



### 5个视图拓展类

>作用：
>
>提供了几种后端视图（对数据资源进行曾删改查）处理流程的实现，如果需要编写的视图属于这五种，则视图可以通过继承相应的扩展类来复用代码，减少自己编写的代码量。
>
>这五个扩展类需要搭配GenericAPIView父类，因为五个扩展类的实现需要调用GenericAPIView提供的序列化器与数据库查询的方法。

#### ListModelMixin

> 列表视图扩展类，提供`list(request, *args, **kwargs)`方法快速实现列表视图，返回200状态码。
>
> 该Mixin的list方法会对数据进行过滤和分页。

##### 源代码:

```python
class ListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        # 过滤
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

##### 举例：

```python
from rest_framework.mixins import ListModelMixin

class BookListView(ListModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request):
        return self.list(request)
```



#### CreateModelMixin

> 创建视图扩展类，提供`create(request, *args, **kwargs)`方法快速实现创建资源的视图，成功返回201状态码。
>
> 如果序列化器对前端发送的数据验证失败，返回400错误。

##### 源代码:

```python
class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        # 获取序列化器
        serializer = self.get_serializer(data=request.data)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 保存
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```



#### RetrieveModelMixin

> 详情视图扩展类，提供`retrieve(request, *args, **kwargs)`方法，可以快速实现返回一个存在的数据对象。
>
> 如果存在，返回200， 否则返回404。

##### 源代码:

```python
class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        # 获取对象，会检查对象的权限
        instance = self.get_object()
        # 序列化
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

##### 举例：

```python
class BookDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request, pk):
        return self.retrieve(request)
```



#### UpdateModelMixin

>更新视图扩展类，提供`update(request, *args, **kwargs)`方法，可以快速实现更新一个存在的数据对象。
>
>同时也提供`partial_update(request, *args, **kwargs)`方法，可以实现局部更新。
>
>成功返回200，序列化器校验数据失败时，返回400错误。

##### 源代码：

```python
class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
```



#### DestroyModelMixin

>删除视图扩展类，提供`destroy(request, *args, **kwargs)`方法，可以快速实现删除一个存在的数据对象。
>
>成功返回204，不存在返回404。

##### 源代码：

```python
class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
```



#### 使用GenericAPIView和视图扩展类，实现api接口，代码：

```python
from rest_framework.mixins import ListModelMixin,CreateModelMixin
class Students2GenericAPIView(GenericAPIView,ListModelMixin,CreateModelMixin):
    # 本次视图类中要操作的数据[必填]
    queryset = Student.objects.all()
    # 本次视图类中要调用的默认序列化器[选填]
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取多个学生信息"""
        return self.list(request)

    def post(self,request):
        """添加学生信息"""
        return self.create(request)


from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
class Student2GenericAPIView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()

    serializer_class = StudentModelSerializer

    # 在使用GenericAPIView视图获取或操作单个数据时,视图方法中的代表主键的参数最好是pk
    def get(self,request,pk):
        """获取一条数据"""
        return self.retrieve(request,pk)

    def put(self,request,pk):
        """更新一条数据"""
        return self.update(request,pk)

    def delete(self,request,pk):
        """删除一条数据"""
        return self.destroy(request,pk)
```



###  GenericAPIView的视图子类

#### CreateAPIView

提供 post 方法

继承自： GenericAPIView、CreateModelMixin

#### ListAPIView

提供 get 方法

继承自：GenericAPIView、ListModelMixin

#### RetrieveAPIView

提供 get 方法

继承自: GenericAPIView、RetrieveModelMixin

#### DestoryAPIView

提供 delete 方法

继承自：GenericAPIView、DestoryModelMixin

#### UpdateAPIView

提供 put 和 patch 方法

继承自：GenericAPIView、UpdateModelMixin

#### RetrieveUpdateAPIView

提供 get、put、patch方法

继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin

#### RetrieveUpdateDestoryAPIView

提供 get、put、patch、delete方法

继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin



###  视图集ViewSet

> 使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：
>
> - list() 提供一组数据
> - retrieve() 提供单个数据
> - create() 创建数据
> - update() 保存数据
> - destory() 删除数据

ViewSet视图集类不再实现get()、post()等方法，而是实现动作 **action** 如 list() 、create() 等。

视图集只在使用as_view()方法的时候，才会将**action**动作与具体请求方式对应上。如：

```python
class BookInfoViewSet(viewsets.ViewSet):

    def list(self, request):
        books = BookInfo.objects.all()
        serializer = BookInfoSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            books = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookInfoSerializer(books)
        return Response(serializer.data)
```

在设置路由时，我们可以如下操作

```python
urlpatterns = [
    url(r'^books/$', BookInfoViewSet.as_view({'get':'list'}),
    url(r'^books/(?P<pk>\d+)/$', BookInfoViewSet.as_view({'get': 'retrieve'})
]
```



### 使用ModelViewSet编写5个接口

```python
# views.py
from rest_framework.viewsets import ModelViewSet
class Book5View(ModelViewSet):  #5个接口都有，但是路由有点问题
    queryset = Book.objects
    serializer_class = BookSerializer
    
# urls.py
# 使用ModelViewSet编写5个接口
    path('books5/', views.Book5View.as_view(actions={'get':'list','post':'create'})), #当路径匹配，又是get请求，会执行Book5View的list方法
    re_path('books5/(?P<pk>\d+)', views.Book5View.as_view(actions={'get':'retrieve','put':'update','delete':'destroy'})),

```



### 继承ViewSetMixin的视图类

```python
# views.py
from rest_framework.viewsets import ViewSetMixin
class Book6View(ViewSetMixin,APIView): #一定要放在APIVIew前
    def get_all_book(self,request):
        print("xxxx")
        book_list = Book.objects.all()
        book_ser = BookSerializer(book_list, many=True)
        return Response(book_ser.data)
    
# urls.py
    #继承ViewSetMixin的视图类，路由可以改写成这样
    path('books6/', views.Book6View.as_view(actions={'get': 'get_all_book'})),

```



关于更多的视图操作请访问：[请点击这](http://www.liuqingzheng.top/python/Django-rest-framework%E6%A1%86%E6%9E%B6/4-drf-%E8%A7%86%E5%9B%BE%E7%BB%84%E4%BB%B6/)





## 路由

对于视图集ViewSet，我们除了可以自己手动指明请求方式与动作action之间的对应关系外，还可以使用Routers来帮助我们快速实现路由信息。

REST framework提供了两个router

- **SimpleRouter**
- **DefaultRouter**



### 使用方法

1. 创建router对象，并注册视图集

   ```python
   from rest_framework import routers
   
   router = routers.SimpleRouter()
   router.register(r'router_stu', StudentModelViewSet, base_name='student')
   ```

   register(prefix, viewset, base_name)

   - prefix 该视图集的路由前缀
   - viewset 视图集
   - base_name 路由别名的前缀

   如上述代码会形成的路由如下：

   ```python
   ^books/$    name: book-list
   ^books/{pk}/$   name: book-detail
   ```

2. 添加路由数据

   可以有两种方式：

   ```python
   urlpatterns = [
       ...
   ]
   urlpatterns += router.urls
   ```

   或

   ```python
   urlpatterns = [
       ...
       url(r'^', include(router.urls))
   ]
   ```

### 代码演示

使用路由类给视图集生成了路由地址

```python
# 必须是继承ModelViewSet的视图类才能自动生成路由
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
		# 这种方法不会自动生成，需要用action配置
    def login(self,request):
        """学生登录功能"""
        print(self.action)
        return Response({"message":"登录成功"})
```

路由代码：

```python
from django.urls import path, re_path
from . import views
urlpatterns = [
    ...
]

"""使用drf提供路由类router给视图集生成路由列表"""
# 实例化路由类
# drf提供一共提供了两个路由类给我们使用,他们用法一致,功能几乎一样
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# 注册视图集
# router.register("路由前缀",视图集类)
router.register("router_stu",views.StudentModelViewSet)

# 把生成的路由列表追加到urlpatterns
print( router.urls )
urlpatterns += router.urls
```

上面的代码就成功生成了路由地址[增/删/改/查一条/查多条的功能]，但是不会自动我们在视图集自定义方法的路由。

所以我们如果也要给自定义方法生成路由，则需要进行action动作的声明。



### 视图集中附加action的声明

在视图集中，如果想要让Router自动帮助我们为自定义的动作生成路由信息，需要使用`rest_framework.decorators.action`装饰器。

以action装饰器装饰的方法名会作为action动作名，与list、retrieve等同。

action装饰器可以接收两个参数：

- **methods**: 声明该action对应的请求方式，列表传递

- detail

  : 声明该action的路径是否与单一资源对应，及是否是

  ```
  xxx/<pk>/action方法名/
  ```

  - True 表示路径格式是`xxx/<pk>/action方法名/`
  - False 表示路径格式是`xxx/action方法名/`

举例：

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # methods 设置当前方法允许哪些http请求访问当前视图方法
    # detail 设置当前视图方法是否是操作一个数据
    # detail为True，表示路径名格式应该为 router_stu/{pk}/login/
    @action(methods=['get'], detail=False)
    def login(self, request):
        return Response({'msg':'登陆成功'})

    @action(methods=['put'], detail=True)
    def get_new_5(self, request,pk):
        return Response({'msg':'获取5条数据成功'})
```

由路由器自动为此视图集自定义action方法形成的路由会是如下内容：

```python
^router_stu/get_new_5/$    name: router_stu-get_new_5
^router_stu/{pk}/login/$   name: router_stu-login
```



## 认证

### 编写models

```python
# models.py
class User(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    user_type=models.IntegerField(choices=((1,'超级用户'),(2,'普通用户'),(3,'二笔用户')))

class UserToken(models.Model):
    user=models.OneToOneField(to='User')
    token=models.CharField(max_length=64)
```



### 新建认证类

```python
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app03 import models

class LoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if token:
            usr_token = models.Token.objects.filter(token=token).first()
            if usr_token:
                return usr_token.user,token
            else:
                raise AuthenticationFailed('认证失败')
        else:
            raise AuthenticationFailed('没得token')
```



### 编写视图

```python
def get_random(name):
    import hashlib
    import time
    md=hashlib.md5()
    md.update(bytes(str(time.time()),encoding='utf-8'))
    md.update(bytes(name,encoding='utf-8'))
    return md.hexdigest()
class Login(APIView):
    def post(self,reuquest):
        back_msg={'status':1001,'msg':None}
        try:
            name=reuquest.data.get('name')
            pwd=reuquest.data.get('pwd')
            user=models.User.objects.filter(username=name,password=pwd).first()
            if user:
                token=get_random(name)
                models.UserToken.objects.update_or_create(user=user,defaults={'token':token})
                back_msg['status']='1000'
                back_msg['msg']='登录成功'
                back_msg['token']=token
            else:
                back_msg['msg'] = '用户名或密码错误'
        except Exception as e:
            back_msg['msg']=str(e)
        return Response(back_msg)



class Course(APIView):
    authentication_classes = [TokenAuth, ]

    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        return HttpResponse('post')
```



### 全局使用

在settings.py文件中加上

```python
REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES":["app01.service.auth.Authentication",]
}
```



### 局部使用

在视图类中加上

```python
authentication_classes = [TokenAuth, ]
```



### 局部禁用
```python
authentication_classes = [ ]
```





## 权限

权限控制可以限制用户对于视图的访问和对于具体数据对象的访问。

- 在执行视图的dispatch()方法前，会先进行视图访问权限的判断
- 在通过get_object()获取具体对象时，会进行模型对象访问权限的判断



### 自定义权限

#### 编写权限类

```python
from rest_framework.permissions import BasePermission
class UserPermission(BasePermission):
    message = '不是超级用户，查看不了'
    def has_permission(self, request, view):
        # user_type = request.user.get_user_type_display()
        # if user_type == '超级用户':
        # 权限在认证之后，所以能取到user
        user_type = request.user.user_type
        print(user_type)
        if user_type == 1:
            return True
        else:
            return False
```



#### 全局使用

```python
REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES":["app01.service.auth.Authentication",],
    "DEFAULT_PERMISSION_CLASSES":["app01.service.permissions.SVIPPermission",]
}
```



#### 局部使用

```python
# 局部使用只需要在视图类里加入：
permission_classes = [UserPermission,]

```



#### 说明

如需自定义权限，需继承rest_framework.permissions.BasePermission父类，并实现以下两个任何一个方法或全部

- `.has_permission(self, request, view)`

  是否可以访问视图，view表示当前视图

- `.has_object_permission(self, request, view, obj)`

  是否可以访问数据对象，view表示当前对象，obj为数据对象



### 内置权限

####　内置权限类

```python
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
- AllowAny 允许所有用户
- IsAuthenticated 仅通过认证的用户
- IsAdminUser 仅管理员用户
- IsAuthenticatedOrReadOnly 已经登陆认证的用户可以对数据进行增删改操作，没有登陆认证的只能查看数据。
```



#### 全局使用

可以在配置文件中全局设置默认的权限管理类，如

```python
REST_FRAMEWORK = {
    ......
    'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAuthenticated',)
         }
```

如果未指明，则采用如下默认配置

```python
'DEFAULT_PERMISSION_CLASSES': (
   'rest_framework.permissions.AllowAny',
)
```



#### 局部使用

也可以在具体的视图中通过permission_classes属性来设置，如

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)
    ...
```



#### 实际操作

```python
# 创建超级用户，登陆到admin，创建普通用户（注意设置职员状态，也就是能登陆）
# 全局配置IsAuthenticated
# setting.py
'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
# urls.py
 path('test/', views.TestView.as_view()),
# views.py
class TestView(APIView):
    def get(self,request):
        return Response({'msg':'个人中心'})
# 登陆到admin后台后，直接访问可以，如果没登陆，不能访问

##注意：如果全局配置了
rest_framework.permissions.IsAdminUser
# 就只有管理员能访问，普通用户访问不了
```







## drf配置

> 浏览器响应成浏览器的格式，postman响应成json格式，通过配置实现的（默认配置）
>
> 不管是postman还是浏览器，都返回json格式数据
>
> drf有默认的配置文件---》先从项目的setting中找，找不到，采用默认的
>
> drf的配置信息，先从自己类中找--》项目的setting中找---》默认的找

- 局部使用:对某个视图类有效
      在视图类中写如下

  ​	`from rest_framework.renderers import JSONRenderer
  ​        renderer_classes=[JSONRenderer,]`

- 全局使用：全局的视图类，所有请求，都有效
      在setting.py中加入如下
          `REST_FRAMEWORK = {
              'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
                  'rest_framework.renderers.JSONRenderer',  # json渲染器
                  'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览API渲染器
              )
          }`

