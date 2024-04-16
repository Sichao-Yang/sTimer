import re
from datetime import datetime
import configparser
import time
from tkinter import *
from stimer import add_leading_zero, splaysound


def gettime():
    now = datetime.now()
    return now.hour, now.minute, now.second


def parse_ss(ss_str):
    ret = re.match("(\d+)x(\d+)", ss_str)
    if ret:
        return int(ret[1]), int(ret[2])
    else:
        raise ValueError("screen_size format is not as 1920x1080, please check!")

def resize(var_int, ratio):
    return int(var_int/ratio)

def main():
    config = configparser.ConfigParser()
    config.read("cfg.ini")
    second_screen = config.get("top", "second_screen_position")
    sound_path_tick = config.get("top", "sound_path_tick")
    tick = config.getboolean("top", "tick")

    root = Tk()
    # the best way to check screen1 and 2's size is still to manually check in windows display setting
    # sw1, sh1 = root.winfo_screenwidth(), root.winfo_screenheight()
    sw1, sh1 = parse_ss(config.get("top", "screen1_size"))
    sw2, sh2 = parse_ss(config.get("top", "screen2_size"))
    
    if second_screen == "right":
        root.geometry("%dx%d%+d+%d" % (sw2, sh2, sw1, 0))
    elif second_screen == "left":
        root.geometry("%dx%d%+d+%d" % (sw2, sh2, -sw1, 0))
    elif second_screen == "no":
        laptop_ratio = eval(config.get("top", "laptop_ratio"))
        if laptop_ratio !=1:
            sw1 = resize(sw1, laptop_ratio)
            sh1 = resize(sh1, laptop_ratio)
        sw2 = sw1
        sh2 = sh1
        root.geometry("%dx%d%+d+%d" % (sw2, sh2, 0, 0))
    else:
        raise NotImplementedError

    print(f"screen2:\nscreenwidth: {sw2}\nscreenheight: {sh2}")

    # default setting based on sh: 1440
    font_size = 300
    x_start = 100
    y_shift = 300
    # resize
    if sh2 in [1080, 1200, 960]:
        ratio = 1440/sh2
        font_size = resize(font_size, ratio)
        x_start = resize(x_start, ratio)
        y_shift = resize(y_shift, ratio)
    else:
        raise NotImplementedError

    root.configure(background="#001")

    x_shift = sw2 // 3
    y_start = sh2 // 2 - y_shift
    Font_tuple = ("Arial Black", font_size, "")
    hrs = StringVar()
    Entry(root, textvariable=hrs, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0).place(x=x_start, y=y_start)
    mins = StringVar()
    Entry(root, textvariable=mins, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0).place(
        x=x_start + x_shift, y=y_start
    )
    secs = StringVar()
    Entry(root, textvariable=secs, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0).place(
        x=x_start + x_shift * 2, y=y_start
    )

    def clocking():
        while True:
            hr, min, sec = gettime()
            hrs.set(add_leading_zero(hr))
            mins.set(add_leading_zero(min))
            secs.set(add_leading_zero(sec))
            root.update()
            if tick:
                splaysound(sound_path_tick)
            time.sleep(1)

    Button(root, text="Start Clock", command=clocking).pack()
    root.mainloop()


if __name__ == "__main__":
    main()
