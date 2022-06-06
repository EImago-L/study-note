# jQuery

**jQuery内部封装了原生的js代码（还额外添加了很多的功能）
能够让你通过更少的代码完成js操作 
类似于python的模块  在前端模块不叫模块	叫“类库”**
**兼容多个浏览器** 

下载连接:[jQuery官网](https://jquery.com/)

中文文档:[jQuery AP中文文档](http://jquery.cuishifeng.cn/)

**jQuery基本语法**:

jQuery(选择器).action

jQuery() === $()

**jQuery与js代码对比:**

```js
//js:
let pEle = doument.getElementById('d1')
pEle.style.color = 'red'

//jQuery:
$('p').class('color','blue')
```



## 基本选择器

### id选择器

```js
$('#d1')
//w.fn.init [div#d1]0: div#d1length: 1__proto__: Object(0)
```

### class选择器

```js
$('.c1')
//w.fn.init [p.c1, prevObject: w.fn.init(1)]0: p.c1length: 1prevObject: w.fn.init [document]__proto__: Object(0)
```

### 标签选择器

```js
$('span')
//w.fn.init(3) [span, span, span, prevObject: w.fn.init(1)]
```

### 属性选择器

```js
$('[name]')

$('[name=username]')

$('input[name=username]')

```

### jQuery对象转为标签对象

```js
$('#d1')[0]
//<div id=​"d1">​…​</div>​
```

### 标签对象转为jQuery对象

```js
$(document.getElementById('d1'))
//w.fn.init [div#d1]
```



## 组合选择器/分组与嵌套

```js
$('div')
//w.fn.init(2) [div#d1, div.c1, prevObject: w.fn.init(1)]

$('div.c1')
//w.fn.init [div.c1, prevObject: w.fn.init(1)]0: div.c1length: 1prevObject: w.fn.init [document]__proto__: Object(0)

$('div#d1')
//w.fn.init [div#d1, prevObject: w.fn.init(1)]

$('*')
//w.fn.init(19) [html, head, meta, title, meta, link, script, script, body, span, span, div#d1, span, p#d2, span, span, div.c1, span, span, prevObject: w.fn.init(1)]
               
$('#d1,.c1,p')  // 并列+混用
//w.fn.init(3) [div#d1, p#d2, div.c1, prevObject: w.fn.init(1)]
              
$('div span')  // 后代
//w.fn.init(3) [span, span, span, prevObject: w.fn.init(1)]

$('div>span')  // 儿子
//w.fn.init(2) [span, span, prevObject: w.fn.init(1)]

$('div+span')  // 毗邻
//w.fn.init [span, prevObject: w.fn.init(1)]

$('div~span')  // 弟弟
//w.fn.init(2) [span, span, prevObject: w.fn.init(1)]
```



## 基本筛选器

```js
$('ul li')

$('ul li:first') //大儿子

$('ul li:last') //小儿子

$('ul li:eq(2)') //放索引

$('ul li:even') //偶数索引 0包含在内

$('ul li:odd')  //奇数索引

$('ul li:gt(2)') //大于2的索引

$('ul li:lt(2)') //小于2的索引

$('ul li:not("#d1")') //移除满足条件的标签

$('div:has("p")') //选择出包含一个或多个标签在内的标签
```



## 表单筛选器

```js
$('input[type="text"]')
//等价于
$(":text")

$('input[type="password"]')
//等价于
$(':password')


```

**对于$('input[type="text"]')这种写法过于麻烦，我们用$(":text")替代**

**以“:”起手，后面接属性的值，但这只在form表单中有效**

```js
:text
:password
:file
:radio
:checkbox
:submit
:reset
:button
...

表单对象属性
:enabled
:disabled
:checked
:selected
```

**特殊情况：**

```js
$(':checked')  // 它会将checked和selected都拿到
w.fn.init(2) [input, option, prevObject: w.fn.init(1)]0: input1: optionlength: 2prevObject: w.fn.init [document]__proto__: Object(0)

$(':selected')  // 它不会 只拿selected
w.fn.init [option, prevObject: w.fn.init(1)]

$('input:checked')  // 自己加一个限制条件
w.fn.init [input, prevObject: w.fn.init(1)]
```



## 筛选器方法

```js
$('#d1').next()  // 同级别下一个

$('#d1').nextAll()	//同级别的下面全部标签

$('#d1').nextUntil('.c1')  // 同级别的下面标签不包括有c1类的
              
              
$('.c1').prev()  // 上一个

$('.c1').prevAll()

$('.c1').prevUntil('#d2')

              
$('#d3').parent()  // 第一级父标签

$('#d3').parent().parent()	//第二级父标签

$('#d3').parent().parent().parent()

$('#d3').parent().parent().parent().parent()


$('#d3').parents()	//所有父标签

$('#d3').parentsUntil('body') 	//所有父标签直到body
              
              
$('#d2').children()  // 儿子
              
$('#d2').siblings()  // 同级别上下所有
              
              
              
$('div p')
# 等价           
$('div').find('p')  // find从某个区域内筛选出想要的标签 
              
              
"""下述两两等价"""
$('div span:first')
$('div span').first()
                                                                             
$('div span:last')
$('div span').last()
                                                                                    
$('div span:not("#d3")')
$('div span').not('#d3')

```



## 操作标签

### 操作类

- addClass()	添加类

- removeClass()	移除类

- hasClass()	判断是否拥有类

- toggleClass()	无则添加有则删除

### css操作

```js
//一行代码将第一个p标签变成红色第二个p标签变成绿色"""
$('p').first().css('color','red').next().css('color','green')
// jQuery的链式操作 使用jQuery可以做到一行代码操作很多标签
// jQuery对象调用jQuery方法之后返回的还是当前jQuery对象 也就可以继续调用其他方法
```

### 位置操作

- offset()	相对于浏览器窗口的位置

- position()	相对于父标签的位置

- scrollTop()	滚动条到顶部的距离

  ```js
  $(window).scrollTop()
  $(window).scrollTop(500)	//加了参数就是设置	
  ```

- scrollLeft()     滚动条到左边的距离

### 尺寸

- $('p').height()    文本
- $('p').width()
- $('p').innerHeight()    文本+padding
- $('p').innerWidth()
- $('p').outerHeight()    文本+padding+border
- $('p').outerWidth()

### 文本操作

**括号内不加参数就是获取加了就是设置**

- 操作标签内部文本

  ```js
  $('div').text()
  $('div').text('你们都是我的大宝贝')
  ```

- 操作标签

  ```js
  $('div').html()
  $('div').text('<h1>你们都是我的大宝贝</h1>')
  ```

### 获取值操作

**括号内不加参数就是获取加了就是设置**

```js
$('#d1').val()
$('#d1').val('520快乐')

$('#d2').val()
//"C:\fakepath\01_测试路由.png"

$('#d2')[0].files[0]  # 牢记两个对象之间的转换
//File {name: "01_测试路由.png", lastModified: //1557043083000, lastModifiedDate: Sun May 05 2019 //15:58:03 GMT+0800 (中国标准时间), //webkitRelativePath: "", size: 28733, …}
```

### 属性操作

- 获取属性

  ```js
  $pEle.attr('id')
  //"d1"
  ```

- 设置属性

  ```js
  $pEle.attr('class','c1')
  $pEle.attr('id','id666'
  ```

- 移除属性

  ```js
  $pEle.removeAttr('password')
  ```

**特别注意：**

对于标签上有的能够看到的属性和自定义属性用attr
对于返回布尔值比如checkbox radio option是否被选中用prop

```js
$('#d2').prop('checked')
//false
$('#d2').prop('checked')
//true
$('#d3').prop('checked',true)
//w.fn.init [input#d3]
$('#d3').prop('checked',false)
//w.fn.init [input#d3]
```

## 文档处理

### 创建标签

```js
let $pEle = $('<p>')
```

### 插入标签

- 内部尾部追加

  ```js
  let $pEle = $('<p>')
  $pEle.attr('id','d2')
  $('#d1').append($pEle)
  
  $pEle.appendTo($('#d1'))
  ```

- 放在某个标签后面

  ```js
  $('#d2').after($pEle)
  
  $pEle.insertAfter($('#d2'))
  ```

- 放在某个标签前面

  ```js
  $('#d2').before($pEle)
  
  $pEle.insertBefore($('#d2'))
  ```

### 删除标签

```js
$('#d1').remove()  // 将标签从DOM树中删除

$('#d1').empty()  // 清空标签内部所有的内容
```

## 事件

### 克隆事件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <style>
        #d1 {
            background-color: darkgray;
            border: 1px solid red;
            width:100px;
            height: 100px;
        }
    </style>
</head>
<body>
<button id="d1">
    屠龙宝刀，点击就送
</button>
<script>
    $("#d1").on('click',function () {
        $(this).clone().insertAfter($('body'))
    })
</script>
</body>
</html>
```

### 自定义模态框

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <style>
        body {
            margin: 0;
        }

        .cover {
            background-color: rgba(128,128,128,0.4);
            z-index: 99;
            position: fixed;
            left: 0;
            right: 0;
            top: 0;
            bottom: 0;

        }
        .model {
            background-color: red;
            width: 200px;
            height: 200px;
            z-index: 100;
            position: fixed;
            top: 50%;
            left: 50%;
            margin-left: -100px;
            margin-top: -100px;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div>
        这是底层内容
        <button id="d1">出来</button>
        <div class="cover hidden">
            <div class="model hidden">
            <form action="">
                username<input type="text">
                password<input type="password">
                <button id="d2">消失</button>
            </form>
                </div>
        </div>
    </div>

    <script>
        $('#d1').on(
            'click',function () {
                $('.cover').toggleClass('hidden')
                $('.model').toggleClass('hidden')
            }
        )
    </script>
</body>
</html>
```

### 左侧菜单

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <style>
        body {
            margin:0 ;
        }

        #navigate {
            position: fixed;
            float: left;
            background-color: #9d9d9d;
            width: 20%;
            height: 100%;
        }
        #navigate div {
            text-align: center;
        }
        .item p{
            border: 1px solid darkcyan;
        }
        .hidden {
            display: none;
        }
        h2:hover {
            color: #eeeeee;
        }
    </style>
</head>
<body>
<div id="navigate">
    <div><h2>title</h2><div class="item"><p>111</p><p>222</p><p>333</p></div></div>
    <div><h2>title</h2><div class="item hidden"><p>111</p><p>222</p><p>333</p></div></div>
    <div><h2>title</h2><div class="item hidden"><p>111</p><p>222</p><p>333</p></div></div>
</div>
<script>
    $('h2').on('click',function () {
        $('.item').addClass('hidden')
        $(this).siblings().removeClass('hidden')
    })
</script>
</body>
</html>
```

### 返回顶部

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <style>

        div {
            width: 100%;
            height: 300px;

        }
        #ret {

            position: fixed;
            right: 10px;
            bottom: 30px;
            width: 70px;
            height: 20px;
            background-color: red;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>

<div style="background-color: greenyellow" id="d1"></div>
<div style="background-color: #9d9d9d"></div>
<div style="background-color: darkcyan"></div>
<div style="background-color: yellow"></div>
<div style="background-color: orange"></div>
<div id="ret"><a href="#d1" class="clearfix">回到顶部</a></div>
</body>
<script>
    $(window).scroll(function () {
        if ($(this).scrollTop() > 200){
            $('#ret').removeClass('hidden')
        }else {
            $('#ret').addClass('hidden')
        }
    })
</script>
</html>
```

### 自定义登录验证

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
<div>

        <div>
        username:<input type="text" name="username"><span></span>
            </div>
        <div>
        password:<input type="password" name="password"><span></span>
            </div>
         <button id="d1">提交</button>

</div>
<script>
    let $userName = $('[name=username]')
    let $passWord = $('[name=password]')
    $('#d1').on('click',function () {
        let userName = $userName.val()
        let passWord = $passWord.val()
        if (!userName){
            $('[name=username]+span').text('用户名不能为空')
        }
        if (!passWord){
            $('[name=password]+span').text('密码不能为空')
        }
        $('input').focus(function () {
            $(this).next().text('')
        })
    })
</script>
</body>
</html>
```

### input输入事件

```html
<script>
$('[name=username]').on('input',function () {
        console.log(this.value)
    })
</script>
```

### hover事件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
<input type="text" id="d1">
<script>
    $('#d1').hover(function () { //悬浮
        alert('123')
    },function () {  //离开
        alert('321')
        }

    )
</script>
</body>
</html>
```

### 键盘按下事件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
<script>
    $(window).keydown(function (event) {
        console.log(event.keyCode)
        if (event.keyCode === 16){
            alert('shift')
        }
    })
</script>
</body>
</html>
```

阻止后续事件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
<form action="">
    <span></span>
    <input type="submit" id="d1">
</form>
<script>
    $('#d1').on(
        'click',function () {
            $(this).prev().text('hello its me')
            return false
        }
    )
</script>
</body>
</html>
```

### 阻止事件冒泡

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
<div>div
    <p>div>p
        <span>div>p>span</span>
    </p>
</div>
<script>
    $('div').on('click',function () {
        alert('div')
    })
    $('p').on('click',function () {
        alert('p')
    })
    $('span').on('click',function () {
        alert('span')
        return false
    })
</script>
</body>
</html>
```

### 事件委托

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
<button>i have a pen</button>
</body>
<script>
    // $('button').on('click',function () {
    //     alert($(this).text())    // 无法影响到动态创建的标签
    // })

    $('body').on('click','button',function () {
        alert($(this).text())
    })
    // 在指定的范围内 将事件委托给某个标签 无论该标签是事先写好的还是后面动态创建的

    let $btnEle = $('<button>')
    $btnEle.text('i have apple')
    $('body').append($btnEle)
</script>
</html>
```

### 实时获取用户头像

```html
<script>
    $('#myfile').change(function () {
        // 文件阅读器
        // 1 先生成一个文件阅读器对象
        let myFileReaderObj = new FileReader();
        // 2 获取用户上传的头像文件
        let fileObj = $(this)[0].files[0];
        // 3 将文件对象交给阅读器对象读取
        myFileReaderObj.readAsDataURL(fileObj); // 异步操作 io操作
        // 4 等待文件阅读器将文件展示到前端页面 修改src属性
        // 等待文件阅读器加载完毕后再执行
        myFileReaderObj.onload = function () {
            $('#myimg').attr('src',myFileReaderObj.result)
        }
    })

</script>
```





## 页面加载

**等待页面加载完毕再执行代码**

```js
window.onload = function(){
  // js代码
}


//jQuery中等待页面加载完毕
// 第一种
$(document).ready(function(){
  // js代码
})
// 第二种
$(function(){
  // js代码
})
// 第三种: 写在body内部最下方
```

## 动画效果

```js
$('#d1').hide(5000)
w.fn.init [div#d1]
$('#d1').show(5000)
w.fn.init [div#d1]
$('#d1').slideUp(5000)
w.fn.init [div#d1]
$('#d1').slideDown(5000)
w.fn.init [div#d1]
$('#d1').fadeOut(5000)
w.fn.init [div#d1]
$('#d1').fadeIn(5000)
w.fn.init [div#d1]
$('#d1').fadeTo(5000,0.4)
w.fn.init [div#d1]      
```

- 逐渐隐藏

  ```js
  $('div').hide(300) //参数为动画时间
  ```

- 逐渐展示

  ```js
  $('div').show(300)
  ```

- 向上隐藏

  ```js
  $('div').slideUp(3000)
  ```

- 向下展示

  ```js
  $('div').slideDown(3000)
  ```

- 淡入淡出的隐藏

  ```js
  $('div').fadeOut(3000)
  ```

- 淡入淡出的展示

  ```js
  $('div').fadeIn(3000)
  ```

- 淡入淡出的隐藏或出现到一定程度

  ```js
  $('div').fadeTo(3000,0.4)
  ```

## 补充

-  each()

  ```js
  	
  // 第一种方式
  $('div')
  w.fn.init(10) [div, div, div, div, div, div, div, div, div, div, prevObject: w.fn.init(1)]
  $('div').each(function(index){console.log(index)})
  VM181:1 0
  VM181:1 1
  VM181:1 2
  VM181:1 3
  VM181:1 4
  VM181:1 5
  VM181:1 6
  VM181:1 7
  VM181:1 8
  VM181:1 9
  
  $('div').each(function(index,obj){console.log(index,obj)})
  VM243:1 0 <div>​1​</div>​
  VM243:1 1 <div>​2​</div>​
  VM243:1 2 <div>​3​</div>​
  VM243:1 3 <div>​4​</div>​
  VM243:1 4 <div>​5​</div>​
  VM243:1 5 <div>​6​</div>​
  VM243:1 6 <div>​7​</div>​
  VM243:1 7 <div>​8​</div>​
  VM243:1 8 <div>​9​</div>​
  VM243:1 9 <div>​10​</div>​
  
  // 第二种方式
  $.each([111,222,333],function(index,obj){console.log(index,obj)})
  VM484:1 0 111
  VM484:1 1 222
  VM484:1 2 333
  (3) [111, 222, 333]
  ```

  **有了each之后 就无需自己写for循环了 用它更加的方便**

- data

  **能够让标签帮我们存储数据 并且用户肉眼看不见**

  ```js
  
  $('div').data('info','回来吧，我原谅你了!')
  w.fn.init(10) [div#d1, div, div, div, div, div, div, div, div, div, prevObject: w.fn.init(1)]
                 
  $('div').first().data('info')
  "回来吧，我原谅你了!"
  $('div').last().data('info')
  "回来吧，我原谅你了!"
                 
  $('div').first().data('xxx')
  undefined
  $('div').first().removeData('info')
  w.fn.init [div#d1, prevObject: w.fn.init(10)]
             
  $('div').first().data('info')
  undefined
  $('div').last().data('info')
  "回来吧，我原谅你了!"
  ```

  

​	



