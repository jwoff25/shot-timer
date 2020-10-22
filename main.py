import serial
from tkinter import Tk, Label, Button, Frame
import serial.tools.list_ports
import time
import os
import sys
from playsound import playsound

BAUD_RATE = 115200
TICK_RATE = 1
# SOUND_FILE = os.path.join(sys.__MEIPASS, "files/beep.mp3") if getattr(sys, 'frozen', False) else "files/beep.mp3"
SOUND_FILE = "files/beep.mp3"


class Timer():
    def __init__(self, root):
        self.root = root
        self.root.bind('<space>', self.start_timer)
        # timers
        self.start_time = 0
        self.end_time = 0
        self.running = False
        # device
        self.serial_port = None
        self.device = None
        # set serial port
        if not self.set_serial_port():
            exit(1)
        self.init_serial_device()
        # results
        self.results = []
        # UI CODE
        # timer and buttons
        self.timer_frame = Frame(root)
        self.timer_label = Label(self.timer_frame, text="00.00")
        self.timer_label.pack()
        self.start_button = Button(self.timer_frame, text="Start", command=self.start_timer)
        self.start_button.pack()
        self.stop_button = Button(self.timer_frame, text="Stop", command=self.stop_timer)
        self.stop_button.pack()
        self.timer_frame.pack()
        # table for results
        label_width = 5
        result_width = 15
        self.results_frame = Frame(root)
        self.row_1_label = Label(self.results_frame, text="1", borderwidth=1, relief="solid", width=label_width)
        self.row_1_result = Label(self.results_frame, text="", borderwidth=1, relief="solid", width=result_width)
        self.row_1_label.grid(column=0, row=0)
        self.row_1_result.grid(column=1, row=0)
        self.row_2_label = Label(self.results_frame, text="2", borderwidth=1, relief="solid", width=label_width)
        self.row_2_result = Label(self.results_frame, text="", borderwidth=1, relief="solid", width=result_width)
        self.row_2_label.grid(column=0, row=1)
        self.row_2_result.grid(column=1, row=1)
        self.row_3_label = Label(self.results_frame, text="3", borderwidth=1, relief="solid", width=label_width)
        self.row_3_result = Label(self.results_frame, text="", borderwidth=1, relief="solid", width=result_width)
        self.row_3_label.grid(column=0, row=2)
        self.row_3_result.grid(column=1, row=2)
        self.row_4_label = Label(self.results_frame, text="4", borderwidth=1, relief="solid", width=label_width)
        self.row_4_result = Label(self.results_frame, text="", borderwidth=1, relief="solid", width=result_width)
        self.row_4_label.grid(column=0, row=3)
        self.row_4_result.grid(column=1, row=3)
        self.row_5_label = Label(self.results_frame, text="5", borderwidth=1, relief="solid", width=label_width)
        self.row_5_result = Label(self.results_frame, text="", borderwidth=1, relief="solid", width=result_width)
        self.row_5_label.grid(column=0, row=4)
        self.row_5_result.grid(column=1, row=4)
        self.row_total_label = Label(self.results_frame, text="Total", borderwidth=1, relief="solid", width=label_width)
        self.row_total_result = Label(self.results_frame, text="", borderwidth=1, relief="solid",
                                      width=result_width)
        self.row_total_label.grid(column=0, row=5)
        self.row_total_result.grid(column=1, row=5)
        self.clear_button = Button(self.results_frame, text="Clear", command=self.clear_table).grid(column=1, row=6)
        self.results_frame.pack()

    def init_serial_device(self):
        try:
            self.device = serial.Serial(self.serial_port, BAUD_RATE)
        except serial.SerialException as e:
            print(e)
            exit(1)

    def set_serial_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Generic CDC" in p.description:
                self.serial_port = p.device
                return True
        return False

    @staticmethod
    def play_beep():
        playsound(SOUND_FILE)

    def start_timer(self, event=None):
        if self.running:
            return
        self.running = True
        self.root.after(3000, self.execute)

    def stop_timer(self):
        self.running = False
        self.timer_label.config(text="{:.2f}".format(self.get_total_time()))

    def get_total_time(self):
        return self.end_time - self.start_time

    def sensor_has_been_hit(self):
        out = self.device.readline().decode().rstrip()
        print("Serial output: {0}".format(out))
        if out == "1" or out == "0":
            if int(out) > 0:
                return True
        return False

    def clear_values(self):
        self.start_time = 0
        self.end_time = 0
        self.init_serial_device()

    def set_result(self):
        total = self.get_total_time()
        self.timer_label.config(text="{:.2f}".format(total))
        row_number = len(self.results) + 1
        if row_number == 1:
            self.row_1_result.config(text="{:.2f}".format(total))
        elif row_number == 2:
            self.row_2_result.config(text="{:.2f}".format(total))
        elif row_number == 3:
            self.row_3_result.config(text="{:.2f}".format(total))
        elif row_number == 4:
            self.row_4_result.config(text="{:.2f}".format(total))
        elif row_number == 5:
            self.row_5_result.config(text="{:.2f}".format(total))
        else:
            self.results = []
            self.row_1_result.config(text="")
            self.row_2_result.config(text="")
            self.row_3_result.config(text="")
            self.row_4_result.config(text="")
            self.row_5_result.config(text="")
            self.row_total_result.config(text="")
            self.row_1_result.config(text="{:.2f}".format(total))
        self.results.append(round(total, 2))
        self.calculate_and_set_total()

    def calculate_and_set_total(self):
        if len(self.results) > 1:
            total = sum([r for r in self.results if r is not max(self.results)])
            self.row_total_result.config(text="{:.2f}".format(total))
        else:
            self.row_total_result.config(text="{:.2f}".format(self.results[0]))

    def clear_table(self):
        self.results = []
        self.row_1_result.config(text="")
        self.row_2_result.config(text="")
        self.row_3_result.config(text="")
        self.row_4_result.config(text="")
        self.row_5_result.config(text="")
        self.row_total_result.config(text="")

    def timer_loop(self):
        if self.running:
            self.end_time = time.time()
            total_time = self.get_total_time()
            print(total_time)
            if self.sensor_has_been_hit():
                self.stop_timer()
                self.set_result()
            else:
                self.root.after(TICK_RATE, self.timer_loop)

    def execute(self):
        self.clear_values()
        # Play starting beep
        Timer.play_beep()
        # Get start time
        self.start_time = time.time()
        # Run timer
        self.timer_loop()


app = Tk()
app.title("Steel Challenge Timer")
gui = Timer(app)
app.minsize(300, 300)
app.mainloop()
