from openpyxl import Workbook
from datetime import datetime
from tkinter import filedialog 
from google_sheet_utils import GoogleSheetUtils
import pygetwindow as gw
from tkinter import ttk
import tkinter as tk
import pandas as pd
import threading
import time
import os


g_sheet = GoogleSheetUtils()


class WindowTimeTracker:
    def __init__(self):
        self.active_window = None
        self.start_time = None
        self.window_time_dict = {}
        self.today_date = datetime.now().strftime("%Y-%m-%d")
        self.stop_tracking_event = threading.Event()
        self.idle_timer = threading.Timer(300, self.handle_idle)
        self.idle_start_time = None
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Window Time Tracker")

        start_button = ttk.Button(self.root, text="Start", command=self.start_tracking_thread)
        start_button.pack()

        stop_button = ttk.Button(self.root, text="Stop", command=self.save_data_on_exit)
        stop_button.pack()

    def start_tracking_thread(self):
        threading.Thread(target=self.start_tracking).start()
        self.root.iconify()  # Minimize the main window

    def start_tracking(self):
        while not self.stop_tracking_event.is_set():
            new_active_window = gw.getActiveWindow()
            if new_active_window != self.active_window:
                if self.start_time is not None:
                    end_time = time.time()
                    elapsed_time = end_time - self.start_time
                    if self.active_window is not None and self.active_window.title != "Window Time Tracker":
                        self.update_window_time(self.active_window.title, int(elapsed_time))
                        print(f"Time spent in '{self.active_window.title}': {elapsed_time:.2f} seconds")
                self.active_window = new_active_window
                self.start_time = time.time()
                if self.idle_start_time is not None:
                    self.idle_timer.cancel()
                    self.idle_start_time = None
            else:
                if self.start_time is not None:
                    current_time = time.time()
                    if current_time - self.start_time >= 300 and self.idle_start_time is None:
                        self.idle_start_time = current_time
                        self.idle_timer.start()

            time.sleep(1)

    def handle_idle(self):
        self.idle_start_time = None
        self.start_time = time.time()
        self.idle_timer.cancel()

    def update_window_time(self, window_title, elapsed_time):
        if window_title in self.window_time_dict:
            self.window_time_dict[window_title] += elapsed_time
        else:
            self.window_time_dict[window_title] = elapsed_time

    def save_data_on_exit(self):
        self.stop_tracking_event.set()
        g_sheet.sent_details_to_sheet(self.window_time_dict, self.today_date)
        

        """ uncomment below code to perform save excel sheet localy """

        # user_response = tk.messagebox.askquestion("Save Report", "Do you want to save your report?")
        # if user_response == "yes":
        #     file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        #     if file_path:
        #         self.export_report(file_path)

        self.root.quit()

    def export_report(self, file_path):
        df = pd.DataFrame.from_dict(self.window_time_dict, orient='index', columns=['Total Time (s)'])
        total_hours = df['Total Time (s)'].sum() / 3600
        df.loc['Total Hour'] = [total_hours]
        df.at['Total Hour', 'Date'] = self.today_date

        # Create a new Workbook object
        workbook = Workbook()
        
        # Create a new worksheet in the Workbook
        worksheet = workbook.active
        worksheet.title = 'Time Data'
        
        # Write the DataFrame to the worksheet
        for index, row in df.iterrows():
            worksheet.append([index] + list(row))

        # Save the Workbook to the specified file path
        workbook.save(file_path)


if __name__ == "__main__":
    app = WindowTimeTracker()
    app.root.mainloop()
