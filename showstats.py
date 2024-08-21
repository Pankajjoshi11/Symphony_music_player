import tkinter as tk
import matplotlib.pyplot as plt
from datetime import datetime
import pickle

class TkinterWindowDurationTracker:
    def __init__(self):
        self.window = tk.Tk()
        self.start_time = None
        self.end_time = None
        self.durations = []  # Initialize durations as an empty list
        self.run_count = 0
        self.load_durations()

        # Add a label to display statistics
        self.stats_label = tk.Label(self.window, text="Statistics: ", font=("Helvetica", 12))
        self.stats_label.pack()

    def load_durations(self):
        try:
            with open("durations.pkl", "rb") as f:
                self.durations, self.run_count = pickle.load(f)
        except FileNotFoundError:
            pass

        # Ensure self.durations is always a list
        if not isinstance(self.durations, list):
            self.durations = []

    def save_durations(self):
        with open("durations.pkl", "wb") as f:
            pickle.dump((self.durations, self.run_count), f)

    def calculate_statistics(self):
        if self.durations:
            average_duration = sum(self.durations) / len(self.durations)
            max_duration = max(self.durations)
            min_duration = min(self.durations)
            return f"Average Duration: {average_duration:.2f} seconds, Max Duration: {max_duration:.2f} seconds, Min Duration: {min_duration:.2f} seconds"
        else:
            return "No statistics available."

    def on_window_close(self):
        self.end_time = datetime.now()
        if self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
            self.durations.append(duration)
            self.run_count += 1
            if self.run_count % 5 == 0:
                self.durations = []  # Reset durations after every 5 runs
            self.save_durations()
        self.window.quit()

    def run(self):
        self.start_time = datetime.now()
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.window.mainloop()

def plot_durations(durations):
    plt.plot(durations)
    plt.xlabel('Run')
    plt.ylabel('Window Open Duration (seconds)')
    plt.title('Tkinter Window Open Duration Across Runs')
    plt.show()

if __name__ == "__main__":
    tracker = TkinterWindowDurationTracker()
    tracker.run()
    plot_durations(tracker.durations)
