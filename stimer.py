from tkinter import *
from playsound import playsound
import time
from tkinter import ttk
import threading
import configparser

config = configparser.ConfigParser()
config.read("cfg.ini")
FOCUS = eval(config.get("top", "focus_time"))
COOLDOWNS = eval(config.get("top", "short_cooldown_time"))


def background(func, args):
    th = threading.Thread(target=func, args=args)
    th.start()


def add_leading_zero(number):
    return "{:02d}".format(number)


def Reset():
    global STOP
    STOP = True
    hr = FOCUS // (60 * 60)
    min = FOCUS // 60
    sec = FOCUS % 60
    hrs.set(add_leading_zero(hr))
    mins.set(add_leading_zero(min))
    secs.set(add_leading_zero(sec))


def set_pbar():
    pbar = ttk.Progressbar()
    pbar.place(x=50, y=0, width=300)
    return pbar


def Timer(countdown):
    global STOP
    STOP = False
    if countdown == 0:
        return
    pbar = set_pbar()
    incre_amount = 100 / countdown
    while countdown >= 0 and not STOP:
        minute, second = (countdown // 60, countdown % 60)
        hour = 0
        if minute > 60:
            hour, minute = (minute // 60, minute % 60)
        secs.set(add_leading_zero(second))
        mins.set(add_leading_zero(minute))
        hrs.set(add_leading_zero(hour))
        root.update()
        time.sleep(1)
        countdown -= 1
        pbar.step(incre_amount)
    pbar.destroy()


def _playsound(filepath):
    # playsound(filepath)
    background(playsound, (filepath,))


def Start(cooldown=True, cooldown_time=COOLDOWNS):
    countdown = int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(secs.get())
    Timer(countdown)
    if not STOP:
        _playsound("asset/alarm.mp3")
        if cooldown:
            Timer(cooldown_time)


def Stop():
    global STOP
    STOP = True


root = Tk()
root.title("sTimer")
root.geometry("400x160+0+0")
root.config(bg="#000")
root.resizable(False, False)
root.wm_attributes("-topmost", 1)

# timer
timer_y = 20
unit_y = timer_y + 40
hrs = StringVar()
Entry(
    root, textvariable=hrs, width=2, font="arial 50", bg="#001", fg="#fff", bd=0
).place(x=30, y=timer_y)
hrs.set(add_leading_zero(FOCUS // (60 * 60)))
mins = StringVar()
Entry(
    root, textvariable=mins, width=2, font="arial 50", bg="#001", fg="#fff", bd=0
).place(x=150, y=timer_y)
mins.set(add_leading_zero(FOCUS // (60)))
secs = StringVar()
Entry(
    root, textvariable=secs, width=2, font="arial 50", bg="#001", fg="#fff", bd=0
).place(x=270, y=timer_y)
secs.set(add_leading_zero(FOCUS % 60))
Label(root, text="hour", font="arial 15", bg="#000", fg="#fff").place(x=105, y=unit_y)
Label(root, text="min", font="arial 15", bg="#000", fg="#fff").place(x=225, y=unit_y)
Label(root, text="sec", font="arial 15", bg="#000", fg="#fff").place(x=345, y=unit_y)

buttonStart = Button(
    root,
    text="Start",
    bg="#ea3548",
    bd=0,
    fg="#fff",
    width=10,
    height=2,
    font="arial 10 bold",
    command=Start,
)
buttonStop = Button(
    root,
    text="Stop",
    bg="#ea3548",
    bd=0,
    fg="#fff",
    width=10,
    height=2,
    font="arial 10 bold",
    command=Stop,
)
buttonFocus = Button(
    root,
    text="Reset",
    bg="#ea3548",
    bd=0,
    fg="#fff",
    width=10,
    height=2,
    font="arial 10 bold",
    command=Reset,
)
button_y = timer_y + 80
xs = [30, 155, 280]
buttonFocus.place(x=xs[0], y=button_y)
buttonStart.place(x=xs[1], y=button_y)
buttonStop.place(x=xs[2], y=button_y)


root.mainloop()
