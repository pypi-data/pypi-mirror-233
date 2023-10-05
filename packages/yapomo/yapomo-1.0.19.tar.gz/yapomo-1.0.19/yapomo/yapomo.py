"yapomo - Yet Another Pomodoro Timer."

"""Copyright (C) 2023  João Dias

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import Tk, Toplevel, ttk, font

from datetime import timedelta
import time

class const():
    DURATION = 25 # minutes
    SIZE_RATIO = 1 / 9  # of screen width

    # unicode symbols
    READY, STARTED, PAUSED = "\u23f5", "\u23f2", "\u23f8"

    UPDATE_RATE = 100 # miliseconds

class PomodoroTimer:
    def __init__(self, window):
        self.window = window
        self.window.title("yapomo")
        self.adapt_size_to_screen(window)
        self.counter = 0
        self.time_left = const.DURATION * 60 # in seconds
        self.state = "READY" # or "STARTED" or "PAUSED"
        self.setup_widgets(window)
        self.setup_ui_bindings()
        self.register_callback()

    def adapt_size_to_screen(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        screen_ratio = self.screen_ratio = int(screen_width / screen_height)

        self.width = int(screen_width * const.SIZE_RATIO)
        self.height = int(self.width / screen_ratio)

        window.geometry("{}x{}".format(self.width, self.height))
        window.resizable(width=False, height=False)

    def setup_widgets(self, window):
        w = self.width
        h = self.height
        canvas = self.canvas = tk.Canvas(window, bg="black")

        # arc extent
        extent = 0

        self.outline = canvas.create_arc(
            int(w * 0.05),
            int(h * 0.05),
            int(w * 0.95),
            int(h * 0.95),
            start=90,
            extent=extent,
            fill="red",
            outline="red")

        self.circle = canvas.create_arc(
            int(w * 0.09),
            int(h * 0.09),
            int(w * 0.91),
            int(h * 0.91),
            start=90,
            extent=359.9,
            fill="black",
            outline="black"
        )

        self.counter_label = canvas.create_text(
            int(w / 2),
            int(h / 2),
            text=str(self.counter)
         )

        counter_font = font.Font(family="TkTextFont", size=64)

        canvas.itemconfigure(
            self.counter_label,
            fill="#801010",
            font=counter_font
        )


        t = timedelta(seconds=self.time_left)
        self.time_left_label = canvas.create_text(
            int(w / 2),
            int(h / 2),
            text="0{}".format(str(t)) if (len(str(t)) == 7) else str(t)
         )

        time_left_font = font.Font(family="TkTextFont", size=18)

        canvas.itemconfigure(
            self.time_left_label,
            fill="white",
            font=time_left_font
        )

        self.status_label = canvas.create_text(
            int(w / 2),
            int(h / 1.225),
            text=const.READY
         )

        status_font = font.Font(family="TkTextFont", size=24)

        canvas.itemconfigure(
            self.status_label,
            fill="gray",
            font=status_font
        )

        canvas.grid(row=0, column=0, sticky=tk.NSEW)

    def setup_ui_bindings(self):
        self.canvas.bind("<Button-1>", self.next_state)

    def next_state(self, event=None):
        if self.state == "READY":
            self.start_time = time.time() # seconds since Unix epoch.
            self.state = "STARTED"
        elif self.state == "STARTED":
            self.state = "PAUSED"
        elif self.state == "PAUSED":
            self.start_time = time.time() - (60 * const.DURATION - self.time_left)
            self.state = "STARTED"

    def register_callback(self):
        self.canvas.after(const.UPDATE_RATE, self.on_update)

    def on_update(self):
        flag = False
        if self.state == "STARTED":
            self.current_time = time.time()
            self.time_left = 60 * const.DURATION - (
                self.current_time - self.start_time
            )
            if self.time_left < 0:
                self.state = "READY"
                self.time_left = const.DURATION * 60
                self.counter += 1
                flag = True
        self.update_widgets()
        if flag:
            flag = False
            self.flash_counter()

        self.canvas.after(const.UPDATE_RATE, self.on_update)

    def flash_counter(self):
        for i in range(20):
            self.canvas.itemconfigure(
                self.counter_label,
                fill="#FF0000",
            )
            self.window.update()
            time.sleep(0.25)
            self.canvas.itemconfigure(
                self.counter_label,
                fill="#801010",
            )
            self.window.update()
            time.sleep(0.25)


    def update_widgets(self):
        self.canvas.itemconfigure(
            self.outline,
            extent= -359.9 * (1 - self.time_left / (const.DURATION * 60))
        )

        t = timedelta(seconds=int(self.time_left))
        self.canvas.itemconfigure(
            self.time_left_label,
            text="0{}".format(str(t)) if (len(str(t)) == 7) else str(t)
 
        )

        self.canvas.itemconfigure(
            self.counter_label,
            text=str(self.counter)
        )

        if self.state == "READY":
            self.canvas.itemconfigure(
                self.status_label,
                text=const.READY
            )
        elif self.state == "STARTED":
            self.canvas.itemconfigure(
                self.status_label,
                text=const.STARTED
            )
        elif self.state == "PAUSED":
            self.canvas.itemconfigure(
                self.status_label,
                text=const.PAUSED
            )

    def reset(self):
        self.state = "READY"
        self.time_left = 60 * const.DURATION

    def reset_all(self):
        self.state = "READY"
        self.counter = 0
        self.time_left = 60 * const.DURATION


    def on_right_click(self, event=None):
        self.popup_menu.tk_popup(event.x_root, event.y_root)
    
    def on_escape(self, event=None):
        self.popup_menu.unpost()


def main():
    root = Tk()
    root.option_add("*tearOff", tk.FALSE)
    
    pt = PomodoroTimer(root)
    
    popup_menu = tk.Menu(root)
    popup_menu.add_command(
        label="Reset",
        command=pt.reset
        )
    popup_menu.add_command(
        label="Reset All",
        command=pt.reset_all
        )
    popup_menu.add_command(
        label="Quit",
        command=root.destroy
        )
    
    pt.popup_menu = popup_menu
    
    root.bind("<3>", pt.on_right_click)
    root.bind("<Escape>", pt.on_escape)
    
    root.mainloop()
        
