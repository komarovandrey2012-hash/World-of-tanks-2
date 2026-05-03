from units import Tank
from tkinter import*

HP = 100
canvas = Canvas

def get_hp():
    return Tank.get_hp()

def update():
    if get_hp() == 100:
        return
    elif get_hp() == 75:
        canvas.itemconfig()