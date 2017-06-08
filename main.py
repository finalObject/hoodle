from tkinter import *
import random
import time
from ball import *
from paddle import *

tk = Tk()
tk.title("Game")
tk.resizable(0,0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk,width=500,height=400,bd=0,highlightthickness=0)
canvas.pack()
tk.update();
paddle = Paddle(canvas,'gray')
ball = Ball(canvas,'red',paddle)
while 1:
    if ball.hit_bottom==False:
        ball.draw()
    paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
