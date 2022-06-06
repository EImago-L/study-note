# **redis**

## **Redis安装**

| Redis官方网站                          | Redis中文官方网站 |
| -------------------------------------- | ----------------- |
| [**http://redis.io**](http://redis.io) | http://redis.cn/  |

![image-20211221114055472](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221114055472.png)

### **安装步骤**

安装C 语言的编译环境

```shell
yum install centos-release-scl scl-utils-build
yum install -y devtoolset-8-toolchain
scl enable devtoolset-8 bash

测试 gcc版本 
gcc --version
```

下载redis-6.2.1.tar.gz放/opt目录

 解压命令：tar -zxvf redis-6.2.1.tar.gz

解压完成后进入目录：cd redis-6.2.1

在redis-6.2.1目录下再次执行make命令（只是编译好）

​	如果没有准备好C语言编译环境，make 会报错—Jemalloc/jemalloc.h：没有那个文件

​	解决方案：运行make distclean

​	在redis-6.2.1目录下再次执行make命令（只是编译好）

跳过make test 继续执行: make install

安装目录：/usr/local/bin



查看默认安装目录：

- redis-benchmark：性能测试工具，可以在自己本子运行，看看自己本子性能如何
- redis-check-aof：修复有问题的AOF文件
- redis-check-dump：修复有问题的dump.rdb文件
- redis-sentinel：Redis集群使用
- redis-server：Redis服务器启动命令
- redis-cli：客户端，操作入口



### **启动Redis**

拷贝一份redis.conf到其他目录
cp /opt/redis-3.2.5/redis.conf /myredis

修改redis.conf文件将里面的daemonize no 改成 yes，让服务在后台启动

输入`redis-server/myredis/redis.conf`启动

在/usr/local/bin目录下输入`redis-cli`进入客户端







```shell
cp /opt/redis-6.2.6/redis.conf	/etc/redis.conf
#将daemonize no 改为 yes
# 启动:
redis-server /etc/redis.conf
```



## redis的五大数据类型

- string
- list
- set
- hash
- zset



## Redis健（key）

- keys * 	查看建库中所有key
- exists key	判断某个key是否存在

- type key 	查看你的key是什么类型

- del key 	删除指定的key数据

- unlink key	根据value选择非阻塞删除

  仅将keys从keyspace元数据中删除，正真的删除操作会在后续异步操作

- expire key 10    为给定的key设置过期时间

- ttl key    查看key还有多少秒过期

  -1表示永不过期，-2表示已经过期

- select    切换数据库

- dbsize    查看当前数据库的key的数量

- flushdb    清空当前库

- flushall    通杀全部库



## **Redis 字符串**

String是Redis最基本的类型，你可以理解成与Memcached一模一样的类型，一个key对应一个value。

String类型是二进制安全的。意味着Redis的string可以包含任何数据。比如jpg图片或者序列化的对象。

String类型是Redis最基本的数据类型，一个Redis中字符串value最多可以是512M

### **常用命令**

- `set <key> <value>`	添加键值对

  ![image-20211221123824136](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221123824136.png)

  - NX：当数据库中key不存在时，可以将key-value添加数据库

  - XX：当数据库中key存在时，可以将key-value添加数据库，与NX参数互斥
  - EX：key的超时秒数
  - PX：key的超时毫秒数，与EX互斥

- `get <key>`    查询对应健值

- `append <key> <value>`    将给定的value追加到原值的末尾

- `strlen <key>`   获取值的长度

- `setnx <key><value>`    只有key不存在时，设置key的值

- `incr <key>`    将key中存储的数字值增1,只能对数字值操作，如果为空，新增值为1

- `decr <key>`    将key中存储的数字值减1，只能对数字值操作，如果为空，新增值为-1

- `incrby/decrby <key> <步长>`    将存储的数字值增减，自定义步长

- `mset <key1> <value1> <key2> <value2>...`    同时设置一个或多个key-value对

- `mget <key1> <key2> ...`    同时获取一个或多个value

- `msetnx <key1> <value1> <key2> <value2>...`    同时设置一个或多个key-value对，当且仅当所有给定key都不存在

- `getrange <key> <起始位置> <结束位置>`    获取值的范围

- `setrange <key> <起始位置> <value>`    用value覆写key所存储的字符串值，从起始位置开始

- `setex <key> <过期时间> <value>`    设置键值的同时，设置过期时间，单位秒

- `getset <key> <value>`    以新换旧，设置了新值同时获取旧值 



### **数据结构**

String的数据结构为简单动态字符串(Simple Dynamic String,缩写SDS)。是可以修改的字符串，内部结构实现上类似于Java的ArrayList，采用预分配冗余空间的方式来减少内存的频繁分配.

![image-20211221124218446](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221124218446.png)

如图中所示，内部为当前字符串实际分配的空间capacity一般要高于实际字符串长度len。当字符串长度小于1M时，扩容都是加倍现有的空间，如果超过1M，扩容时一次只会多扩1M的空间。需要注意的是字符串最大长度为512M。



## **redis列表**

单键多值

Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）。

它的底层实际是个双向链表，对两端的操作性能很高，通过索引下标的操作中间的节点性能会较差。

![image-20211221130651465](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221130651465.png)



### 常用命令

- `lpush/rpush <key> <value1> <value2> <value3>...`    从左边/右边插入一个或多个值
- `lpoprpop <key>`   从左边/右边弹出一个值。值弹完后键也会没有
- `rpoplpush <key1> <key2>`    从key1的右边弹出一个值插入到key2的左边
- `lrange <key> <start> <stop>`    按照索引下标获得元素（从左往右）
- `lindex <key> <index>`    按照下标获取元素（从左往右）
- `llen <key>`    获得列表长度
- `linsert <key> before/after <value> <newvalue>`     在value之前/之后插入newvalue值
- `lrem <key> <n> <value>`    从左边删除n个value
- `lset <key> <index> <value>`    将列表key下标为index的值换成value





### **数据结构**

List的数据结构为快速链表quickList。

首先在列表元素较少的情况下会使用一块连续的内存存储，这个结构是ziplist，也即是压缩列表。

它将所有的元素紧挨着一起存储，分配的是一块连续的内存。

当数据量比较多的时候才会改成quicklist。

因为普通的链表需要的附加指针空间太大，会比较浪费空间。比如这个列表里存的只是int类型的数据，结构上还需要两个额外的指针prev和next。

![image-20211221130900490](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221130900490.png)

Redis将链表和ziplist结合起来组成了quicklist。也就是将多个ziplist使用双向指针串起来使用。这样既满足了快速的插入删除性能，又不会出现太大的空间冗余。



## **redis集合**

Redis set对外提供的功能与list类似是一个列表的功能，特殊之处在于set是可以**自动排重**的，当你需要存储一个列表数据，又不希望出现重复数据时，set是一个很好的选择，并且set提供了判断某个成员是否在一个set集合内的重要接口，这个也是list所不能提供的。

Redis的Set是string类型的无序集合。它底层其实是一个value为null的hash表，所以添加，删除，查找的**复杂度都是**O(1)。

一个算法，随着数据的增加，执行时间的长短，如果是O(1)，数据增加，查找数据的时间不变

### **常用命令**

- `sadd <key> <value1> <value2>...`    将一个或多个元素加入到key中，已有的元素将会被忽略
- `smembers <key>`    取出该集合的所有值
- `sismember <key> <value>`    判断集合\<key>是否含有该\<value>值，有1，没有0
- `scard <key>`    返回该集合的元素个数
- `srem <key> <value1> <value2>...`    删除集合中的某个元素
- `spop <key>`    随机从该集合中吐出一个值
- `srandmember <key> <n>`    随机从该集合中取出n个值。不会从集合中删除
- `smove <source> <destination> value` 把集合中一个值从一个集合移动到另一个集合
- `sinter <key1> <key2>`    返回两个集合的交集元素
- `sunion <key1> <key2>`   返回连个集合的并集
- `sdiff <key1> <key2>`     返回两个集合的差集



### **数据结构**

Set数据结构是dict字典，字典是用哈希表实现的。

Java中HashSet的内部实现使用的是HashMap，只不过所有的value都指向同一个对象。Redis的set结构也是一样，它的内部也使用hash结构，所有的value都指向同一个内部值。



## **redis hash**

Redis hash 是一个键值对集合。

Redis hash是一个string类型的field和value的映射表，hash特别适合用于存储对象。

类似Java里面的Map<String,Object>

用户ID为查找的key，存储的value用户对象包含姓名，年龄，生日等信息，如果用普通的key/value结构来存储


### **常用命令**

- `hset <key> <field> <value>`    给key集合中的field键赋值value
- `hget <hey1> <field>`    从key1集合field取出value
- `hmset <key1> <field1> <value1> <field2> <value2>...`    批量设置hash的值
- `hexists <key> <field>`    查看哈希表key中，给定field是否存在
- `hkeys <key>`    列出该hash集合的所有field
- `hvals <key>`    列出还hash集合中所有value
- `hincrby <key> <field> <increment>`    为哈希表key中的域field 的值加上增量
- `hsetnx <key> <field> <value>`    将哈希表key中的field的值设置为value 当且仅当field不存在


### **数据结构**

Hash类型对应的数据结构是两种：ziplist（压缩列表），hashtable（哈希表）。当field-value长度较短且个数较少时，使用ziplist，否则使用hashtable。



## **redis有序集合zset**

Redis有序集合zset与普通集合set非常相似，是一个没有重复元素的字符串集合。

不同之处是有序集合的每个成员都关联了一个**评分（score）**,这个评分（score）被用来按照从最低分到最高分的方式排序集合中的成员。集合的成员是唯一的，但是评分可以是重复了 。

因为元素是有序的, 所以你也可以很快的根据评分（score）或者次序（position）来获取一个范围的元素。

访问有序集合的中间元素也是非常快的,因此你能够使用有序集合作为一个没有重复成员的智能列表。

### **常用命令**

- `zadd <key> <score1> <value1> <score2> <value2>...`     将一个或多个member元素及其score值加入到有序集key中
- `zrange <key> <start> <stop> [withscores]`    返回有序集key中，下标start top之间的元素，带withscores 可以让分数一起返回
- `zrangebyscore <key> <min> <max> [withscores] [limit offset count]`    返回key中，所有score位于min和max之间的成员，按score从小到大依次排序
- `zrevrangebyscore <key> <max> <min> [withscores] [limit offset count]`    同上，从大到小排序
- `zincrby <key> <increment> <value>`    为元素的score加上增量
- `zrem <key> <value>`     删除该集合下，指定值的元素
- `zcount <key> <min> <max>`    统计该集合，分数区间内的元素个数
- `zrank <key> <value>` 返回该值在集合中的排名，从0 开始  



### **数据结构**

SortedSet(zset)是Redis提供的一个非常特别的数据结构，一方面它等价于Java的数据结构Map<String, Double>，可以给每一个元素value赋予一个权重score，另一方面它又类似于TreeSet，内部的元素会按照权重score进行排序，可以得到每个元素的名次，还可以通过score的范围来获取元素的列表。

zset底层使用了两个数据结构

- hash，hash的作用就是关联元素value和权重score，保障元素value的唯一性，可以通过元素value找到相应的score值。

- 跳跃表，跳跃表的目的在于给元素value排序，根据score的范围获取元素列表。

#### **跳跃表**

有序集合在生活中比较常见，例如根据成绩对学生排名，根据得分对玩家排名等。对于有序集合的底层实现，可以用数组、平衡树、链表等。数组不便元素的插入、删除；平衡树或红黑树虽然效率高但结构复杂；链表查询需要遍历所有效率低。Redis采用的是跳跃表。跳跃表效率堪比红黑树，实现远比红黑树简单。

实例：
对比有序链表和跳跃表，从链表中查询出51

1. 有序表

   ![image-20211221141950766](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221141950766.png)

   要查找值为51的元素，需要从第一个元素开始依次查找、比较才能找到。共需要6次比较。

2. 跳跃表

   ![image-20211221142012743](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142012743.png)

   从第2层开始，1节点比51节点小，向后比较。

   21节点比51节点小，继续向后比较，后面就是NULL了，所以从21节点向下到第1层

   在第1层，41节点比51节点小，继续向后，61节点比51节点大，所以从41向下

   在第0层，51节点为要查找的节点，节点被找到，共查找4次。

   从此可以看出跳跃表比有序链表效率要高

   

## **redis bitmaps**

现代计算机用二进制（位） 作为信息的基础单位， 1个字节等于8位， 例如“abc”字符串是由3个字节组成， 但实际在计算机存储时将其用二进制表示， “abc”分别对应的ASCII码分别是97、 98、 99， 对应的二进制分别是01100001、 01100010和01100011，如下图

![image-20211221142251272](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142251272.png)

合理地使用操作位能够有效地提高内存使用率和开发效率。

Redis提供了Bitmaps这个“数据类型”可以实现对位的操作：

- Bitmaps本身不是一种数据类型， 实际上它就是字符串（key-value） ， 但是它可以对字符串的位进行操作。
-  Bitmaps单独提供了一套命令， 所以在Redis中使用Bitmaps和使用字符串的方法不太相同。 可以把Bitmaps想象成一个以位为单位的数组， 数组的每个单元只能存储0和1， 数组的下标在Bitmaps中叫做偏移量。

 ![image-20211221142328483](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142328483.png)

 

### **命令常用**

- `setbit<key> <offset> <value>`    设置Bitmaps中某个偏移量的值（0或1）

  ![image-20211221142500216](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142500216.png)

  offset:偏移量从0开始

  实例：每个独立用户是否访问过网站存放在Bitmaps中， 将访问的用户记做1， 没有访问的用户记做0， 用偏移量作为用户的id。

  设置键的第offset个位的值（从0算起） ， 假设现在有20个用户，userid=1， 6， 11， 15， 19的用户对网站进行了访问， 那么当前Bitmaps初始化结果如图
  ![image-20211221142545420](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142545420.png)

  unique:users:20201106代表2020-11-06这天的独立访问用户的Bitmaps

  ![image-20211221142611043](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142611043.png)

  很多应用的用户id以一个指定数字（例如10000） 开头， 直接将用户id和Bitmaps的偏移量对应势必会造成一定的浪费， 通常的做法是每次做setbit操作时将用户id减去这个指定数字。

  在第一次初始化Bitmaps时， 假如偏移量非常大， 那么整个初始化过程执行会比较慢， 可能会造成Redis的阻塞。

- `getbit <key> <offset>`    获取Bitmaps中某个偏移量的值

  ![image-20211221142706481](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142706481.png)

  实例：
  获取id=8的用户是否在2020-11-06这天访问过， 返回0说明没有访问过：
  ![image-20211221142728425](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142728425.png)

- `bitcount <key> [start end]`      统计字符串从start字节到end字节比特值为1的数量

  实例：
  计算2022-11-06这天的独立访问用户数量
  ![image-20211221142832224](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142832224.png)

  start和end代表起始和结束字节数， 下面操作计算用户id在第1个字节到第3个字节之间的独立访问用户数， 对应的用户id是11， 15， 19。

  ![image-20211221142854337](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221142854337.png)

   注意：redis的setbit设置或清除的是bit位置，而bitcount计算的是byte位置。

- `bitop and(or/not/xor) <destkey> [key…]`    bitop是一个复合操作， 它可以做多个Bitmaps的and（交集） 、 or（并集） 、 not（非） 、 xor（异或） 操作并将结果保存在destkey中。

  实例：2020-11-04 日访问网站的userid=1,2,5,9。

  setbit unique:users:20201104 1 1

  setbit unique:users:20201104 2 1

  setbit unique:users:20201104 5 1

  setbit unique:users:20201104 9 1

   

  2020-11-03 日访问网站的userid=0,1,4,9。

  setbit unique:users:20201103 0 1

  setbit unique:users:20201103 1 1

  setbit unique:users:20201103 4 1

  setbit unique:users:20201103 9 1

   

  计算出两天都访问过网站的用户数量

  bitop and unique:users:and:20201104_03 unique:users:20201103 unique:users:20201104

  ![image-20211221143043157](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221143043157.png)

  ![image-20211221143127463](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221143127463.png)

  计算出任意一天都访问过网站的用户数量（例如月活跃就是类似这种） ， 可以使用or求并集

  ![image-20211221143139344](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221143139344.png)



### **Bitmaps与set对比**

假设网站有1亿用户， 每天独立访问的用户有5千万， 如果每天用集合类型和Bitmaps分别存储活跃用户可以得到表

| set和Bitmaps存储一天活跃用户对比 |                    |                  |                        |
| -------------------------------- | ------------------ | ---------------- | ---------------------- |
| 数据  类型                       | 每个用户id占用空间 | 需要存储的用户量 | 全部内存量             |
| 集合  类型                       | 64位               | 50000000         | 64位*50000000 = 400MB  |
| Bitmaps                          | 1位                | 100000000        | 1位*100000000 = 12.5MB |

 

很明显， 这种情况下使用Bitmaps能节省很多的内存空间， 尤其是随着时间推移节省的内存还是非常可观的

| set和Bitmaps存储独立用户空间对比 |        |        |       |
| -------------------------------- | ------ | ------ | ----- |
| 数据类型                         | 一天   | 一个月 | 一年  |
| 集合类型                         | 400MB  | 12GB   | 144GB |
| Bitmaps                          | 12.5MB | 375MB  | 4.5GB |

 

但Bitmaps并不是万金油， 假如该网站每天的独立访问用户很少， 例如只有10万（大量的僵尸用户） ， 那么两者的对比如下表所示， 很显然， 这时候使用Bitmaps就不太合适了， 因为基本上大部分位都是0。

| set和Bitmaps存储一天活跃用户对比（独立用户比较少） |                    |                  |                        |
| -------------------------------------------------- | ------------------ | ---------------- | ---------------------- |
| 数据类型                                           | 每个userid占用空间 | 需要存储的用户量 | 全部内存量             |
| 集合类型                                           | 64位               | 100000           | 64位*100000 = 800KB    |
| Bitmaps                                            | 1位                | 100000000        | 1位*100000000 = 12.5MB |

 



## **redis hyperloglog**

### **简介**

在工作当中，我们经常会遇到与统计相关的功能需求，比如统计网站PV（PageView页面访问量）,可以使用Redis的incr、incrby轻松实现。

但像UV（UniqueVisitor，独立访客）、独立IP数、搜索记录数等需要去重和计数的问题如何解决？这种求集合中不重复元素个数的问题称为基数问题。

解决基数问题有很多种方案：

1. 数据存储在MySQL表中，使用distinct count计算不重复个数

2. 使用Redis提供的hash、set、bitmaps等数据结构来处理

以上的方案结果精确，但随着数据不断增加，导致占用空间越来越大，对于非常大的数据集是不切实际的。

能否能够降低一定的精度来平衡存储空间？Redis推出了HyperLogLog

Redis HyperLogLog 是用来做基数统计的算法，HyperLogLog 的优点是，在输入元素的数量或者体积非常非常大时，计算基数所需的空间总是固定的、并且是很小的。

在 Redis 里面，每个 HyperLogLog 键只需要花费 12 KB 内存，就可以计算接近 2^64 个不同元素的基数。这和计算基数时，元素越多耗费内存就越多的集合形成鲜明对比。

但是，因为 HyperLogLog 只会根据输入元素来计算基数，而不会储存输入元素本身，所以 HyperLogLog 不能像集合那样，返回输入的各个元素。

什么是基数?

比如数据集 {1, 3, 5, 7, 5, 7, 8}， 那么这个数据集的基数集为 {1, 3, 5 ,7, 8}, 基数(不重复元素)为5。 基数估计就是在误差可接受的范围内，快速计算基数。



### **常用命令**

- `pfadd <key> < element> [element ...]`      添加指定元素到 HyperLogLog 中

  ![image-20211221143623895](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221143623895.png)

  实例：
  ![image-20211221143645339](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221143645339.png)

  将所有元素添加到指定HyperLogLog数据结构中。如果执行命令后HLL估计的近似基数发生变化，则返回1，否则返回0。

- `pfcount <key> [key ...]`     计算HLL的近似基数，可以计算多个HLL，比如用HLL存储每天的UV，计算一周的UV可以使用7天的UV合并计算即可

  实例：
  ![image-20211221143756240](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221143756240.png)

- `pfmerge <destkey> <sourcekey> [sourcekey ...]` 将一个或多个HLL合并后的结果存储在另一个HLL中，比如每月活跃用户可以使用每天的活跃用户来合并计算可得

  ![image-20211221143823145](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221143823145.png)

  实例：
  ![image-20211221143834376](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221143834376.png)

  



## **redis geospatial**

###  **简介**

Redis 3.2 中增加了对GEO类型的支持。GEO，Geographic，地理信息的缩写。该类型，就是元素的2维坐标，在地图上就是经纬度。redis基于该类型，提供了经纬度设置，查询，范围查询，距离查询，经纬度Hash等常见操作。



### **常用命令**

- `geoadd <key> < longitude> <latitude> <member> [longitude latitude member...]`   添加地理位置（经度，纬度，名称）

  ![image-20211221144140216](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221144140216.png)

  实例：

  `geoadd china:city 121.47 31.23 shanghai`

  `geoadd china:city 106.50 29.53 chongqing 114.05 22.52 shenzhen 116.38 39.90 beijing`

  ![image-20211221144232100](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221144232100.png)

  两极无法直接添加，一般会下载城市数据，直接通过程序一次性导入。

  有效的经度从 -180 度到 180 度。有效的纬度从 -85.05112878 度到 85.05112878 度。

  当坐标位置超出指定范围时，该命令将会返回一个错误。

  已经添加的数据，是无法再次往里面添加的。

- `geopos <key> <member> [member...]`     获得指定地区的坐标值

  ![image-20211221144330982](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221144330982.png)

  实例：
  ![image-20211221144357981](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221144357981.png)

- `geodist <key> <member1> <member2> [m|km|ft|mi ]`     获取两个位置之间的直线距离

  实例：
  获取两个位置之间的直线距离

  ![image-20211221144455973](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221144455973.png)

  单位：

  m 表示单位为米[默认值]。

  km 表示单位为千米。

  mi 表示单位为英里。

  ft 表示单位为英尺。

  如果用户没有显式地指定单位参数， 那么 GEODIST 默认使用米作为单位

- `georadius <key> < longitude> <latitude> radius [m|km|ft|mi]`  以给定的经纬度为中心，找出某一半径内的元素

  ![image-20211221144549355](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221144549355.png)

  经度 纬度 距离 单位

  实例：
  ![image-20211221144626388](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221144626388.png)



## **Redis 事务与锁机制**

### **定义**

Redis事务是一个单独的隔离操作：事务中的所有命令都会序列化、按顺序地执行。事务在执行的过程中，不会被其他客户端发送来的命令请求所打断。

**Redis事务的主要作用就是串联多个命令防止别的命令插队**。



### **Multi、Exec、Discard**

从输入Multi命令开始，输入的命令都会依次进入命令队列中，但不会执行，直到输入Exec后，Redis会将之前的命令队列中的命令依次执行。

组队的过程中可以通过discard来放弃组队。

![image-20211221121304274](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221121304274.png)

![image-20211221121316857](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221121316857.png)

组队成功，提交成功



![image-20211221121329676](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221121329676.png)

组队阶段报错，提交失败



### **事务的报错处理**

组队中某个命令出现了报告错误，执行时整个的所有队列都会被取消。

![image-20211221121437503](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221121437503.png)

如果执行阶段某个命令报出了错误，则只有报错的命令不会被执行，而其他的命令都会执行，不会回滚。

![image-20211221121452820](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221121452820.png)



### **事务冲突问题**

一个请求想给金额减8000

一个请求想给金额减5000

一个请求想给金额减1000

![image-20211221122439819](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221122439819.png)

3个线程同时对金额进行操作，最后金额为负，这样肯定会出问题。我们给金额加上锁来解决

#### **悲观锁**

![image-20211221122639959](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221122639959.png)

**悲观锁(Pessimistic Lock)**, 顾名思义，就是很悲观，每次去拿数据的时候都认为别人会修改，所以每次在拿数据的时候都会上锁，这样别人想拿这个数据就会block直到它拿到锁。**传统的关系型数据库里边就用到了很多这种锁机制**，比如**行锁**，**表锁**等，**读锁**，**写锁**等，都是在做操作之前先上锁。

#### **乐观锁**

![image-20211221122711973](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221122711973.png)

**乐观锁(Optimistic Lock),** 顾名思义，就是很乐观，每次去拿数据的时候都认为别人不会修改，所以不会上锁，但是在更新的时候会判断一下在此期间别人有没有去更新这个数据，可以使用版本号等机制。**乐观锁适用于多读的应用类型，这样可以提高吞吐量**。Redis就是利用这种check-and-set机制实现事务的。



#### **watch key [key ...]**

在执行multi之前，先执行watch key1 [key2],可以监视一个(或多个) key ，如果在事务**执行之前这个(或这些) key 被其他命令所改动，那么事务将被打断。**

![image-20211221123510147](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221123510147.png)

#### **unwatch**

取消 WATCH 命令对所有 key 的监视。

如果在执行 WATCH 命令之后，EXEC 命令或DISCARD 命令先被执行了的话，那么就不需要再执行UNWATCH 了。



### **Redis事务三特性**

- 单独的隔离操作

  事务中的所有命令都会序列化、按顺序地执行。事务在执行的过程中，不会被其他客户端发送来的命令请求所打断。

- 没有隔离级别的概念 

  队列中的命令没有提交之前都不会实际被执行，因为事务提交前任何指令都不会被实际执行

- 不保证原子性

  事务中如果有一条命令执行失败，其后的命令仍然会被执行，没有回滚



## **Redis 持久化**

Redis 提供了2个不同形式的持久化方式。

- RDB（Redis DataBase）

- AOF（Append Of File）



### **RDB**

在指定的**时间间隔**内将内存中的数据集**快照**写入磁盘， 也就是行话讲的Snapshot快照，它恢复时是将快照文件直接读到内存里



#### **如何执行？**

Redis会单独创建（fork）一个子进程来进行持久化，会先将数据写入到 一个临时文件中，待持久化过程都结束了，再用这个临时文件替换上次持久化好的文件。 整个过程中，主进程是不进行任何IO操作的，这就确保了极高的性能 如果需要进行大规模数据的恢复，且对于数据恢复的完整性不是非常敏感，那RDB方式要比AOF方式更加的高效。**RDB的缺点是最后一次持久化后的数据可能丢失**。



#### **Fork**

- Fork的作用是复制一个与当前进程一样的进程。新进程的所有数据（变量、环境变量、程序计数器等） 数值都和原进程一致，但是是一个全新的进程，并作为原进程的子进程
- 在Linux程序中，fork()会产生一个和父进程完全相同的子进程，但子进程在此后多会exec系统调用，出于效率考虑，Linux中引入了“**写时复制技术**”
- **一般情况父进程和子进程会共用同一段物理内存**，只有进程空间的各段的内容要发生变化时，才会将父进程的内容复制一份给子进程。
- 

#### **持久化流程**

![image-20211221152935693](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221152935693.png)

#### **dump.rdb文件**

在redis.conf中配置文件名称，默认为dump.rdb

![image-20211221153031089](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221153031089.png)

##### **配置位置**

rdb文件的保存路径，也可以修改。默认为Redis启动时命令行所在的目录下

dir "/myredis/"

![image-20211221153204437](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221153204437.png)



#### **如何开启RDB快照**

![image-20211221153402868](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221153402868.png)

**命令：**

- `save` ：save时只管保存，其它不管，全部阻塞。手动保存。不建议。

  格式：save 秒钟 写操作次数

- `bgsave`：Redis会在后台异步进行快照操作， **快照同时还可以响应客户端请求。**

可以通过lastsave 命令获取最后一次成功执行快照的时间

`flushall`命令：执行flushall命令，也会产生dump.rdb文件，但里面是空的，无意义

RDB是整个内存的压缩过的Snapshot，RDB的数据结构，可以配置复合的快照触发条件，

默认是1分钟内改了1万次，或5分钟内改了10次，或15分钟内改了1次。

**禁用**：
不设置save指令，或者给save传入空字符串



#### **stop-writes-on-bgsave-error**

![image-20211221154002177](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221154002177.png)

当Redis无法写入磁盘的话，直接关掉Redis的写操作。推荐yes.



#### **rdbcompression 压缩文件**

![image-20211221154052183](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221154052183.png)

对于存储到磁盘中的快照，可以设置是否进行压缩存储。如果是的话，redis会采用LZF算法进行压缩。

如果你不想消耗CPU来进行压缩的话，可以设置为关闭此功能。推荐yes.



#### **rdbchecksum** **检查完整性**

![image-20211221154123170](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221154123170.png)



在存储快照后，还可以让redis使用CRC64算法来进行数据校验，

但是这样做会增加大约10%的性能消耗，如果希望获取到最大的性能提升，可以关闭此功能

推荐yes.



#### **rdb的备份**

先通过config get dir 查询rdb文件的目录 

将*.rdb的文件拷贝到别的地方

rdb的恢复

- 关闭Redis

- 先把备份的文件拷贝到工作目录下 cp dump2.rdb dump.rdb

- 启动Redis, 备份数据会直接加载



#### **优势**

- 适合大规模的数据恢复

- 对数据完整性和一致性要求不高更适合使用

- 节省磁盘空间

- 恢复速度快

#### **劣势**

- Fork的时候，内存中的数据被克隆了一份，大致2倍的膨胀性需要考虑

- 虽然Redis在fork时使用了**写时拷贝技术**,但是如果数据庞大时还是比较消耗性能。

- 在备份周期在一定间隔时间做一次备份，所以如果Redis意外down掉的话，就会丢失最后一次快照后的所有修改。



#### **如何停止**

动态停止RDB：redis-cli config set save ""#save后给空值，表示禁用保存策略



### **AOF**

以**日志**的形式来记录每个写操作（增量保存），将Redis执行过的所有写指令记录下来(**读操作不记录**)， **只许追加文件但不可以改写文件**，redis启动之初会读取该文件重新构建数据，换言之，redis 重启的话就根据日志文件的内容将写指令从前到后执行一次以完成数据的恢复工作



#### **AOF持久化流程**

1. 客户端的请求写命令会被append追加到AOF缓冲区内；
2. AOF缓冲区根据AOF持久化策略[always,everysec,no]将操作sync同步到磁盘的AOF文件中；
3. AOF文件大小超过重写策略或手动重写时，会对AOF文件rewrite重写，压缩AOF文件容量；
4. Redis服务重启时，会重新load加载AOF文件中的写操作达到数据恢复的目的；

![image-20211221165602910](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221165602910.png)

#### **AOF启动/修复/恢复**

-  AOF的备份机制和性能虽然和RDB不同, 但是备份和恢复的操作同RDB一样，都是拷贝备份文件，需要恢复时再拷贝到Redis工作目录下，启动系统即加载。
- 正常恢复
  - 修改默认的appendonly no，改为yes
  - 将有数据的aof文件复制一份保存到对应目录(查看目录：config get dir)
  - 恢复：重启redis然后重新加载
- 异常恢复
  - 修改默认的appendonly no，改为yes
  - 如遇到**AOF文件损坏**，通过/usr/local/bin/redis-check-aof--fix appendonly.aof进行恢复
  - 备份被写坏的AOF文件
  - 恢复：重启redis，然后重新加载

可以在redis.conf中配置文件名称，默认为 appendonly.aof

AOF文件的保存路径，同RDB的路径一致。

AOF和RDB同时开启，系统默认取AOF的数据（数据不会存在丢失）



#### **AOF同步频率设置**

- appendfsync always

  始终同步，每次Redis的写入都会立刻记入日志；性能较差但数据完整性比较好

- appendfsync everysec

  每秒同步，每秒记入日志一次，如果宕机，本秒的数据可能丢失。

- appendfsync no

  redis不主动进行同步，把同步时机交给操作系统。



#### **Rewrite 压缩**

##### **是什么？**

AOF采用文件追加方式，文件会越来越大为避免出现此种情况，新增了重写机制, 当AOF文件的大小超过所设定的阈值时，Redis就会启动AOF文件的内容压缩， 只保留可以恢复数据的最小指令集.可以使用命令bgrewriteaof



##### **重写原理，如何实现重写**

AOF文件持续增长而过大时，会fork出一条新进程来将文件重写(也是先写临时文件最后再rename)，redis4.0版本后的重写，是指上就是把rdb 的快照，以二级制的形式附在新的aof头部，作为已有的历史数据，替换掉原来的流水账操作。

no-appendfsync-on-rewrite：

如果 no-appendfsync-on-rewrite=yes ,不写入aof文件只写入缓存，用户请求不会阻塞，但是在这段时间如果宕机会丢失这段时间的缓存数据。（降低数据安全性，提高性能）

   如果 no-appendfsync-on-rewrite=no, 还是会把数据往磁盘里刷，但是遇到重写操作，可能会发生阻塞。（数据安全，但是性能降低）

触发机制，何时重写

Redis会记录上次重写时的AOF大小，默认配置是当AOF文件大小是上次rewrite后大小的一倍且文件大于64M时触发

重写虽然可以节约大量磁盘空间，减少恢复时间。但是每次重写还是有一定的负担的，因此设定Redis要满足一定条件才会进行重写。 

auto-aof-rewrite-percentage：设置重写的基准值，文件达到100%时开始重写（文件是原来重写后文件的2倍时触发）

auto-aof-rewrite-min-size：设置重写的基准值，最小文件64MB。达到这个值开始重写。

例如：文件达到70MB开始重写，降到50MB，下次什么时候开始重写？100MB

系统载入时或者上次重写完毕时，Redis会记录此时AOF大小，设为base_size,

如果Redis的AOF当前大小>= base_size +base_size*100% (默认)且当前大小>=64mb(默认)的情况下，Redis会对AOF进行重写。 



##### **重写流程**

1. bgrewriteaof触发重写，判断是否当前有bgsave或bgrewriteaof在运行，如果有，则等待该命令结束后再继续执行。
2. 主进程fork出子进程执行重写操作，保证主进程不会阻塞。
3. 子进程遍历redis内存中数据到临时文件，客户端的写请求同时写入aof_buf缓冲区和aof_rewrite_buf重写缓冲区保证原AOF文件完整以及新AOF文件生成期间的新的数据修改动作不会丢失。
4. 子进程写完新的AOF文件后，向主进程发信号，父进程更新统计信息。2).主进程把aof_rewrite_buf中的数据写入到新的AOF文件。
5. 使用新的AOF文件覆盖旧的AOF文件，完成AOF重写。

![image-20211221170400211](https://eimago.oss-cn-beijing.aliyuncs.com/typora-img/image-20211221170400211.png)



#### **优势**

- 备份机制更稳健，丢失数据概率更低。
- 可读的日志文本，通过操作AOF稳健，可以处理误操作。



#### **劣势**

- 比起RDB占用更多的磁盘空间。
- 恢复备份速度要慢。
- 每次读写都同步的话，有一定的性能压力。
- 存在个别Bug，造成恢复不能。



