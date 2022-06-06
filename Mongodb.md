# Mongodb

## mongodb基本操作

### 查看数据库

> `show databases`

### 选择数据库

> `use database`

隐式创建，在mongodb中选择不存在的数据库不会报错，后期当该数据库有数据时会自动创建

### 查看集合

> `show collections`

### 创建集合

> `db.createCollection('c1')`

### 删除集合

> `db.c1.drop()`

### 删除数据库

> 通过use语法选择数据库后`dropDatabase()`



## Mongodb插入数据

> `db.集合名.insert(json数据)`
>
> 集合存在则直接插入数据，集合不存在隐式创建

#### 练习：

在test2数据库的c1集合中插入数据（姓名叫eson，年龄18岁）

```
use test2
db.c1.insert({"username":"eson",age:"18"})
```

mongdb会给每条数据增加一个唯一的_id健

可以自定义_id健

`db.c1.insert({_id:1,username:"eson",age:"18"})`

### 插入多条数据

> 传递数组，数组中写一个个json数据

```
db.c1.insert([{username:"u1",age:1},
	{username:"u2",age:2},
	{username:"u3",age:3}
])
```

### 快速插入多条数据

> mongodb底层是用js引擎实现的，所以支持部分js语法

#### 需求：在test2数据库的c2集合中插入10条数据，分别为a1,a2,a3...

```
for(let i=1;i<=10;i++){
	db.c2.insert({username:"a"+i,age:i})
}
```



## Mongodb查询数据

> 基础语法：`db.集合名.find(条件[,查询的列])`

