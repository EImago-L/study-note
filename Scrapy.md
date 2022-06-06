# Scrapy

## Scrapy爬虫框架介绍

- 文档
  - [英文文档](https://docs.scrapy.org/en/latest/)
  - [中文文档](https://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html)

- 什么是scrapy

  基于`twisted`搭建的异步爬虫框架

  scrapy爬虫框架根据组件化设计理念和丰富的中间件，使其成为了一个兼具高性能和高拓展的框架

- scrapy提供的主要功能

  - **具有优先级功能的调度器**
  - 去重功能
  - 并发限制
  - IP使用次数限制
  - ....

- scrapy的使用场景

  - 不适合scrapy的项目场景
    - 业务非常简单，对性能要求也没有那么高，那么我们写多进程，多线程，异步脚本即可
    - 业务非常复杂，请求之间有顺序和失效时间的限制
    - 如果你遵守框架的主要设计理念，**那就不要使用框架**
  - 适合使用scrapy的项目
    - 数据量大，对性能又有一定要求，又去要用到**去重功能**和**优先级功能的调度器**



### **scrapy组件**

![](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/scrapy_architecture_02.png)

- `ENGINE`从`SPIDERS`中获取初始请求任务`requests`
- `ENGINE`得到`requests`之后发送给`SCHEDULER`，`SCHEDULER`对请求进行调度后产出任务
- `SCHEDULER`返回下一个请求任务给`ENGINE`，途径下载器中间件
- `ENGINE`将请求任务交给`DOWNLOADER`取完成下载任务，途径下载器中间件
- 一旦下载器完成请求任务，将产生一个`response`对象给`ENGINE`，途径下载器中间件
- `ENGINE`收到`response`对象后，将该对象发送给`SPIDERS`去解析和处理，途径爬虫中间件
- `SPIDER`解析返回结果
  - 将解析结果`ITEMS`发送给`ENGINE`
  - 生成一个新的`requests`任务发送给`ENGINE`
- 如果`ENGINE`拿到的是`ITEMS`，那么就会发送给`ITEM PIPELINES`做处理，如果是`requests`则发送给`SCHEDULER`
- 周而复始，直到没有任务产出



### **Scrapy安装**

- 安装

  ```
  pip install scrapy
  ```

- 创建项目

  ```
  scrapy startproject jd_crawler_scrapy
  ```

- 目录结构

  - spiders(目录)

    存放`SPIDERS`项目文件, 一个scrapy项目下可以有多个爬虫实例

  - items

    解析后的结构化结果.

  - middlewares

    下载器中间件和爬虫中间件的地方

  - piplines

    处理items的组件, 一般都在pipelines中完成items插入数据表的操作

  - settings

    统一化的全局爬虫配置文件

  - scrapy.cfg

    项目配置文件

- scrapy爬虫demo

  ```
  import scrapy
  
  
  class JdSearch(scrapy.Spider):
      name = "jd_search"
  
      def start_requests(self):
          for keyword in ["鼠标", "键盘", "显卡", "耳机"]:
              for page_num in range(1, 11):
                  url = f"https://search.jd.com/Search?keyword={keyword}&page={page_num}"
  
                  # 选用FormRequest是因为它既可以发送GET请求, 又可以发送POST请求
                  yield scrapy.FormRequest(
                      url=url,
                      method='GET',
                      # formdata=data,             # 如果是post请求, 携带数据使用formdata参数
                      callback=self.parse_search   # 指定回调函数处理response对象
                  )
  
  
      def parse_search(self, response):
          print(response)
  ```

- 启动爬虫

  ```
  scrapy crawl spider_name
  ```



## **Scrapy的启动和debug**

- 命令行

  ```python
   scrapy crawl jd_search
  ```

- 启动脚本

  ```python
  # 新建run.py
  
  from scrapy import cmdline
  
  command = "scrapy crawl jd_search".split()
  cmdline.execute(command)
  ```

  通过命令行启动不可以debug，我们可以通过创建启动脚本的方式来启动项目方便debug



### **Scrapy Item**

只是对解析的结构化结果进行一个约束, 在到达pipeline前就可以检查出数据错误.



### **Scrapy的设置**

- ROBOTTEXT_OBEY

  获取对方网站是否允许爬虫获取数据的信息.

- 设置中间件

  数字越小, 离`ENGINE`越近

  ```python
  DOWNLOADER_MIDDLEWARES = {
     # 'jd_crawler_scrapy.middlewares.JdCrawlerScrapyDownloaderMiddleware': 543,
     'jd_crawler_scrapy.middlewares.UAMiddleware': 100,
  }
  ```

- 设置PIPELINE

  ```python
  ITEM_PIPELINES = {
     'jd_crawler_scrapy.pipelines.JdCrawlerScrapyPipeline': 300,
  }
  ```

- 请求限制

  - **CONCURRENT_REQUESTS**

    请求并发数，通过控制请求并发数达到避免或延缓ip被封禁

    ```python
    CONCURRENT_REQUESTS = 1
    ```

  - CONCURRENT_REQUESTS_PER_DOMAIN

    控制每个`域名`请求的并发数

  - CONCURRENT_REQUESTS_IP

    控制每个`IP`请求的次数. 通过这样的方式可以过掉一些对IP封禁严格的网站.

  - CONCURRENT_ITEMS

    默认为100, 控制处理`item`的并发数. 如果我存入的数据库性能比较差, 通过这样的方式解决防止数据库崩溃的情况

  - **DOWNLOAD_DELAY**

    默认为0, 控制请求的频率. 在调度完一个请求后, 休息若干秒. 

    > Scrapy会自动帮我们进行随机休息    (DOWNLOAD_DELAY - 0.5, DOWNLOAD_DELAY + 0.5)

    ```
    DOWNLOAD_DELAY = 2
    ```

  - **DOWNLOAD_TIMEOUT**

    控制每个请求的超时时间. 通过这样的方式解决IP代理池质量差的问题.

    ```
    # 根据自己的IP代理池质量自定决定
    DOWNLOAD_TIMEOUT = 6   
    ```

  - **REDIRECT_ENABLE**

    默认为`True`, 建议修改为`False`, 因为大部分情况下, 重定向都是识别出你当前身份有问题, 重定向到`log in`页面

- 重试机制

  - **RETRY_ENABLE**

    ```
    RETYR_ENABLE = False
    ```

    默认为`True`, 建议改成`False`, 然后自己重写重试中间件

  - RETRY_TIMES

    控制重新次数,  RETRY_TIMES其实是当前项目的兜底配置

    > 如果当前请求失败后永远会重试, 正好你请求的接口是收费的, 万一有一天报错, 那么产生的费用是巨大的.

    ```
    RETRY_TIMES = 3
    ```

  - RETRY_HTTP_CODES

    ```
    RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
    ```

- 过滤器

  - **设置中指定过滤器**

    ```
    DUPEFILTER_CLASS = "jd_crawler_scrapy.middlewares.MyRFPDupeFilter"
    ```

  - **Spider中打开过滤器**

    ```
                  yield scrapy.FormRequest(
                        dont_filter=False,
                        url=url,
                        method='GET',
                        # formdata=data,           
                        callback=self.parse_search  
                    )
    ```

  - 过滤器

    ```python
    from scrapy.dupefilters import RFPDupeFilter
    from w3lib.url import canonicalize_url
    from scrapy.utils.python import to_bytes
    import hashlib
    import weakref
    
    _fingerprint_cache = weakref.WeakKeyDictionary()
    
    class MyRFPDupeFilter(RFPDupeFilter):
        """
        过滤器是在到达下载器之前就生成了过滤指纹, 如果我们的下载器中间件报错了, 那么过滤指纹仍然生效, 但是没有实际请求.
        所以我们可以通过一些特殊参数来进行自定义过滤规则
        """
        def request_fingerprint(self, request, include_headers=None, keep_fragments=False):
            cache = _fingerprint_cache.setdefault(request, {})
            cache_key = (include_headers, keep_fragments)
            if cache_key not in cache:
                fp = hashlib.sha1()
                fp.update(to_bytes(request.method))
                fp.update(to_bytes(canonicalize_url(request.url, keep_fragments=keep_fragments)))
                fp.update(request.body or b'')
                fp.update(request.meta.get("batch_no", "").encode("utf-8"))
                cache[cache_key] = fp.hexdigest()
            return cache[cache_key]
    ```

  

- LOG

  - LOG_ENABLE

    默认为`True`, 是否使用log

  - LOG_FILE 

    设置保存的log文件目录

  - LOG_LEVEL(按严重程序排序)

    - CRITICAL
    - ERROR
    - WARNING
    - INFO
    - DEBUG



### **Scrapy的中间件**

- 请求头中间件

  ```PYTHON
  class UAMiddleware:
      def process_request(self, request, spider):
          request.headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
  
  ```

- 重试中间件

  ```PYTHON
  from scrapy.downloadermiddlewares.retry import RetryMiddleware
  from scrapy.utils.response import response_status_message
  
  class MyRetryMiddleware(RetryMiddleware):
      """
      解决对方服务器返回正常状态码200, 但是根据IP需要进行验证码验证的情况.
      我们可以通过换IP可以解决验证码, 那么就应该重试.
      """
      def process_response(self, request, response, spider):
          if request.meta.get('dont_retry', False):
              return response
          if "验证码" in response.text:
              reason = response_status_message(response.status)
              return self._retry(request, reason, spider) or response
          return response
  ```



### **一个小demo**

```PYTHON
# jd_search.py

import scrapy
from jd_crawler_scrapy.items import JdCrawlerScrapyItem
from bs4 import BeautifulSoup
import json

class JdSearch(scrapy.Spider):
    name = "jd_search"

    def start_requests(self):
        for keyword in ["鼠标", "键盘", "显卡", "耳机"]:
            for page_num in range(1,51):
                url = f"https://search.jd.com/Search?keyword={keyword}&page={page_num}"
                yield scrapy.FormRequest(url=url,
                                         method="GET",
                                         callback=self.parse_search
                                         )


    def parse_search(self,response):
        soup = BeautifulSoup(response.text,"lxml")
        item_array = soup.select("ul[class='gl-warp clearfix'] li[class='gl-item']")
        for item in item_array:
            try:
                sku_id = item.attrs["data-sku"]
                img = item.select("img[data-img='1']")
                price = item.select("div[class='p-price']")
                title = item.select("div[class='p-name p-name-type-2']")
                shop = item.select("div[class='p-shop']")
                icons = item.select("div[class='p-icons']")

                img = img[0].attrs['data-lazy-img'] if img else ""
                price = price[0].strong.i.text if price else ""
                title = title[0].text.strip() if title else ""
                shop = shop[0].a.attrs['title'] if shop[0].text.strip() else ""
                icons = json.dumps([tag_ele.text for tag_ele in icons[0].select("i")]) if icons else ""

                item = JdCrawlerScrapyItem()
                item["sku_id"] = sku_id
                item["img"] = img
                item["price"] = price
                item["title"] = title
                item["shop"] = shop
                item["icons"] = icons
                yield item

            except Exception as e:
                print(e.args)
```



```python
# items.py

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdCrawlerScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sku_id = scrapy.Field()
    img = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    shop = scrapy.Field()
    icons = scrapy.Field()
```



```python
# middlewares.py

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class JdCrawlerScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JdCrawlerScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class UaMiddleware:
    def process_request(self, request, spider):
        request.headers["User-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
```



```python
# pipelines.py

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from jd_crawler_scrapy.items import JdCrawlerScrapyItem
class JdCrawlerScrapyPipeline:

    def __init__(self):
        self.mysql_con = None

    def process_item(self, item, spider):
        if not self.mysql_con:
            self.mysql_con = pymysql.connect(**spider.settings["MYSQL_CONF"])
            # print(settings.MYSQL_CONF)

        if isinstance(item,JdCrawlerScrapyItem):
            cursor = self.mysql_con.cursor()
            sql = """insert into jd_search(sku_id,img,price,title,shop,icons)
                    values ('{}','{}','{}','{}','{}','{}')""".format(
                item['sku_id'],item['img'],item['price'],item['title'],item['shop'],item['icons']
            )
            cursor.execute(sql)
            self.mysql_con.commit()
            cursor.close()
        return item
```



```python
# settings.py

# Scrapy settings for jd_crawler_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jd_crawler_scrapy'

SPIDER_MODULES = ['jd_crawler_scrapy.spiders']
NEWSPIDER_MODULE = 'jd_crawler_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jd_crawler_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jd_crawler_scrapy.middlewares.JdCrawlerScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'jd_crawler_scrapy.middlewares.JdCrawlerScrapyDownloaderMiddleware': 543,
   'jd_crawler_scrapy.middlewares.UaMiddleware': 100,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'jd_crawler_scrapy.pipelines.JdCrawlerScrapyPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#mysql_conf
MYSQL_CONF = {
   "host":"127.0.0.1",
   "user":"root",
   "password":"",
   "db":"jd"
}

LOG_FILE = r"D:\my_major\python\apeclass\jd_crawler_scrapy\jd.log"
LOG_LEVEL = "INFO"
```



## **Spider的用法**

- 定义爬取网站的动作
- 分析爬取下来的网页

我们定义的Spider继承自`scrapy.spider.Spider`，这是最基本的Spider类，一些特殊的Spider类也都是继承自它。



### **基础属性**

- name

  爬虫名称，定义Spider名字的字符串，**必须唯一**

- allowed_domains

  允许爬取的域名，可选。不在此范围的连接不会被跟进爬取

- start_url

  起始的url列表，我们没有实现`start_requests()`方法时，会默认从这个列表开始爬取

- custom_settings

  一个字典，专属于spider的配置，会覆盖全局设置。必须定义成类变量

- crawler

  由`from_crawler()`方法设置，代表本Spider对应的Crawler对象。包含很多项目组件。

- settings

  `Settings`对象可以得到全局设置变量



### **常用方法**

- start_requests()

  生成一个初始化请求，它必须返回一个可迭代对象。默认使用`start_urls`里面的url来构造`requests`发送get请求。如果想启用post，可以重写这个方法，发送post请求时使用`FormRequest`

- parse()

  如果`Response`没有指定回调函数，该方法会被默认调用，用来解析页面。该方法必须返回一个包含`Request`或`Item`的可迭代对象

- closed()

  当Spider关闭时，该方法会被调用，这里一般定义释放资源的一些操作或其他收尾操作



## **Downloader Midlleware用法**

下载中间件，位于`Scrapy`和`Response`之间的处理模块



### **核心方法**

- **`process_request(request, spider)`**

  `Request`被`Engine`调度给`Downloader`之前，`process_request()`方法会被调用。

  返回值必须为`None`、`Response`、`Request`对象之一，或者抛出`IgnoreRequest`异常。

  参数：

  - `request`：是Request对象
  - `spider`：是Spider对象

  返回值为`None`时，Scrapy继续处理`Request`，接着执行其他`Downloader Middleware`的`process_request()`方法，直到
  `Downloader`把`Request`执行后得到`Response`后结束。

  返回值为`Response`对象时，每个`Downloader Middleware`的`process_response()`方法会被依次调用。调用完毕后`Response`对象发送给`Spider`来处理。

  返回值为`Request`对象时，这个`Request`会重新放到调度队列里。

  `IgnoreRequest`异常抛出时，`Downloader Middleware`的`process_exception()`方法依次执行。如果没有一个方法处理异常，`Request`的`erroback()`方法就会回调，如果还没被处理，那只有算了。

- **`process_response(request, response,spider)`**

  `Downloader`执行`Request`下载之后，会得到对应的`Response`。`Scrapy`引擎便会将`Response`发送给`Spider`进行解析。在发送之前,我们都可以用`process_response()`方法来对`Response`进行处理。

  方法的返回值必须为`Request`对象、`Response`对象之一,或者抛出`IgnoreRequest`异常。

  参数：

  - `reuqest`：是Request对象
  - `spider`：是Spider对象
  - `response`：是Response对象

  返回值为`Request`对象时，这个`Request`会重新放到调度队列里

  返回值为`Response`对象时，更低优先级的`Downloader Middleware`的`process_response()`方法会继续调用,继续对该`Response`对象进行处理。

  如果`IgnoreRequest`异常抛出，则`Request`的`errorback()`方法会回调。如果该异常还没有被处理，那么它便会被忽略。

- **`process_exception(request, exception, spider)`**

  当`Downloader`或 `process requcst()`方法抛出异常时,例如抛出 `IgnoreRequest`异常，`process_exception()`方法就会被调用。方法的返回值必须为`None`、`Response`对象、`Request`对象之一。

  参数：

  - `reuqest`：是Request对象
  - `spider`：是Spider对象
  - `exception`：是Exception对象

  返回为`None`时，更低优先级的 `Downloader Middleware`的`process_exception()`会被继续顺次调用,直到所有的方法都被调度完毕。

  返回为`Response`对象时，更低优先级的`Downloader Middleware`的`process_exception()`方法不再被继续调用,每个`Downloader Middleware`的 `process_response()`方法转而被依次调用。

  当返回为`Request`对象时，更低优先级的`Downloader Middleware`的 `process_exception()`也不再被继续调用,该`Request`对象会重新放到调度队列里面等待被调度,它相当于一个全新的`Request`。然后,该`Request`又会被`process_request()`方法顺次处理。



### **一个小demo**

随机选择user-agent和修改response状态码

```python
# middlewares.py

class RandomUserAgentMiddleWare:
    def __init__(self):
        self.user_agents = [
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"
        ]

    def process_request(self,request,spider):
        request.headers["User-Agent"]  = random.choice(self.user_agents)

    def process_response(self,request,response,spider):
        response.status = 201
        return response
```



```python
#settings.py

DOWNLOADER_MIDDLEWARES = {
   'scrapydownloadertest.middlewares.RandomUserAgentMiddleWare': 543,
}
```



## **Spider Middleware的用法**

Spider Middleware有如下三个作用。

- 我们可以在`Downloader`生成的`Response`发送给`Spider`之前，也就是在`Response`发送给`Spider`之前对`Response`进行处理。

- 我们可以在`Spider`生成的 `Request`发送给`Scheduler`之前,也就是在`Request`发送给`Scheduler`之前对`Request`进行处理。
- 我们可以在`Spider`生成的`Item`发送给`Item Pipeline`之前，也就是在 `Item`发送给`Item Pipeline`之前对`Item`进行处理。



### **核心方法**

- **`process_spider_input(response, spider)`**

  当`Response`被`Spider Middleware`处理时，`process_spider_input()`方法被调用。

  应该返回`None`或抛出一个异常

  如果它返回 `None`，`Scrapy`将会继续处理该`Response`，调用所有其他的 `Spider Middleware，`直到`Spide`r处理该`Response`。

  如果它抛出一个异常，`Scrapy`将不会调用任何其他`Spider Middleware`的 `process_spider_input()`方法,而调用`Request` 的 `errback()`方法。`errback` 的输出将会被重新输入到中间件中,使用`process_spider_output()`方法来处理,当其抛出异常时则调用`process_spider_exception()`来处理。

- **`process_spider_output(response, result, spider)`**

  当`Spider`处理`Response`返回结果时,`process_spider_output()`方法被调用。

  必须返回`Request`或`Item`对象的可迭代对象

- **`process_spider_exception(response, exception, spider)`**

  当`Spider`或`Spider Middleware`的 process_spider_input()方法抛出异常时，`process_spider_exception()`方法被调用。

  该方法要么返回`None`，要么返回一个包含`Response`或`Item`对象的可迭代对象

  如果它返回`None`，`Scrapy`将继续处理该异常,调用其他`Spider Middleware`中的`process_spider_exception()`方法,直到所有`Spider Middleware`都被调用。

  如果它返回一个可迭代对象，则其他`Spider Middleware`的 `process_spider_output()`方法被调用,其他的`process_spider_exception()`不会被调用。

- **`process_start_requests(start_requests, spider)`**

  `process_start_requests()`方法以`Spider`启动的`Request`为参数被调用,执行的过程类似于`processspider_output()`，只不过它没有相关联的`Response`，并且必须返回`Request`。



## **Item Pipline的用法**

Item Pipeline的主要功能：

- 清理HTML数据
- 验证爬取数据、检查爬取字段
- 查重并丢弃重复内容
- 将爬取结果保存到数据库中



### **核心方法**

- **`process_item(item, spider)`**

  `process_item()`是必须要实现的方法，被定义的`Item Pipeline` 会默认调用这个方法对`Item`进行处理。比如，我们可以进行数据处理或者将数据写入到数据库等操作。它必须返回 `Item`类型的值或者抛出一个 `DropItem`异常。

  参数：

  - item：Item对象，被处理的item
  - spider：Spider对象，生成该Item的Spider

  如果它返回的是 `Item`对象，那么此`Item`会被低优先级的`Item Pipeline`的`process_item()`方法处理,直到所有的方法被调用完毕。

  如果它抛出的是`DropItem`异常,那么此 `Item`会被丢弃,不再进行处理。

- **`open_spider(spider)`**

  `open_spider()`方法是在`Spider`开启的时候被自动调用的。在这里我们可以做一些初始化操作，如开启数据库连接等。其中,参数`spider`就是被开启的 `Spider`对象。

- **`close_spider(spider)`**

  `close_spider()`方法是在`Spider` 关闭的时候自动调用的。在这里我们可以做一些收尾工作，如关闭数据库连接等。其中,参数`spider`就是被关闭的 `Spider`对象。

- **`from_crawler(cls, crawler)`**

  `from_crawler()`方法是一个类方法，用`@classmethod` 标识，是一种依赖注入的方式。它的参数是`crawler`，通过`crawler`对象，我们可以拿到`Scrapy`的所有核心组件，如全局配置的每个信息，然后创建一个`Pipeline`实例。参数cls就是Class,最后返回一个 Class实例。



### **一个小demo**

爬取https://image.so.com的美女图片，将信息保存在数据库中，图片保存在本地

```python
# images.py

import scrapy
import json
from urllib.parse import urlencode
from scrapy import Spider,Request
from images360.items import Images360Item


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {
            "ch": "beauty",
        }
        base_url = "https://image.so.com/zjl?"

        for page in range(1,self.settings.get("MAX_PAGE")+1):
            data["sn"] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get("list"):
            item = Images360Item()
            item["id"] = image.get("id")
            item["url"] = image.get("qhimg_url")
            item["title"] = image.get("title")
            item["thumb"] = image.get("qhimg_thumb")
            yield item

```



```python
# items.py

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Images360Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table = 'images'
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    thumb = scrapy.Field()

```



```python
# settings.py

# Scrapy settings for images360 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'images360'

SPIDER_MODULES = ['images360.spiders']
NEWSPIDER_MODULE = 'images360.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'images360 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'images360.middlewares.Images360SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'images360.middlewares.Images360DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'images360.pipelines.MysqlPipeline': 300,
   'images360.pipelines.ImagePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MAX_PAGE = 100

MYSQL_HOST = "127.0.0.1"
MYSQL_DATABASE = "images360"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""

IMAGES_STORE = './beauty'

```



```python
# pipelines.py

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Images360Pipeline:
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    def file_path(self,request,response=None,info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        yield Request(item['url'])

class MysqlPipeline:
    def __init__(self,host,database,user,password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            database = crawler.settings.get("MYSQL_DATABASE"),
            user = crawler.settings.get("MYSQL_USER"),
            password = crawler.settings.get("MYSQL_PASSWORD")
        )

    def open_spider(self,spider):
        self.db = pymysql.connect(
            self.host,
            self.user,
            self.password,
            self.database,
            charset="utf8"
        )
        self.cursor = self.db.cursor()

    def close_spider(self,spider):
        self.db.close()

    def process_item(self,item,spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = "insert into %s (%s) values (%s)" % (item.table,keys,values)
        self.cursor.execute(sql,tuple(data.values()))
        self.db.commit()
        return item
```

没有对middlewares.py进行修改 



## **Scrapy 通用爬虫**

### **CrawlSpider类**

官方文档：http://scrapy.readthedocs.io/en/latest/topics/spiders.html#crawlspider 

`CrawlSpider`继承自`Spider`类。除了`Spider`类的所有方法和属性,它还提供了一个非常重要的属性和方法。

- `rules`，它是爬取规则属性，是包含一个或多个Rule对象的列表。每个Rule对爬取网站的动作都做了定义，CrawlSpider会读取rules的每一个Rule并进行解析。
- `parse_start_url()`，它是一个可重写的方法。当start_urls里对应的Request得到 Response时，该方法被调用，它会分析Response并必须返回Item对象或者Request对象。



#### **Rule定义**

```python
classscrapy.spiders.Rule(link_extractor=None, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None, errback=None)
```



#### **Rule参数说明**

- `link_extractor`：是Link Extractor对象。通过它，Spider可以知道从爬取的页面中提取哪些链接。提取出的链接会自动生成 Request。它又是一个数据结构，一般常用LxmlLinkExtractor对象作为参数。

  ```python
  class scrapy.linkextractors.lxmlhtml.LxmllinkExtractor(allow=(), deny=(), allow_domains=(), deny_domains=(), deny_extnsions=None, restrict_xpaths=(), restrict_css=(), tags=('a','area'), attrs=('href', ), canonicalize=False, unique=True, process_value=None, strip=True) 
  ```

  - allow：正则表达式或正则表达式列表，符合正则的链接会被跟进。
  - deny：与上面相反，符合的正则不会被跟进。
  - allow_domains：域名白名单。
  - deny_domains：域名黑名单。
  - restrict_xpaths：定义当前页面提取链接的区域
  - restrict_css：与上面相同，只不过写的是css选择器

- `callback`：回调函数

- `cb_kwargs`：字典，回调函数的参数

- `follow`：布尔值，从response提取的链接是否会被跟进

- `process_links`：指定处理函数，从 link_extractor中获取到链接列表时，该函数将会调用,它主要用于过滤

- `process_request`：同样是指定处理函数,根据该Rule提取到每个Request时，该函数都会调用,对Request进行处理。该函数必须返回Request或者None。

#### **举个栗子**

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article\/.*\.html', restrict_xpaths='//div[@id="rank-defList"]//div[@class="item_con"]'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]//a[contains(.,"下一页")]'), follow=True),
    )
```





### **Item Loader类**

#### **API：**

```python
class scrapy.loader.ItemLoader([Item, selector, response], **kwargs)
```



#### **参数说明**

- `item`：它是Item对象，可以调用add_xpath()、add_css()或add_value()等方法来填充 Item对象
- `selector`：它是Selector对象,用来提取填充数据的选择器。
- `response`：它是Response对象，用于使用构造选择器的Response

##### **举个例子**

```python
from scrapyuniversal.items import NewsItem,ChinaLoader

    def parse_item(self, response):
        
        loader = ChinaLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//h1[@id="chan_newsTitle"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('text', '//div[@id="chan_newsDetail"]/p[position()<last()]/text()')
        loader.add_xpath('datetime', '//div[@class="chan_newsInfo_source"]/span[@class="time"]/text()')
        loader.add_xpath('source', '//div[@id="chan_newsInfo"]//text()', re='来源：(.*)')
        loader.add_value('website', "中华网")

        yield loader.load_item()
```



#### **常用的Processor**

- `Identity`

  Identity是最简单的Processor，不进行任何处理,直接返回原来的数据。

- `TakeFirst`

  TakeFirst返回列表的第一个非空值,类似extract_first()的功能,常用作Output Processor

  ```python
  from scrapy.loader.processors import TakeFirst
  processor = TakeFirst()
  print(processor([' ',1,2,3]))
  
  ### 1
  ```

- `Join`

  相当于字符串的join方法

  ```python
  from scrapy.loader.processors import Join
  processor = Join(',')
  print(processor(['one ', 'two' , 'three']))
  
  ### one,two,three
  ```

- `Compose`

  给定多个函数的组合，输入值会被指定的函数依次处理

  ```python
  from scrapy.loader.processors import Compose
  processor = Compose(str.upper, lambda s:s.strip())
  print(processor(' hello world'))
  
  ### HELLO WORLD
  ```

- `MapCompose`

  与`Compose`相似，迭代处理输入一个列表的值

  ```python
  from scrapy.loader.processors import MapCompose
  processor = MapCompose(str.upper, lambda s:s.strip())
  print(processor(["Hello", "World", "Python"]))
  
  ### ["HELLO", "WORLD", "PATHON"]
  ```

- `SelectJmes`

  查询json，传入key，返回value，需要先安装jmespath库

  ```python
  from scrapy.loader.processors import SelectJmes
  processor = SelectJmes('foo')
  print(processor({'foo': 'bar'}))
  
  ### bar
  ```

#### **举个栗子**

```python
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join,Compose


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    datetime = scrapy.Field()
    source = scrapy.Field()
    website = scrapy.Field()

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s:s.strip())
    source_out = Compose(Join(), lambda s:s.strip())
```



### **通用配置抽取**

#### **china.json**

```json
{
  "spider": "universal",
  "website": "中华科技网",
  "type": "新闻",
  "index": "http://tech.china.com",
  "settings": {
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
  },
  "start_urls": {
    "type" : "dynamic",
    "method": "china",
    "args":[
      5,
      10
    ]
  },
  "allowed_domains": [
    "tech.china.com"
  ],
  "rules": "china",
  "item": {
    "class": "NewsItem",
    "loader": "ChinaLoader",
    "attrs": {
      "title": [
        {
          "method": "xpath",
          "args": [
            "//h1[@id=\"chan_newsTitle\"]/text()"
          ]
        }
      ],
      "url": [
        {
          "method": "attr",
          "args": [
            "url"
          ]
        }
      ],
      "text": [
        {
          "method": "xpath",
          "args": [
            "//div[@id='chan_newsDetail']/p[position()<last()]/text()"
          ]
        }
      ],
      "datetime": [
        {
          "method": "xpath",
          "args": [
            "//div[@class='chan_newsInfo_source']/span[@class='time']/text()"
          ]
        }
      ],
      "source": [
        {
          "method": "xpath",
          "args": [
            "//div[@id='chan_newsInfo']//text()"
          ],
          "re": "来源：(.*)"
        }
      ],
      "website": [
        {
          "method": "value",
          "args": [
            "中华网"
          ]
        }
      ]
    }
  }
}
```

#### **rules.py**

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    "china":(
        Rule(LinkExtractor(allow=r'article\/.*\.html', restrict_xpaths='//div[@id="rank-defList"]//div[@class="item_con"]'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]//a[contains(.,"下一页")]'), follow=True),
    )
}
```

#### **utils.py**

```python
from os.path import realpath, dirname
import json

def get_config(name):
    path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    with open(path,'r',encoding='utf-8') as f:
        return json.loads(f.read())
```

#### **run.py**

```python
import sys
from scrapy.utils.project import get_project_settings
from scrapyuniversal.spiders.universal import UniversalSpider
from scrapyuniversal.utils import get_config
from scrapy.crawler import CrawlerProcess

def run():
    name = sys.argv[1]
    custom_settings = get_config(name)
    # 爬取使用的spider名称
    spider = custom_settings.get('spider','universal')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    # 合并配置
    settings.update(custom_settings.get('settings'))
    process = CrawlerProcess(settings)
    # 启动爬虫
    process.crawl(spider, **{'name':name})
    process.start()

if __name__ == "__main__":
    run()
```

#### **universal.py**

```python
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.utils import get_config
from scrapyuniversal.rules import rules
from scrapyuniversal import urls
from scrapyuniversal.items import NewsItem,ChinaLoader

class UniversalSpider(CrawlSpider):
    name = 'universal'
    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        start_urls = config.get("start_urls")
        if start_urls:
            if start_urls.get("type") == "static":
                self.start_urls = start_urls.get("value")
            if start_urls.get("type") == "dynamic":
                self.start_urls = list(eval('urls.' + start_urls.get("method"))(*start_urls.get("args", [])))
        self.allowed_domains = config.get("allowed_domains")
        super(UniversalSpider,self).__init__(*args,**kwargs)

    def parse_item(self, response):
        item = self.config.get("item")
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get("loader"))(cls,response=response)
            # 动态获取属性配置
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{'re':extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re':extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re':extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            yield loader.load_item()


```

#### **items.py**

```python
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join,Compose

class ScrapyuniversalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    datetime = scrapy.Field()
    source = scrapy.Field()
    website = scrapy.Field()

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s:s.strip())
    source_out = Compose(Join(), lambda s:s.strip())
```



## **Splash的使用**

Splash是一个JavaScript渲染服务，是一个带有HTTPAPI的轻量级浏览器，同时它对接了Python中的Twisted和 QT库。利用它,我们可以实现动态渲染页面的抓取。

使用Splash，我们可以实现如下功能：

- 异步方式处理多个网页渲染过程;
- 口获取渲染后的页面的源代码或截图;
- 通过关闭图片渲染或者使用Adblock规则来加快页面渲染速度;
- 可执行特定的JavaScript脚本;
- 可通过Lua脚本来控制页面渲染过程;
- 获取渲染的详细过程并通过HAR ( HTTP Archive)格式呈现。



### **Splash对象属性**

- **args**

  可以获取加载时的配置参数，如获取URL，如果请求为GET，可以获取GET请求参数；如果请求为post，可以获取表单数据

- **js_enabled**

  Splash的JavaScript执行开关，默认为True

  ```lua
  function main(splash, agrs)
    splash:go("https://www.baidu.com")
    splash.js_enabled = false
    local title = splash:evaljs("document.title")
    return {title=title}
  end
  ```

  这段代码会抛出异常，因为我们禁用js后执行了js代码

- **resource_timeout**

  设置加载的超时时间，单位秒。设置为0或nil代表不检查超时

  ```lua
  function main(splash, args)
    splash.resource_timeout = 0.1
    assert(splash:go('https://www.strongforu.top'))
    return splash:png()
  end
  ```

  这里将超时时间设置为0.1秒，如果超出响应时间就抛出异常

- **images_enabled**

  设置图片是否加载，默认情况下加载。禁用该属性可以提高网页加载速度。但是，禁用图片加载可能会影响js渲染。图片外层的DOM节点高度会受影响。

  另外值得注意的是，Splash使用了缓存。如果一开始加载出来了网页图片,然后禁用了图片加载,再重新加载页面，之前加载好的图片可能还会显示出来，这时直接重启Splash即可。

  ```lua
  function main(splash, args)
    splash.images_enabled = false
    assert(splash:go('https://www.strongforu.top'))
    return splash:png()
  end
  ```

- **plugins_enabled**

  控制浏览器插件是否开启。默认false

  ```lua
  splash.plugins_enabled = true/false
  ```

- **scroll_position**

  设置此属性，控制页面上下左右滚动

  ```lua
  function main(splash, args)
    assert(splash:go('http://www.strongforu.top'))
    splash.scroll_position = {y=400}
    return {png=splash:png()}
  end
  ```

  ![image-20211226163307084](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211226163307084.png)

  如果要让页面左右滚动，可以传入x参数

  ```lua
  splash.scroll_position = {x=100, y=200}
  ```



### **Splash对象方法**

- **go()**

  该方法用于请求连接，可以模拟get和post请求，同时支持传入请求头、表单等数据。

  ```lua
  ok, reason = splash:go{url, baseurl=nil, headers=nil, http_method="GET", body=nil, formdata=nil}
  ```

  参数：

  - url：请求的URL
  - baseurl：资源加载的相对路径
  - headers：请求头
  - http_method：默认GET，支持POST
  - body：发送POST请求时的表单数据，使用的Content-type为application/json
  - formdata：POST的时候的表单数据，使用的Content_tyoe为application/x-www-form-urlencoded

  该方法的返回结果时ok和reason的组合，如果ok为空则代表加载网页出现错误，此时的reason中包含错误原因

  ```lua
  function main(splash, args)
    local ok, rason = splash:go{"http://httpbin.org/post", http_method="POST", body="name=Germer"}
    if ok then
      return splash:html()
   	end
  end
  ```

  ![image-20211226165217650](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211226165217650.png)

- **wait()**

  控制页面等待时间

  ```lua
  ok,reason = splash:wait{time. cancel_on_redirect=false, cancel_on_error=true}
  ```

  参数：

  - time：等待的秒数
  - cancel_on_redirect：可选，默认false，表示如果发生重定向就停止等待，并返回重定向结果
  - cancel_on_error：可选，默认false，表示如果加载发生错误就停止等待

  返回结果同样是ok，reason的组合

  ```lua
  function main(splash, args)
    splash:go('http://www.taobao.com')
    splash:wait(2)
    return {html=splash:html()}
  end
  ```

  访问淘宝并等待2秒，随后返回页面源代码

- **jsfunc()**

  调用js定义的方法，但是所调用的方法需要用双中括号包围。

  ```lua
  function main(splash, args)
    local get_div_count = splash:jsfunc([[
      function(){
      var body = document.body;
      var divs = body.getElementsByTagName('div');
      return divs.length;
    }
      ]])
    splash:go('http://www.baidu')
    return ("The are %s DIVs"):format(get_div_count())
  end
  ```

- **evaljs()**

  执行js代码，并返回最后一条js语句的返回结果

  ```lua
  function main(splash, agrs)
    splash:go("http://www.baidu.com")
    local title = splash:evaljs("document.title")
    return title
  end
  ```

- **runjs()**

  执行js代码，与`evaljs()`类似，但更偏向于，执行某些动作和声明某些方法

  ```lua
  function main(splash, args)
    splash:go("https://www.baidu.com")
    splash:runjs("foo=function(){return 'bar'}")
    local result = splash:evaljs("foo()")
    return result
  end
  ```

- **autoload()**

  设置每个页面访问时自动加载的对象

  ```lua
  ok, reason = splash:autoload(source_or_url, source=nil,url=nil )
  ```

  参数

  - source_or_url：js代码或js库链接
  - source：js代码
  - url：js库链接

  此方法只负责加载js代码或库，不执行任何操作，如需执行操作，可以调用evaljs()或runjs()

  ```lua
  function main(splash, args)
    splash:autoload([[
      function get_document_title(){
      return document.title;
    }
      ]])
    splash:go("https://www.baidu.com")
    return splash:evaljs("get_document_title()")
  end
  ```

- **call_later()**

  设置定时任务和延迟时间来实现延时执行，并且可以在执行前通过`cancel()`方法重新执行定时任务。

  ```lua
  function main(splash, args)
    local snapshots = {}
    local timer = splash:call_later(function()
        snapshots["a"] = splash:png()
        splash:wait(1)
        snapshots["b"] = splash:png()
        end,0.2)
    splash:go("https://www.taobao.com")
    splash:wait(3)
    return snapshots
  end
  ```

- **http_get()**

  模拟发送HTTP的GET请求

  ```lua
  response = splash:http_get{url, headers=nil, follow_redirects=true}
  ```

  参数：

  - url：请求URL
  - headers：可选，默认为空，请求头
  - follow_redirects：可选，表示是否启动自动重定向，默认true

  ```lua
  function main(splash, args)
    local treat = require("treat")
    local response = splash:http_get("http://httpbin.org/get")
    return {
      html = treat.as_string(response.body),
      url = response.url,
      status = response.status
    }
  end
  ```

- **http_post()**

  和`http_get()`类似，此方法用来模拟发送POST请求，不过多了一个参数body

  ```lua
  response = splash:http_post{url, headers=nil, follow_redirects, nody=nil}
  ```

  参数：

  - url：请求URL
  - headers：可选，默认为空，请求头
  - follow_redirects：可选，表示是否启动自动重定向，默认true
  - body：可选，表单数据，默认为空

  ```lua
  function main(splash, args)
    local treat = require("treat")
    local json = require("json")
    local response = splash:http_post{
      "http://httpbin.org/post",
      body=json.encode({name="Germey"}),
      headers={["content-type"]="application/json"}
    }
    return {
      html=treat.as_string(response.body),
      url=response.url,
      status=response.status
    }
  end
  ```

- **html()**

  获取网页源代码

  ```lua
  function main(splash, args)
    splash:go("https://httpbin.org/get")
    return splash:html()
  end
  ```

- **png()**

  获取网页PNG格式截图

  ```lua
  function main(splash, args)
    splash:go("https://www.taobao.com")
    return splash:png()
  end
  ```

- **jpeg()**

  获取网页JPEG格式截图

- **har()**

  获取页面加载过程

  ```lua
  function main(splash, args)
    splash:go("https://www.strongforu.top")
    return splash:har()
  end
  ```

  ![image-20211226184549129](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211226184549129.png)

- **url()**

  获取当前正在访问的url

  ```lua
  function main(splash, args)
    splash:go("https://www.strongforu.top")
    return splash:url()
  end
  ```

- **get_cookies()**

  获取当前页面的Cookies

  ```lua
  function main(splash, args)
    splash:go("https://www.strongforu.top")
    return splash:get_cookies()
  end
  ```

- **add_cookie()**

  为当前页面添加Cookie

  ```lua
  cookies = splash:add_cookie{name,value,path=nil, domain=nil, expires=nil, httpOnly=nil, secure=nil}
  ```

  该方法的各个参数代表cookie的各个属性

  ```lua
  function main(splash, args)
    splash:add_cookie{"sessionid","1656515","/",domain="https://www.strongforu.top"}
    splash:go("https://www.strongforu.top")
    return splash:get_cookies()
  end
  ```

  ![image-20211226185722710](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211226185722710.png)

- **clear_cookies()**

  清楚所有cookies

- **get_viewport_size()**

  获取当前浏览器页面大小

  ```lua
  function main(splash, args)
    splash:go("https://strongforu.top")
    return splash:get_viewport_size()
  end
  ```

- **set_viewport_size()**

  设置当前浏览器页面大小

  ```lua
  function main(splash, args)
    splash:set_viewport_size(400,700)
    splash:go("https://strongforu.top")
    return splash:get_viewport_size()
  end
  ```

- **set_viewport_full()**

  设置浏览器全屏显示

  ```lua
  function main(splash, args)
    splash:set_viewport_full()
    splash:go("https://strongforu.top")
    return splash:png()
  end
  ```

- **set_user_agent()**

  设置浏览器的User_Agent()

  ```lua
  function main(splash, args)
    splash:set_user_agent("Splash")
    splash:go("http://httpbin.org/get")
    return splash:html()
  end
  ```

  ![image-20211226190458457](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211226190458457.png)

- **set_custom_headers()**

  设置请求头

  ```lua
  function main(splash, args)
    splash:set_custom_headers({
        ["User-Agent"] = "Splash",
        ["Site"] = "Splash",
      })
    splash:go("http://httpbin.org/get")
    return splash:html()
  end
  ```

  ![image-20211226190919693](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211226190919693.png)

- **select()**

  选择符合条件的第一个节点，若有多个节点符合，则只返回第一个，参数为CSS选择器

  ```lua
  function main(splash)
    splash:go("https://www.baidu.com")
    splash:select("#kw")
    splash:send_text("Splash")
    splash:wait(1)
    return splash:png()
  end
  ```

  ![image-20211226191238864](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211226191238864.png)

- **select_all()**

  返回所有符合条件的节点

  ```lua
  function main(splash)
    local treat = require("treat")
    assert(splash:go("http://quotes.toscrape.com"))
    assert(splash:wait(0.5))
    local texts = splash:select_all(".quote .text")
    local results = {}
    for index, text in ipairs(texts) do
      results[index] = text.node.innerHTML
    end
    return treat.as_array(results)
  end
  ```

- **mouce_click()**

  模拟鼠标点击操作，传入参数为x和y。也可以直接选中某个节点，然后调用此方法

  ```lua
  function main(splash, args)
    splash:go("https://www.baidu.com")
    input = splash:select('#kw')
    input:send_text('Splash')
    submit = splash:select('#su')
    submit:mouse_click()
    splash:wait(3)
    return splash:png()
  end
  ```



### **Splash API调用**

Splash给我们提供了一些HTTP API接口,我们只需要请求这些接口并传递相应的参数即可。

- **render.html**

  获取js渲染后的html代码，接口地址就是Splash的运行地址加上此接口的名称。

  我们给接口传递一个url参数来指定渲染的url，返回结果就是页面渲染后的源代码

  ```python
  import requests
  url = "http://localhost:8050/render.html?url=https://www.baidu.com"
  response = requests.get(url)
  print(response.text)
  ```

  还可以传入wait参数指定等待秒数

  ```python
  import requests
  url = "http://localhost:8050//render.html?url=https://www.baidu.com&wait=3"
  response = requests.get(url)
  print(response.text)
  ```

- **render.png**

  获取网页截图，可以通过设置width和height来控制宽高，返回png格式图片的二进制数据

  ```python
  import requests
  url = "http://localhost:8050/render.png"
  params = {
      "url":"https://www.baidu.com",
      "wait":"3",
      "width":"100",
      "height":"700"
  }
  response = requests.get(url=url,params=params)
  print(response.url)
  with open('strongforu.png','wb') as f:
      f.write(response.content)
  ```

- **render.jpeg**

  和render.png类似，只不过该接口返回jpeg格式的图片二进制数据，此接口比多了参数quality设置图片质量

- **render.har**

  返回页面加载过程的har数据

- **render.json**

  此接口包含前面接口的所有功能，返回结果是json格式

  ```python
  import requests
  url = "http://localhost:8050/render.json"
  params = {
      'url':"http:httpbin.org"
  }
  response = requests.get(url,params=params)
  print(response.json())
  ```

  ![image-20211227120842555](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211227120842555.png)

  我们可以通过传入不同参数控制其返回结果。比如,传入 html=1,返回结果即会增加源代码数据;传入png=1，返回结果即会增加页面PNG截图数据;传入 har=1，则会获得页面HAR数据。例如:

  ```python
  import requests
  url = "http://localhost:8050/render.json"
  params = {
      'url':"http:httpbin.org",
      'html':1,
      "png":1
  }
  response = requests.get(url,params=params)
  print(response.json())
  ```

- **execute**

  此接口可以实现与lua脚本的对接

  ```python
  import requests
  url = "http://47.95.212.59:8050/execute"
  lua = '''
  function main(splash, args)
    local treat = require("treat")
    local response = splash:http_get("http://httpbin.org/get")
    return {
      html = treat.as_string(response.body),
      url = response.url,
      status = response.status
    }
  end
  '''
  params = {
      'lua_source' : lua
  }
  response = requests.get(url,params=params)
  print(response.text)
  ```



### **Scrapy使用splash**

在scrapy的settings.py添加如下内容

```python
SPLASH_URL = 'http://localhost:8050'	#splash的地址

# 在downloader middleware和spidermiddleware中添加如下内容
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# 还需要配置一个去重的类DUPEFILTER_CLASS和Cache存储HTTPCACHE_STORAGE
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```

在spider中使用`SplashRequest`

```python
yield SplashRequest(url, self.parse_result,
    args={
        # optional; parameters passed to Splash HTTP API
        'wait': 0.5,
        # 'url' is prefilled from request url
        # 'http_method' is set to 'POST' for POST requests
        # 'body' is set to request body for POST requests
    },
    endpoint='render.json', # optional; default is render.html
    splash_url='<url>',     # optional; overrides SPLASH_URL
)
```



#### **举个栗子**

```python
from scrapy_splash import SplashRequest
from urllib.parse import quote

script = """
function main(splash, args)
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(args.wait))
  js = string.format("document.querySelector('#mainsrp-pager div.form > input').value=%d;document.querySelector('#mainsrp-pager div.form > span.btn.J_Submit').click()", args.page)
  splash:evaljs(js)
  assert(splash:wait(args.wait))
  return splash:html()
end
"""

class StaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://s.taobao.com/search?q='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE')+1):
                url = self.base_url + quote(keyword)
                yield SplashRequest(
                    url=url,
                    callback=self.parse,
                    endpoint='execute',
                    args={'lua_source':script,'page':page,'wait':4}
                )
```













