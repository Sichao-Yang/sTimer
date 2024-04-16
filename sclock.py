from datetime import datetime
import time
from tkinter import *
from stimer import add_leading_zero, splaysound


def gettime():
    now = datetime.now()
    return now.hour, now.minute, now.second

def main():
    second_screen = "right"
    sound_path_tick = "asset/audio/tick.mp3"
    tick = True

    root = Tk()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    print(f"screen1:\nscreenwidth: {sw}\nscreenheight: {sh}")


    if sh == 1440:
        font_size = 300
        x_start = 100
        y_shift = 300
    else:
        raise NotImplementedError

    if second_screen == "right":
        root.geometry("%dx%d%+d+%d" % (sw, sh, sw, 0))
    elif second_screen == "left":
        root.geometry("%dx%d%+d+%d" % (sw, sh, -sw, 0))
    else:
        raise NotImplementedError
    root.configure(background="#001")


    x_shift = sw // 3
    y_start = sh // 2 - y_shift
    Font_tuple = ("Arial Black", font_size, "")
    hrs = StringVar()
    Entry(
        root, textvariable=hrs, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0
    ).place(x=x_start, y=y_start)
    mins = StringVar()
    Entry(
        root, textvariable=mins, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0
    ).place(x=x_start + x_shift, y=y_start)
    secs = StringVar()
    Entry(
        root, textvariable=secs, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0
    ).place(x=x_start + x_shift * 2, y=y_start)


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
