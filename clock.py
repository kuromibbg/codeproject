import tkinter as tk
from tkinter import messagebox
import time
import threading

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Timer")  # Set the title to "My Timer"
        self.root.geometry("800x600")  # Set window size to 800x600

        self.running = False
        self.paused = False
        self.remaining_time = 0

        # Set a larger font for better readability
        self.label = tk.Label(root, text="Enter time in hours, minutes, and seconds:", font=("Arial", 16))
        self.label.pack(pady=20)

        self.entry_hours = tk.Entry(root, font=("Arial", 16), width=5)
        self.entry_hours.pack(pady=10)
        self.entry_hours.insert(0, "0")  # Set default value to 0

        self.entry_minutes = tk.Entry(root, font=("Arial", 16), width=5)
        self.entry_minutes.pack(pady=10)
        self.entry_minutes.insert(0, "0")  # Set default value to 0

        self.entry_seconds = tk.Entry(root, font=("Arial", 16), width=5)
        self.entry_seconds.pack(pady=10)
        self.entry_seconds.insert(0, "0")  # Set default value to 0

        # Frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_countdown, font=("Arial", 16))
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_countdown, font=("Arial", 16))
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_countdown, font=("Arial", 16))
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.time_left_label = tk.Label(root, text="", font=("Arial", 48))
        self.time_left_label.pack(pady=40)

    def countdown(self, total_seconds):
        self.running = True
        self.start_button.config(state=tk.DISABLED)  # Disable the Start button
        while total_seconds > 0 and self.running:
            hrs, rem = divmod(total_seconds, 3600)
            mins, secs = divmod(rem, 60)
            self.time_left_label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")
            self.root.title(f"My Timer - {hrs:02}:{mins:02}:{secs:02}")  # Update title bar
            self.root.update()
            time.sleep(1)
            total_seconds -= 1

        if total_seconds == 0 and self.running:
            self.notify_user()

        self.reset_after_countdown()  # Reset state after countdown ends

    def notify_user(self):
        self.time_left_label.config(text="Time's up!")
        self.root.title("My Timer - Time's up!")  # Update title bar on completion
        messagebox.showinfo("Notification", "Time's up!")

    def start_countdown(self):
        if not self.running:  # Only allow starting if not already running
            try:
                hours = int(self.entry_hours.get())
                minutes = int(self.entry_minutes.get())
                seconds = int(self.entry_seconds.get())
                self.remaining_time = hours * 3600 + minutes * 60 + seconds
                if self.remaining_time > 0:
                    threading.Thread(target=self.countdown, args=(self.remaining_time,)).start()
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid numbers.")

    def pause_countdown(self):
        if self.running:
            self.running = False
            self.paused = True

    def reset_countdown(self):
        self.running = False
        self.paused = False
        self.remaining_time = 0
        self.time_left_label.config(text="")
        self.root.title("My Timer")  # Reset title
        self.start_button.config(state=tk.NORMAL)  # Re-enable the Start button

    def reset_after_countdown(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)  # Re-enable the Start button

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()