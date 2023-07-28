import tkinter as tk
from tkinter import messagebox
import time
import threading


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro App")

        self.work_time = 0  # Inicialmente, el contador será 00:00
        self.short_break_time = 5 * 60  # 5 minutes in seconds
        self.long_break_time = 15 * 60  # 15 minutes in seconds

        self.is_break = False
        self.is_running = False
        self.is_paused = False
        self.pause_time = 0

        self.work_timer_label = tk.Label(root, text="Work Time (minutes):")
        self.work_timer_label.pack(pady=5)

        self.work_timer_value = tk.StringVar()
        self.work_timer_value.set("25")  # Default work time is 25 minutes
        self.work_timer_entry = tk.Entry(root, textvariable=self.work_timer_value, font=("Helvetica", 16))
        self.work_timer_entry.pack()

        self.break_timer_label = tk.Label(root, text="Break Time (minutes):")
        self.break_timer_label.pack(pady=5)

        self.break_timer_value = tk.StringVar()
        self.break_timer_value.set("5")  # Default break time is 5 minutes
        self.break_timer_entry = tk.Entry(root, textvariable=self.break_timer_value, font=("Helvetica", 16))
        self.break_timer_entry.pack()

        self.timer_label = tk.Label(root, text="00:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_timer, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Ajustar el tamaño de la ventana
        root.geometry("400x250")

    def start_timer(self):
        if not self.is_running:
            try:
                work_timer_minutes = int(self.work_timer_value.get())
                break_timer_minutes = int(self.break_timer_value.get())
                if work_timer_minutes <= 0 or break_timer_minutes <= 0:
                    raise ValueError
                self.work_time = work_timer_minutes * 60
                self.short_break_time = break_timer_minutes * 60
                self.timer_label.config(text=self.format_time(self.work_time))
                self.is_running = True
                self.update_timer()
                self.pause_button.config(state=tk.NORMAL)
                self.reset_button.config(state=tk.NORMAL)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid positive numbers for work and break time.")

    def pause_timer(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_button.config(text="Resume")
            self.pause_time = time.time() - self.pause_time
        elif self.is_running and self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="Pause")
            self.pause_time = time.time() - self.pause_time
            self.update_timer()

    def update_timer(self):
        if self.is_running and not self.is_paused:
            if self.work_time > 0:
                self.work_time -= 1
                self.timer_label.config(text=self.format_time(self.work_time))
                self.root.after(1000, self.update_timer)
            else:
                if not self.is_break:
                    self.work_time = int(self.break_timer_value.get()) * 60  # Start break time
                    self.is_break = True
                    self.show_notification("Time to take a break!")
                else:
                    self.work_time = int(self.work_timer_value.get()) * 60  # Start work time
                    self.is_break = False
                    self.show_notification("Time to get back to work!")
                self.timer_label.config(text=self.format_time(self.work_time))
                if self.work_time > 0:  # Added this condition to stop the break timer when it reaches zero
                    self.update_timer()  # Start the next timer automatically

    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.is_break = False
        self.work_time = int(self.work_timer_value.get()) * 60
        self.timer_label.config(text=self.format_time(self.work_time))
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def show_notification(self, message):
        threading.Thread(target=messagebox.showinfo, args=("Pomodoro Notification", message)).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
