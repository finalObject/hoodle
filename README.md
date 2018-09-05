原本在这里 <a href="http://finalobject.cn/lucario/hoddle">finalobject.cn</a>

刚刚开始接触python，在实验室翻到了一本python的书，感觉像是给零基础，甚至可能是小孩看的，名字记不起来了，反正看着很有意思，教你写几个小游戏。花了两天时间follow了两个游戏，一个是这个，另外一个是火柴人。

把自己实现的过程，还有一些对于tkinter和python的理解记录下来。

github：<a href="https://github.com/finalObject/hoodle">https://github.com/finalObject/hoodle</a>

<img class="size-medium wp-image-200 aligncenter" src="http://finalobject.cn/wp-content/uploads/2018/09/hoddle-1-300x253.jpg" alt="" width="300" height="253" />
<p style="text-align: center;">极其简单的界面</p>

<h1>环境问题</h1>
一开始写这个代码的时候是可以顺利导入tkinter的，但是能到我想总结一下，写这篇文章的时候，无论是python2还是python3，都无法顺利导入tkinter/Tkinter了。

原因的话应该是我卸载过mac自带的python，然后用homebrew重新安装过，导致环境不一样了。据说tkinter是python自带的，不应该出现这种情况，然后看了官网，有这么一段话
<blockquote>
<h5>If you are using Python (prior to 3.7) from a python.org 64-bit/32-bit Python installer for macOS 10.6 and later, you should only use IDLE or tkinter with an updated third-party Tcl/Tk 8.5 (not 8.6), like <a class="reference external" href="http://www.activestate.com/activetcl/downloads">ActiveTcl 8.5</a> installed.</h5>
</blockquote>
貌似说新版本python3需要使用第三方TCL/TK才能正常使用。我就是直接安装了这里推荐的activetcl，安装完毕之后python3能够正常导入tkinter了。另外，安装完之后多了一个叫做wish的桌面软件，应该也是这个第三方库自带的一个桌面程序吧。
<h1>基本结构</h1>
tkinter这个库貌似特别的轻量，很多人并不推荐做大型的桌面程序开发，不过作为入门python图形界面的话我感觉再好不过了，毕竟图形界面编程的思路大致都是相通的。

在tkinter里，可以用Tk()获取一个窗口，然后在初始化一个画布和这个窗口绑定起来，之后再创造画布中使用到的一个个元素，每个元素拥有图形啊坐标啊之类的属性，并且拥有一个draw()函数，更新其在画布上的状态。设置好所有元素的属性和行为之后，只需要在主程序里不断更新画布就可以了。

当然上面这个思路并不是必须的，只不过是相对来讲比较好的一个实现方式。tkinter并不限制你用其他的形式去实现图形界面，本身就只是提供了两个（目前使用到的）输入输出的函数，一个是输入绑定函数，用来检测键盘输入，一个是move函数，在往画布上添加元素的时候，会返回一个id，可以用过id来控制该元素在画布上的显示。
<h1>代码实现</h1>
项目中是三个py文件，分别是main.py，ball.py以及paddle.py，后面两个文件分别定义了ball和paddle两个类。

main.py:
<pre class="lang:python decode:true" title="main.py">from tkinter import *
import random
import time
from ball import *
from paddle import *

#初始化窗口
tk = Tk()
tk.title("Game")
tk.resizable(0,0)
tk.wm_attributes("-topmost",1)
#添加绑定在这个窗口上的画布
canvas = Canvas(tk,width=500,height=400,bd=0,highlightthickness=0)
#根据画布内容调整大小
canvas.pack()
#更新窗口
tk.update();
#初始化自己定义的两个对象，球拍和球
paddle = Paddle(canvas,'gray')
ball = Ball(canvas,'red',paddle)
#开始主循环，不断更新
while 1:
    ball.draw()
    paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
</pre>
paddle.py:
<pre class="lang:python decode:true" title="paddle.py">from tkinter import *
import random
import time
class Paddle:
    def __init__(self,canvas,color):
        self.canvas = canvas
        #在画布中创建一个矩形，代表球拍，矩形的id返还给球拍类，使得后面能够对其进行空寂
        self.id = canvas.create_rectangle(0,0,100,10,fill=color)
        #设置这个矩形在画布中的初始位置
        self.canvas.move(self.id,200,300)
        #这是球拍水平移动的速度
        self.x=0
        self.canvas_width=self.canvas.winfo_width()
        #按键绑定
        self.canvas.bind_all('&lt;KeyPress-Left&gt;',self.turn_left)
        self.canvas.bind_all('&lt;KeyPress-Right&gt;',self.turn_right)
    #对应的按键绑定函数   
    def turn_left(self,evt):
        #如果按下左键，球拍的速度就变更为-5，也就是往左的速度
        self.x = -5
    def turn_right(self,evt):
        #同理
        self.x = 5
    def draw(self):
        #根据速度更新自己在画布中的位置
        self.canvas.move(self.id,self.x,0)
        #获取其在画布中的位置，pos是一个数组[x1,y1,x2,y2]，应该就是左上点和右下点的坐标
        pos = self.canvas.coords(self.id)
        #如果碰触边界，速度变为反方向的1
        if pos[0]&lt;=0:
            self.x=1
        if pos[2]&gt;=self.canvas_width:
            self.x=-1</pre>
ball.py:
<pre class="lang:python decode:true" title="ball.py">from tkinter import *
import random
import time

class Ball:
    def __init__(self,canvas,color,paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10,10,25,25,fill=color)
        self.canvas.move(self.id,245,100)
        #这个数组是引入随机数，使得球横向速度是这个数组中的随机一个
        starts=[-3,-2,-1,1,2,3]
        #改变数组的元素的位置，随机的
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        #这个是触底信号，如果小球触底了，那么变成True
        self.hit_bottom = False
    def hit_bon(self):
        #边界触碰检测，这个球的边界触碰仍然使用左上点和右下点（是有一点不科学）
        pos = self.canvas.coords(self.id)
        posP = self.canvas.coords(self.paddle.id)
        #如果触边，对应方向的速度就变成反方向的3
        if pos[1] &lt;= 0:
            self.y = 3
        if pos[3]&gt;=self.canvas_height:
            self.y = -3
            #如果触底，设置标志位，可以作为游戏结束的依据
            self.hit_bottom = True
        if pos[0] &lt;= 0:
            self.x = 3
        if pos[2] &gt;= self.canvas_width:
            self.x = -3
    #和球拍的碰触检测，和边界触碰检测同理，不过这个并不会更新速度，而是吧信号返回
    def hit_paddle(self):
        pos = self.canvas.coords(self.id)
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2]&gt;=paddle_pos[0] and pos[0]&lt;=paddle_pos[2]:
            if pos[3]&gt;=paddle_pos[1] and pos[3]&lt;=paddle_pos[3]:
                return True
        return False
    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        self.hit_bon()
        #检测到碰触球拍，修改速度
        if self.hit_paddle()==True:
            self.y = -self.y
</pre>
有一点点需要讨论的地方就是，ball里面虽然设置了触底信号，但是却没用实际用起来。不过github上应该是用起来了，就是把main.py中（我这个代码插件写上中文注释行号显示貌似就会有问题）
<pre class="lang:python decode:true ">ball.draw()</pre>
修改为
<pre class="lang:default decode:true ">if ball.hit_bottom==False:
    ball.draw()</pre>
这样的话球一旦触底，就会被粘在底边上啦哈哈。不过就在我写文章的时候我才意识到，这样其实是不太好的，虽然直观得就是球一旦触底就不再更新位置了，但是这个逻辑判断不应该加载主函数里，这个不应该是主函数需要考虑的问题。

这段判断代码应该加载ball自己的draw函数里，如果触底，就不进行移动以及其他的检测。

另外注意到画布里的move函数，发现在两个类初始化的时候，这个move函数里输入的直接就是初始坐标，但是在每次的更新中，move函数输入的却是代表速度的x和y，也就是单位时间的偏移量。其实是这样的，每个元素被创建的时候，默认的位置是(0,0)，然后所以第一次调用move函数的时候，输入的是偏移量，但是由于原来的初始位置是(0,0)，所以结果就是最终坐标也就是偏移量。
