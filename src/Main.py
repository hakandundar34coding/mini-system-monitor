#!/usr/bin/env python3

# Import modules
import tkinter as tk
from tkinter import ttk

from cairo import ImageSurface, Context, FORMAT_ARGB32

import PIL
from PIL import Image, ImageTk

import webbrowser

import os
import sys

from Config import Config
# Read settings
Config.config_read_func()
#from Performance import Performance



# Define class
class MainWindow:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Generate main window and configure it
        self.main_window = tk.Tk()
        self.main_window.geometry(Config.remember_window_size)
        # Disable window sizing in x and y directions.
        self.main_window.resizable(False, False)
        self.main_window.title("Mini System Monitor")
        self.application_icon = tk.PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "/../icons/mini-system-monitor.png")
        # "True" is used in order to use same wimdow icon for other windows of the application.
        self.main_window.iconphoto(True, self.application_icon)
        self.main_window.rowconfigure(0, minsize=1, weight=1)
        self.main_window.columnconfigure(0, minsize=1, weight=1)

        # Define main window GUI objects
        self.main_window_gui_objects()

        # Configuration for running function after window is shown
        self.main_window.after_idle(self.main_window_show_func)

        # Configuration for detecting if window close button (X) is clicked
        self.main_window.protocol('WM_DELETE_WINDOW', self.main_window_close_button_func)

        # Start main loop for keeping the window on the screen.
        self.main_window.mainloop()


    # ----------------------- Called by "__init__" function for generating and configuring main window GUI objects -----------------------
    def main_window_gui_objects(self):

        # Generate a frame (which will contain sub-frames on the main window) and configure it.
        frame_main = tk.Frame(self.main_window)
        frame_main.rowconfigure(1, minsize=1, weight=1)
        frame_main.columnconfigure(0, minsize=1, weight=1)
        frame_main.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Generate a frame (which will contain buttons) and configure it.
        frame_buttons = tk.Frame(frame_main)
        frame_buttons.rowconfigure(0, minsize=1, weight=1)
        frame_buttons.columnconfigure(1, minsize=1, weight=1)
        frame_buttons.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Genreate "More..." button and configure it.
        self.button1 = tk.Button(frame_buttons, text="More...", width=5, height=1, command=self.more_button_func)
        self.button1.grid(row=0, column=0, sticky="ew")

        # Genreate "Settings" button and configure it.
        self.button2 = tk.Button(frame_buttons, text="Settings", width=5, height=1, command=self.settings_button_func)
        self.button2.grid(row=0, column=1, sticky="ew")

        # Genreate "About" button.
        self.button3 = tk.Button(frame_buttons, text="About", width=5, height=1, command=self.about_button_func)
        self.button3.grid(row=0, column=2, sticky="ew")

        # Genreate a label for showing graphics on it.
        self.label1 = tk.Label(frame_main)
        self.label1.grid(row=1, column=0, sticky="nsew")

        # Define a surface for showing Cairo context on it.
        window_size = Config.remember_window_size.split("x")
        self.surface1 = ImageSurface(FORMAT_ARGB32, int(window_size[0]), int(window_size[1]))
        # Define a Cairo context for drawing graphics.
        self.context1 = Context(self.surface1)
        # Update label for showing graphics faster on start.
        self.label1.update()


    # ----------------------- Called for showing More... window -----------------------
    def more_button_func(self):

        self.more_window = MoreWindow(self.main_window)


    # ----------------------- Called for showing Settings window -----------------------
    def settings_button_func(self):

        self.settings_window = SettingsWindow(self.main_window)


    # ----------------------- Called for showing About window -----------------------
    def about_button_func(self):

        self.about_window = AboutWindow(self.main_window, self.application_icon)


    # ----------------------- Called for running code after main window is shown -----------------------
    def main_window_show_func(self):

        # Run "Performance" module in order to provide performance data to Performance tab.
        global Performance
        import Performance
        Performance = Performance.Performance(self)
        Performance.performance_background_initial_func()

        # Start loop function to run loop functions of opened tabs to get data of them.
        self.main_gui_tab_loop_func()


    # ----------------------- Called for detecting clicks on the window close button (X) and exiting the application -----------------------
    def main_window_close_button_func(self):

        # Save current size of the main window.
        main_window_size_and_position = self.main_window.geometry()
        Config.remember_window_size = main_window_size_and_position.split("+")[0]

        # Save settings to file.
        Config.config_save_func()

        # Delete main window and exit the application.
        self.main_window.destroy()
        sys.exit()


    # ----------------------- Called for running loop functions of opened tabs to get data -----------------------
    def main_gui_tab_loop_func(self):

        Performance.performance_background_loop_func()

        Performance.performance_summary_chart_draw_func()

        # Wait and run the function again in order to generate a loop. Time is defined in milliseconds (1000 ms = 1 second).
        self.main_window.after(int(Config.update_interval*1000), self.main_gui_tab_loop_func)



# Define class
class MoreWindow():

    # ----------------------- Always called when MoreWindow class is generated -----------------------
    def __init__(self, main_window):

        # Get main window of the application.
        self.main_window = main_window

        # Generate a window and configure it.
        self.window2001 = tk.Toplevel(self.main_window)
        self.window2001.wm_transient(self.main_window)                                        # "wm_transient()" is used in order to keep the about window on top of the main window.
        self.window2001.grab_set()                                                            # "grab_set()" is used in order to prevent usage of the main window.
        self.window2001.resizable(False, False)                                               # Disable window sizing in x and y directions.
        self.window2001.title("More...")

        # Define Settings window GUI objects
        self.more_window_gui_objects()


    # ----------------------- Called by "__init__" function for generating and configuring window GUI objects -----------------------
    def more_window_gui_objects(self):

        # Generate a frame and configure it.
        frame_main2001 = tk.Frame(self.window2001)
        frame_main2001.rowconfigure(0, minsize=1, weight=1)
        frame_main2001.columnconfigure(0, minsize=1, weight=1)
        frame_main2001.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Generate labels and set texts for showing application information.
        label2001 = tk.Label(frame_main2001, text="See free and open source 'System Monitoring Center' for more features.")
        label2001.grid(row=0, column=0, sticky="ns", padx=0, pady=0)

        label2002 = tk.Label(frame_main2001, text="Web Page", fg="blue", cursor="hand2")
        label2002.grid(row=1, column=0, sticky="ns", padx=0, pady=0)
        label2002.bind("<Button-1>", self.more_window_web_page_link_func)

        # Generate a label and set an image.
        self.image2001 = tk.PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "/../images/smc_screenshot1.png")
        label2001 = tk.Label(frame_main2001, image=self.image2001)
        label2001.grid(row=2, column=0, sticky="ns", padx=0, pady=0)


    # ----------------------- Called for opening project web page when relevant label is clicked -----------------------
    def more_window_web_page_link_func(self, event):

        webbrowser.open_new("https://github.com/hakandundar34coding/system-monitoring-center")



# Define class
class SettingsWindow():

    # ----------------------- Always called when SettingsWindow class is generated -----------------------
    def __init__(self, main_window):

        # Get main window of the application.
        self.main_window = main_window

        # Generate a window and configure it.
        self.window3001 = tk.Toplevel(self.main_window)
        self.window3001.wm_transient(self.main_window)                                        # "wm_transient()" is used in order to keep the about window on top of the main window.
        self.window3001.grab_set()                                                            # "grab_set()" is used in order to prevent usage of the main window.
        self.window3001.resizable(False, False)                                               # Disable window sizing in x and y directions.
        self.window3001.title("Settings")

        # Define Settings window GUI objects
        self.settings_window_gui_objects()


    # ----------------------- Called by "__init__" function for generating and configuring window GUI objects -----------------------
    def settings_window_gui_objects(self):

        # Generate a frame and configure it.
        frame_main3001 = tk.Frame(self.window3001)
        frame_main3001.rowconfigure(0, minsize=1, weight=1)
        frame_main3001.columnconfigure(0, minsize=1, weight=1)
        frame_main3001.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Generate checkbuttons and configure them.
        self.checkbutton3001_variable = tk.IntVar()
        self.checkbutton3001 = tk.Checkbutton(frame_main3001, text="Remember last selected devices", command=self.settings_remember_device_selection_func, variable=self.checkbutton3001_variable, onvalue=1, offvalue=0)
        self.checkbutton3001.grid(row=0, column=0, sticky="w")

        # Generate labels and set texts for showing application information.
        label3001 = tk.Label(frame_main3001, text="Disk")
        label3001.grid(row=4, column=0, sticky="w")
        label3002 = tk.Label(frame_main3001, text="Network")
        label3002.grid(row=5, column=0, sticky="w")

        # Generate comboboxes and configure it.
        self.combobox3001_variable = tk.StringVar()
        self.combobox3001 = ttk.Combobox(frame_main3001, textvariable=self.combobox3001_variable)
        self.combobox3001.grid(row=4, column=1, sticky="w")
        self.combobox3001['state'] = 'readonly'
        self.combobox3001.bind('<<ComboboxSelected>>', self.settings_disk_selection_func)
        disk_list = Performance.disk_list_system_ordered
        self.combobox3001['values'] = disk_list
        #self.combobox3001.set("")

        self.combobox3002_variable = tk.StringVar()
        self.combobox3002 = ttk.Combobox(frame_main3001, textvariable=self.combobox3002_variable)
        self.combobox3002.grid(row=5, column=1, sticky="w")
        self.combobox3002['state'] = 'readonly'
        self.combobox3002.bind('<<ComboboxSelected>>', self.settings_network_card_selection_func)
        network_card_list = Performance.network_card_list
        self.combobox3002['values'] = network_card_list
        #self.combobox3002.set("")

        # Set GUI objects by using user settings.
        if Config.remember_last_selected_hardware == 0:
            #self.checkbutton3001_variable = 0
            self.checkbutton3001.deselect()
        if Config.remember_last_selected_hardware == 1:
            #self.checkbutton3001_variable = 1
            self.checkbutton3001.select()
        self.combobox3002.current(Performance.selected_network_card_number)
        self.combobox3001.current(Performance.selected_disk_number)


    # ----------------------- Called for setting "Remember last selected devices" option GUI object -----------------------
    def settings_remember_device_selection_func(self):

        if self.checkbutton3001_variable.get() == 0:
            Config.remember_last_selected_hardware = 0

        if self.checkbutton3001_variable.get() == 1:
            Config.remember_last_selected_hardware = 1

        Config.config_save_func()


    # ----------------------- Called for selecting disk -----------------------
    def settings_disk_selection_func(self, event):

        selected_device = self.combobox3001.get()
        Config.selected_disk = selected_device
        Performance.performance_set_selected_disk_func()


    # ----------------------- Called for selecting network card -----------------------
    def settings_network_card_selection_func(self, event):

        selected_device = self.combobox3002.get()
        Config.selected_network_card = selected_device
        Performance.performance_set_selected_network_card_func()



# Define class
class AboutWindow():

    # ----------------------- Always called when SettingsWindow class is generated -----------------------
    def __init__(self, main_window, application_icon):

        # Get main window and icon of the application.
        self.main_window = main_window
        self.application_icon = application_icon

        # Generate a window and configure it.
        self.window1001 = tk.Toplevel(self.main_window)
        self.window1001.wm_transient(self.main_window)                                        # "wm_transient()" is used in order to keep the about window on top of the main window.
        self.window1001.grab_set()                                                            # "grab_set()" is used in order to prevent usage of the main window.
        self.window1001.resizable(False, False)                                               # Disable window sizing in x and y directions.
        self.window1001.title("About")

        # Define About window GUI objects
        self.about_window_gui_objects()


    # ----------------------- Called by "__init__" function for generating and configuring window GUI objects -----------------------
    def about_window_gui_objects(self):

        # Get software version from file.
        try:
            software_version = open(os.path.dirname(os.path.abspath(__file__)) + "/__version__").readline()
        except Exception:
            pass

        # Generate a frame and configure it.
        frame_main1001 = tk.Frame(self.window1001)
        frame_main1001.rowconfigure(0, minsize=1, weight=1)
        frame_main1001.columnconfigure(0, minsize=1, weight=1)
        frame_main1001.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        # Generate a image and set application icon.
        label1001 = tk.Label(frame_main1001, image=self.application_icon)
        label1001.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Generate labels and set texts for showing application information.
        label1002 = tk.Label(frame_main1001, text="Mini System Monitor", font=("bold"))
        label1002.grid(row=1, column=0, sticky="ns", padx=0, pady=0)

        label1002 = tk.Label(frame_main1001, text=software_version)
        label1002.grid(row=2, column=0, sticky="ns", padx=0, pady=4)

        label1003 = tk.Label(frame_main1001, text="Mini version of 'System Monitoring Center'.")
        label1003.grid(row=3, column=0, sticky="ns", padx=0, pady=5)

        label1004 = tk.Label(frame_main1001, text="Web Page", fg="blue", cursor="hand2")
        label1004.grid(row=4, column=0, sticky="ns", padx=0, pady=3)
        label1004.bind("<Button-1>", self.about_window_web_page_link_func)

        label1005 = tk.Label(frame_main1001, text="© 2022 Hakan Dündar")
        label1005.grid(row=5, column=0, sticky="ns", padx=0, pady=0)

        label1006 = tk.Label(frame_main1001, text="This program comes with absolutely no warranty.\nSee the GNU General Public License, version 3 or later for details.")
        label1006.grid(row=6, column=0, sticky="ns", padx=0, pady=5)

        label1007 = tk.Label(frame_main1001, text="GPLv3", fg="blue", cursor="hand2")
        label1007.grid(row=7, column=0, sticky="ns")
        label1007.bind("<Button-1>", self.about_window_license_link_func)


    # ----------------------- Called for opening project web page when relevant label is clicked -----------------------
    def about_window_web_page_link_func(self, event):

        webbrowser.open_new("https://github.com/hakandundar34coding/mini-system-monitor")


    # ----------------------- Called for opening license web page when relevant label is clicked -----------------------
    def about_window_license_link_func(self, event):

        webbrowser.open_new("https://www.gnu.org/licenses/gpl-3.0.html")



if __name__ == "__main__":
    # Run class
    MainWindow()

