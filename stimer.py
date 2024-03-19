from tkinter import *
from playsound import playsound
import time
from tkinter import ttk
import threading
import configparser
from tkinter import font


def background(func, args):
    th = threading.Thread(target=func, args=args)
    th.start()


def add_leading_zero(number):
    return "{:02d}".format(number)


def get_available_fonts():
    root = Tk()
    root.title("Font Families")
    print(list(font.families()))


def set_pbar():
    pbar = ttk.Progressbar()
    pbar.place(x=50, y=0, width=300)
    return pbar


def _playsound(filepath):
    # playsound(filepath)
    background(playsound, (filepath,))


class sTimer:
    def __init__(self, config_path=None, cooldown=True):
        config = configparser.ConfigParser()
        if config_path is None:
            config.read("cfg.ini")
        else:
            config.read(config_path)
        self.focus_time = int(eval(config.get("top", "focus_time")))
        self.short_cooldown = int(eval(config.get("top", "short_cooldown_time")))
        self.tick = config.getboolean("top", "tick")
        self.cooldown = cooldown
        self.sound_path_work = config.get("top", "sound_path_work")
        self.sound_path_short_cooldown = config.get("top", "sound_path_short_cooldown")
        self.sound_path_tick = config.get("top", "sound_path_tick")
        self.window_position = config.get("top", "window_position")
        self.stop = False

    def run(self):
        self.root = Tk()
        self.root.title("sTimer")

        height = 160
        width = 400
        # Get the current screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print("Screen width:", screen_width)
        print("Screen height:", screen_height)

        position = {
            "topleft": (0, 0),
            "topright": (screen_width - width, 0),
            "bottomleft": (0, screen_height - height - 40),
            "bottomright": (screen_width - width, screen_height - height - 40),
        }
        x, y = position["bottomright"]
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.config(bg="#000")
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", 1)

        # timer
        timer_y = 20
        unit_y = timer_y + 40
        Font_tuple = ("Arial Black", 40, "")
        self.hrs = StringVar()
        Entry(self.root, textvariable=self.hrs, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0).place(
            x=30, y=timer_y
        )
        self.hrs.set(add_leading_zero(self.focus_time // (60 * 60)))
        self.mins = StringVar()
        Entry(self.root, textvariable=self.mins, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0).place(
            x=150, y=timer_y
        )
        self.mins.set(add_leading_zero(self.focus_time // (60)))
        self.secs = StringVar()
        Entry(self.root, textvariable=self.secs, width=2, font=Font_tuple, bg="#001", fg="#fff", bd=0).place(
            x=270, y=timer_y
        )
        self.secs.set(add_leading_zero(self.focus_time % 60))

        Font_tuple = ("Arial", 15, "")
        Label(self.root, text="hr", font=Font_tuple, bg="#000", fg="#fff").place(x=105, y=unit_y)
        Label(self.root, text="min", font=Font_tuple, bg="#000", fg="#fff").place(x=225, y=unit_y)
        Label(self.root, text="sec", font=Font_tuple, bg="#000", fg="#fff").place(x=345, y=unit_y)
        Font_tuple = ("Arial", 10, "bold")
        buttonStart = Button(
            self.root,
            text="Start",
            bg="#ea3548",
            bd=0,
            fg="#fff",
            width=10,
            height=2,
            font=Font_tuple,
            command=self.Start,
        )
        buttonStop = Button(
            self.root,
            text="Stop",
            bg="#ea3548",
            bd=0,
            fg="#fff",
            width=10,
            height=2,
            font=Font_tuple,
            command=self.Stop,
        )
        buttonFocus = Button(
            self.root,
            text="Reset",
            bg="#ea3548",
            bd=0,
            fg="#fff",
            width=10,
            height=2,
            font=Font_tuple,
            command=self.Reset,
        )
        button_y = timer_y + 80
        xs = [30, 155, 280]
        buttonFocus.place(x=xs[0], y=button_y)
        buttonStart.place(x=xs[1], y=button_y)
        buttonStop.place(x=xs[2], y=button_y)

        self.root.mainloop()

    def Stop(self):
        self.stop = True

    def Reset(self):
        self.stop = True
        hr = self.focus_time // (60 * 60)
        min = self.focus_time // 60
        sec = self.focus_time % 60
        self.hrs.set(add_leading_zero(hr))
        self.mins.set(add_leading_zero(min))
        self.secs.set(add_leading_zero(sec))

    def Start(self):
        countdown = int(self.hrs.get()) * 3600 + int(self.mins.get()) * 60 + int(self.secs.get())
        _playsound(self.sound_path_work)
        self.Timer(countdown, self.tick)
        if not self.stop:
            _playsound(self.sound_path_short_cooldown)
            if self.cooldown:
                # dont play tick sound while cooldown
                self.Timer(self.short_cooldown, False)

    def Timer(self, countdown, tick):
        self.stop = False
        if countdown == 0:
            return
        pbar = set_pbar()
        incre_amount = 100 / countdown
        while countdown >= 0 and not self.stop:
            minute, second = (countdown // 60, countdown % 60)
            hour = 0
            if minute > 60:
                hour, minute = (minute // 60, minute % 60)
            self.secs.set(add_leading_zero(second))
            self.mins.set(add_leading_zero(minute))
            self.hrs.set(add_leading_zero(hour))
            self.root.update()
            time.sleep(1)
            if tick:
                _playsound(self.sound_path_tick)
            pbar.step(incre_amount)
            countdown -= 1
        pbar.destroy()


def run():
    st = sTimer()
    st.run()


if __name__ == "__main__":
    run()
