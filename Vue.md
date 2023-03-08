# **Vue**

## **Vue核心**

### 初识**Vue**

1. 想要Vue工作，就必须创建一个Vue实例，且要传入一个配置对象
2. root容器里面的代码依然符合html规范，只不过混入了一些特殊语法
3. root容器里面的代码被称为Vue模板
4. Vue实例和容器一一对应
5. 真实开发中只有一个Vue实例，配合着组件一起使用。
6. {{XXX}}中的XXX写js表达式，并且XXX可以读取到data中的所有属性
7. 一旦data中的数据发生改变，页面中用到该数据的地方也会自动更新

```html

<!--准备好一个容器-->
<div id="root">
    <h1>Hi,I'm {{name}}</h1>
</div>
<script type="text/javascript">
    Vue.config.productionTip = false    //阻止Vue启动时生成生产提示。
    
    // 创建vue实例
    new Vue({
        el:'#root', //el用于指定当前vue实例为哪个容器服务，值通常为css选择器字符串
        data:{  //data中用于1存储当前数据，数据供el所指定的容器去使用，致我们暂时写成一个对象。
            name:'JayeLiao'
        }
    })
</script>
```



### Vue**模板语法**

Vue模板语法分为插值语法和指令语法



#### **插值语法**

作用：用于解析标签体内容

写法：{{XXX}}，xxx是js表达式，且可以直接读取到data中的所有属性



#### **指令语法**

作用：用于解析标签（包括但不限于 标签属性、标签体内容、绑定事件）

举例：v-bind:href=“XXX” 或简写为:href=“XXX”，XXX同样要写js表达式，且可以读取到data中的所有属性。

> Vue中有很多指令，形式都是v-XXX,这里拿v-bind举例

```html
<body>
<div id="root">
    <h1>插值语法</h1>
    <h3>{{name}}</h3>
    <hr>
    <h1>指令语法</h1>
    <a v-bind:href="school.url">点我去{{school.name}}</a>
    <a :href="school.url.toUpperCase()">我的链接变大写了</a>
</div>
<script>
    Vue.config.productionTip = false;

    new Vue({
        el:'#root',
        data: {
            name: 'jaye',
            school: {
                name:'cqust',
                url:'https://www.cqust.edu.cn/'
            }
        }
    })
</script>
</body>
```



### **数据绑定**

Vue中有两种数据绑定方式

- 单向绑定（v-bind）：数据只能从data流向页面。
- 双向绑定（v-model）：数据不仅能从data流向页面，还可以从页面流向data。
  - 双向绑定一般都应用在表单类元素上
  - v-model：value 可以简写为v-model，因为v-model默认收集的是value值。

```html
<body>
<div id="root">
    <!--单向数据绑定-->
    <input type="text" v-bind:value="name">
    <!--双向数据绑定-->
    <input type="text" v-model:value="name">

    <!--简写-->
    <input type="text" :value="name">
    <input type="text" v-model="name">

    <!--下面的代码是错误的 v-mode只能应用在表单类元素上-->
    <h2 v-model:x="name">hello</h2>
</div>
<script>
    new Vue({
        el:'#root',
        data:{
            name:'jayeLiao'
        }
    })
</script>
</body>
```



### **el于data的两种写法**

- el有2种写法

  - new Vue时候配置el属性
  - 先创建Vue实例， 随后通过vm.$mount('#root')指定el的值。

- data的两种写法

  - 对象式

  - 函数式

    > 学习组件时，data必须使用
    >
    > 函数式，否则会报错。

> 由Vue管理的函数，一定不要使用箭头函数，一旦写了箭头函数，this就不再是Vue实例了。



### **MVVM模型**

M：模型（Model）：data中的数据

V：视图（View）：模板代码

VM：视图模型（ViewModel）：Vue实例



- data种所有的属性，最后都出现在vm身上

- vm身上所有的属性 及Vue原型上的所有属性，在Vue模板种都可以直接使用

![image-20230225233414894](Vue.assets/image-20230225233414894.png)

```html
<body>
<div id="root">
    <h1>{{name}}</h1>
    <h2>{{age}}</h2>
    <h2>{{$el}}</h2>
    <h2>{{_c}}</h2>
    <h2>{{$mount}}</h2>
</div>
<script>
    const vm = new Vue({
        el:'#root',
        data:{
            name:'JayeLiao',
            age:21
        }
    })
    console.log(vm)
</script>
</body>
```



### **数据代理**

#### **回顾Object.defineProperty方法**

```javascript
let person = {
        name: 'jayeLiao',
        sex:'male'
    }
    Object.defineProperty(person, 'age', {
        //value:21,           //属性的值
        //enumerable: true,   //属性是否可以被枚举
        //writable: true,     //属性是否可以修改值
        //configurable: true,  //属性是否可以被删除

        //当有人读取person的age属性时， get函数（getter）就会被调用， 且返回值就是age的值
        get() {
            console.log('有人读取了age属性')
            return 21s;
        },

        //当有人修改person的age属性时，set函数（setter）就会被调用，且会收到修改的具体值
        set(v) {
            console.log('有人修改了age属性的值，值是', v)
        }
    })
```



### **事件处理**

1. 使用`v-on:XXX` 或 `@XXX` 绑定事件，其中XXX是事件名
2. 事件的回调需要配置在methods对象中，最终会在vm上
3. methods中配置的函数，不要用箭头函数，否者this就不是vm了
4. methods中配置的函数，都是被Vue所管理的函数，this的指向是vm 或 组件实例对象
5. `@click="demo"` 和 `@click=“demo($event)”`效果一致，但后者可以传参

```html
<body>
<div id="root">
    <h1>hello,{{name}}</h1>
    <button v-on:click="showInfo1">点我提示信息1（不传参）</button>
    //简写
    <button @click="showInfo2($event, 66)">点我提示信息2（传参）</button>
</div>
<script>
    const vm = new Vue({
        el:'#root',
        data:{
            name:'JayeLiao'
        },
        methods:{
            showInfo1(){
                console.log('hello hello')
            },
            showInfo2(t, num){
                console.log(t)
                console.log(num)
            }
        }
    })
</script>
</body>
```



### **事件修饰符**

1. prevent：阻止默认事件
2. stop：阻止事件冒泡
3. once：事件只触发一次
4. capture：使用事件的捕获模式
5. self：只有event.target是当前操作的元素时才触发事件
6. passive：事件的默认行为立即执行，无需等待事件回调执行完毕

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../js/vue.js"></script>
    <style>
        *{
            margin-top: 20px;
        }
        .demo1{
            height: 50px;
            background-color: skyblue;
        }
        .box1{
            padding: 5px;
            background-color: skyblue;
        }
        .box2{
            padding: 5px;
            background-color: orange;
        }
    </style>
</head>
<body>
    <div id="root">
        <h2>hellow {{name}}</h2>

<!--         阻止默认行为-->
        <a href="https://www.strongforu.top" @click.prevent="showInfo">点我去另一个地方</a>

<!--        阻止事件冒泡-->
        <div class="demo1" @click="showInfo">
            <button @click.stop="showInfo">点我提示信息</button>
        </div>

<!--        事件只触发一次-->
        <button @click.once="showInfo">click me</button>

<!--        使用事件捕获模式-->
        <div class="box1" @click.capture="showMsg(1)">
            div1
            <div class="box2" @click="showMsg(2)">
                div2
            </div>
        </div>

<!--        只有event.traget是当前操作的元素时才会触发事件-->
        <div class="demo1" @click.self="showInfo2">
            <button @click="showInfo2">点我提示信息</button>
        </div>
    </div>
    <script>
        const vm = new Vue({
            el:'#root',
            data:{
                name:'JayeLiao'
            },
            methods:{
                showInfo(){
                    alert('hello hello')
                },
                showMsg(msg){
                    console.log(msg)
                },
                showInfo2(event){
                    console.log(event.target)
                }
            }
        })
    </script>
</body>
</html>
```



### **键盘事件**

1. Vue中常用的按键别名：
   - 回车    enter
   - 删除     delete（捕获删除和退格键）
   - 退出    esc
   - 空格    space
   - 换行    tab（特殊，必须配合keydown去使用）
   - 上    up
   - 下    down
   - 左    left
   - 右    right
2. Vue未提供别名的按键，可以使用按键原始的key值取绑定，的那要注意转为kebab-case（短横线命名）
3. 系统修饰键（用法特殊）：ctrl、alt、shift、meta（可以理解为win键）
   1. 配合keyup使用：按下修饰键的同时，再按下其他键，随后释放其他键，事件才被触发
   2. 配合keydown使用：正常触发事件。
4. 也可以使用keyCode去指定具体的按键（不推荐）
5. Vue.config.keyCodes.自定义键名 = 键码，可以去定制按键别名

```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../js/vue.js"></script>
    <style>
        input{
            display: block;
        }
    </style>
</head>
<body>
<div id="root">
    <h1>hello, {{name}}</h1>
    <input type="text" placeholder="按下键盘查看提示" @keyup="showInfo">
    enter：<input type="text" placeholder="按下回车提示输入" @keyup.enter="showInfo">
    delete：<input type="text" placeholder="按下删除或退格键" @keyup.delete="showInfo">
    esc：<input type="text" placeholder="按下esc" @keyup.esc="showInfo">
    tab：<input type="text" placeholder="按下tab" @keydown.tab="showInfo">
    ↑：<input type="text" placeholder="按下↑" @keydown.up="showInfo">
    ↓：<input type="text" placeholder="按下↓" @keydown.down="showInfo">
    ←：<input type="text" placeholder="按下←" @keydown.left="showInfo">
    →：<input type="text" placeholder="按下→" @keydown.right="showInfo">
    CapsLock：<input type="text" placeholder="按下大写锁定键" @keydown.caps-lock="showInfo">
    ctrl+任意键：<input type="text" placeholder="按下ctrl+任意键" @keyup.ctrl="showInfo">
    alt+任意键：<input type="text" placeholder="按下alt+任意键" @keyup.alt="showInfo">
    shift+任意键：<input type="text" placeholder="按下shift+任意键" @keyup.shift="showInfo">
    win+任意键：<input type="text" placeholder="按下win+任意键" @keyup.meta="showInfo">
</div>
<script>
    const vm = new Vue({
        el:'#root',
        data:{
            name:'JayeLiao'
        },
        methods:{
            showInfo(event){
                console.log(event.key, event.keyCode)
            }
        }
    })
</script>
</body>
</html>
```



### **姓名案例**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../js/vue.js"></script>
</head>
<body>
<div id="root">
    first name: <input type="text" v-model="firstName"><br>
    last name: <input type="text" v-model="lastName"><br>
    full name: <span>{{getFullName()}}</span>
</div>
<script>
    const vm = new Vue({
        el:'#root',
        data:{
            firstName:'Jaye',
            lastName:'Liao'
        },
        methods:{
            getFullName(){
                return this.firstName + '-' + this.lastName
            }
        }
    })
</script>
</body>
</html>
```

当data中的数据发生改变时，Vue都会重新解析，`getFullName（）`也会被重新执行



### **计算属性**

要用的属性不存在，要通过已有的属性（data中的那些变量）计算得来

- 底层接住了`Object.defineproperty`方法提供的getter和setter
- get函数什么时候执行？
  - 初次读取时会执行一次
  - 当以来的属性发生改变时会被再次调用
- 优势：内部有缓存机制，效率更高，调试方便

> 计算属性最终会出现在vm上，直接读取使用即可
>
> 如果计算属性要被修改，那必须写set函数去响应修改，且set函数中要引起计算时依赖的数据发生改变

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../js/vue.js"></script>
</head>
<body>
<div id="root">
    first name: <input type="text" v-model="firstName"><br>
    last name: <input type="text" v-model="lastName"><br>
    full name: <span>{{fullName}}</span>
</div>
<script>
    const vm = new Vue({
        el:'#root',
        data:{
            firstName:'Jaye',
            lastName:'Liao'
        },
        computed:{
          fullName:{
            get(){
              return this.firstName + '-' + this.lastName
            },
            set(value){
              this.firstName, this.lastName = value.split('-')
            }
          }
        }
    })
</script>
</body>
</html>
```



#### **简写形式**

如过计算属性只读，则可以简写为：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../js/vue.js"></script>
</head>
<body>
<div id="root">
    first name: <input type="text" v-model="firstName"><br>
    last name: <input type="text" v-model="lastName"><br>
    full name: <span>{{fullName}}</span>
</div>
<script>
    const vm = new Vue({
        el:'#root',
        data:{
            firstName:'Jaye',
            lastName:'Liao'
        },
        computed:{
            fullName(){
                return this.firstName + '-' + this.lastName
            }
        }
    })
</script>
</body>
</html>
```

简写为一个函数，这个函数相当于`get()`



### **监视属性**

监视属性watch

1. 当被监视的属性发生变化时，回调函数自动调用，进行相关操作
2. 监视属性必须存在才能进行监视
3. 监视属性的两种写法
   1. new Vue时传入watch配置
   2. 通过vm.$watch监视

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../js/vue.js"></script>
</head>
<body>
<div id="root">
    <h2>今天天气很{{info}}</h2>
    <button @click="isHot = !isHot">点击切换天气</button>
</div>
<script>
    const vm = new Vue({
        el:'#root',
        data:{
            isHot:true
        },
        computed:{
            info(){
                return this.isHot ? '炎热':'凉爽'
            }
        },
        /** 这是一种写法
        watch:{
          isHot:{
              immediate:true,   // 初始化时handler调用
              handler(newValue, oldValue){
                  console.log('isHot被修改了', newValue, oldValue)
              }
          }
        }
         **/
    })

    // 另一种写法
    vm.$watch('isHot', {
        immediate:true,   // 初始化时handler调用
        handler(newValue, oldValue){
          console.log('isHot被修改了', newValue, oldValue)
      }
    })
</script>
</body>
</html>
```

#### **简写**

当watch中不设置额外选项时（如immediate、deep）可简写为

```js
const vm = new Vue({
        el:'#root',
        data:{
            isHot:true,
            numbers:{
                a:1,
                b:100
            }
        },
        computed:{
            info(){
                return this.isHot ? '炎热':'凉爽'
            }
        },
        watch:{
            isHot(new, oldValue){
                ...
            },
            numbers: {
                deep:true,
                handler(){
                    console.log("numbers 变了！！！")
                }
            }
        }

    })
    
    或则
    vm.$watch('isHot', function(newVlaue, oldValue){
    ....
	})
```





#### **深度监视**

- Vue中的watch默认不监测对象内部值得改变（一层）
- 配置deep:true可以监测对象内部值的改变（多层）

> Vue自身可以监测对象内部值的改变，但Vue提供的watch默认不可以
>
> 使用watch时根据数据的具体结构，决定是否采用深度监视

```js
const vm = new Vue({
        el:'#root',
        data:{
            isHot:true,
            numbers:{
                a:1,
                b:100
            }
        },
        computed:{
            info(){
                return this.isHot ? '炎热':'凉爽'
            }
        },
        watch:{
            isHot:{
              immediate:true,   // 初始化时handler调用
              handler(newValue, oldValue){
                  console.log('isHot被修改了', newValue, oldValue)
              }
          },
            numbers: {
                deep:true,
                handler(){
                    console.log("numbers 变了！！！")
                }
            }
        }

    })
```



### **绑定样式**

1. class样式
   - 写法：class="XXX" XXX可以是字符串、对象、数组
   - 字符串写法适用于：类名不确定，要动态的获取
   - 对象写法适用于：要绑定多个样式，个数不确定，名字也不确定
   - 数组写法适用于：要绑定多个样式，个数确定，名字也确定，动态的确定样式要不要用
2. sytle样式
   - :style="{fontSize:XXX}" 其中XXX是动态值
   - :style="[a,b]" 其中a、b是样式对象

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../js/vue.js"></script>
    <style>
        .basic{
            border: 1px black solid;
            height: 200px;
        }

        .normal{
            background-color: skyblue;
        }
        .happy{
            background-color: lightseagreen;
            border-color: yellow;
        }
        .angry{
            background-color: red;
        }

        .style1{
            font-size: 50px;
        }
        .style2{
            border-radius: 10px;
        }
        .style3{
            background: linear-gradient(blue, pink);
        }

    </style>
</head>
<body>
<div id="root">
<!--    绑定class样式--字符串写法:适用于样式的类名不确定，需要动态指定-->
    <div class="basic" :class="mood" @click="changeMood"> {{name}} </div>
    <br>

<!--    绑定class样式--数组写法：适用于要绑定的样式个数不确定、名字也不确定-->
    <div class="basic" :class="classArr" >{{name}}</div>
    <br>
<!--    绑定class样式--对象写法：适用于要绑定的样式个数确定、名字确定，但要动态的决定要不要用-->
    <div class="basic" :class="classObj">{{name}}</div>
    <br>

<!--    绑定style样式--对象写法-->
    <div class="basic" :style="styleObj">{{name}}</div>
    <br>
<!--    绑定style样式--数组写法-->
    <div class="basic" :style="styleArr">{{name}}</div>
    <br>
</div>

<script>
    const vm = new Vue({
        el:'#root',
        data:{
            name:'JayeLiao',
            mood:'normal',
            classArr:['style1', 'style2', 'style3'],
            classObj:{
                style1:false,
                style2:false,
            },
            styleObj:{
                fontSize:'60px',
                color:'red'
            },
            styleArr:[
                {
                    fontSize:'60px',
                    color:'blue'
                },
                {
                    backgroundColor:'gray'
                }
            ]
        },
        methods:{
            changeMood(){
                const arr = ['normal', 'happy', 'angry']
                const index = Math.floor(Math.random() * 3)
                this.mood = arr[index]
            }
        }
    })
</script>
</body>
</html>
```



### **条件渲染**

- v-if
  - 写法：
    - v-if="表达式"
    - v-else-if="表达式"
    - v-else="表达式"
  - 适用于切换频率比较低的场景
  - 不展示的DOM元素直接被移除
  - v-if可以和v-else-if、v-else一起使用，但要求结构不能被“打断”
- v-show
  - 写法：v-show="表达式"
  - 适用于：切换频率较高的场景
  - 不展示的DOM元素未被移除，仅仅是使用样式隐藏掉

>使用v-if时，元素可能无法获取到，而使用v-show一定可以获取到