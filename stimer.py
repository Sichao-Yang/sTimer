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
        self.focus_time = self.conv_int(config.get("top", "focus_time"))
        self.short_cooldown = self.conv_int(config.get("top", "short_cooldown_time"))
        self.tick = config.getboolean("top", "tick")
        self.cooldown = cooldown
        self.sound_path_work = config.get("top", "sound_path_work")
        self.sound_path_short_cooldown = config.get("top", "sound_path_short_cooldown")
        self.sound_path_tick = config.get("top", "sound_path_tick")
        self.window_position = config.get("top", "window_position")
        self.total_rep = self.conv_int(config.get("top", "repetition"))
        self.current_rep = 0
        self.timer_active_timer = False
        self.loop_state = "focus"

    def conv_int(self, str):
        return int(eval(str))

    def _format_rep(self):
        return f"{self.current_rep}/{self.total_rep}"

    def _reset_rep(self):
        self.current_rep = 0
        return self._format_rep()

    def _incr_rep(self):
        self.current_rep += 1
        return self._format_rep()

    def run(self):
        self.root = Tk()
        self.root.title("sTimer")

        height = 160
        width = 400
        bottom_y_margin = 70
        # Get the current screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print("Screen width:", screen_width)
        print("Screen height:", screen_height)

        position = {
            "topleft": (0, 0),
            "topright": (screen_width - width, 0),
            "bottomleft": (0, screen_height - height - bottom_y_margin),
            "bottomright": (screen_width - width, screen_height - height - bottom_y_margin),
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

        # repetition
        self.rep_count = StringVar()
        Entry(
            self.root, textvariable=self.rep_count, width=3, font=("Arial Black", 10, ""), bg="#001", fg="#fff", bd=0
        ).place(x=5, y=timer_y - 10)
        self.rep_count.set(self._format_rep())
        # control button
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

    @property
    def timer_active(self):
        return self._active

    @timer_active.setter
    def timer_active(self, value):
        self._active = value

    def start_timer(self):
        self.timer_active = True

    def Stop(self):
        self.timer_active = False

    def Reset(self):
        self.Stop()
        self._reset_timer()
        self.rep_count.set(self._reset_rep())
        # force loop state back to focus
        self.loop_state = "focus"

    def _reset_timer(self):
        hr = self.focus_time // (60 * 60)
        min = self.focus_time // 60
        sec = self.focus_time % 60
        self.hrs.set(add_leading_zero(hr))
        self.mins.set(add_leading_zero(min))
        self.secs.set(add_leading_zero(sec))

    def Start(self):
        self.start_timer()
        while (self.current_rep < self.total_rep) and self.timer_active:
            countdown = int(self.hrs.get()) * 3600 + int(self.mins.get()) * 60 + int(self.secs.get())
            if self.loop_state == "focus":
                _playsound(self.sound_path_work)
                self.Timer(countdown, self.tick)
                if self.timer_active:
                    self.loop_state = "cooldown"
                    _playsound(self.sound_path_short_cooldown)
                    countdown = self.short_cooldown
            if self.loop_state == "cooldown":
                if self.cooldown:
                    # dont play tick sound while cooldown
                    self.Timer(countdown, False)
            # only when the timer finished without stop signal, the following will execute
            if self.timer_active:
                self._incr_rep()
                self.rep_count.set(self._format_rep())
                self._reset_timer()
                self.loop_state = "focus"

    def Timer(self, countdown, tick):
        if countdown == 0:
            return
        pbar = set_pbar()
        incr_amount = 100 / countdown
        while (countdown >= 0) and (self.timer_active):
            minute, second = (countdown // 60, countdown % 60)
            hour = 0
            if minute > 60:
                hour, minute = (minute // 60, minute % 60)
            self.secs.set(add_leading_zero(second))
            self.mins.set(add_leading_zero(minute))
            self.hrs.set(add_leading_zero(hour))
            self.root.update()
            pbar.step(incr_amount)
            if tick:
                _playsound(self.sound_path_tick)
            countdown -= 1
            time.sleep(1)
        pbar.destroy()


def run():
    st = sTimer()
    st.run()


if __name__ == "__main__":
    # st = sTimer()
    # st.stop = True
    # print(st.stop)
    run()
