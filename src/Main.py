#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

import cairo
from cairo import ImageSurface, Context, FORMAT_ARGB32

import PIL
from PIL import Image, ImageTk

from math import sin, cos
import webbrowser

import os
import sys


class Config:

    def __init__(self):

        self.config_default_general_general_func()


    def config_default_general_general_func(self):
        """
        Get settings.
        """

        self.selected_disk = ""
        self.selected_network_card = ""

        # Read-only settings.
        self.remember_last_selected_hardware = 0
        self.update_interval = 0.75
        self.chart_data_history = 5
        self.remember_window_size = "530x420"
        self.chart_line_color_cpu_percent = [0.29, 0.78, 0.0, 1.0]
        self.selected_cpu_core = ""
        self.chart_line_color_memory_percent = [0.27, 0.49, 1.0, 1.0]
        self.performance_memory_data_precision = 1
        self.performance_memory_data_unit = 0
        self.chart_line_color_disk_speed_usage = [1.0, 0.44, 0.17, 1.0]
        self.performance_disk_data_precision = 1
        self.performance_disk_data_unit = 0
        self.performance_disk_speed_bit = 0
        self.chart_line_color_network_speed_data = [0.56, 0.30, 0.78, 1.0]
        self.performance_network_data_precision = 1
        self.performance_network_data_unit = 0
        self.performance_network_speed_bit = 0


class MainWindow:

    def __init__(self):

        # Read settings
        global Config
        Config = Config()

        # Main window
        self.main_window = tk.Tk()
        self.main_window.geometry(Config.remember_window_size)
        # Disable window sizing in x and y directions.
        self.main_window.resizable(False, False)
        self.main_window.title("Mini System Monitor")
        self.application_icon = tk.PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "/../icons/mini-system-monitor.png")
        # "True" is used in order to use same window icon for other windows of the application.
        self.main_window.iconphoto(True, self.application_icon)
        self.main_window.rowconfigure(0, minsize=1, weight=1)
        self.main_window.columnconfigure(0, minsize=1, weight=1)

        # Main window GUI objects
        self.main_window_gui_objects()

        # Run function after window is shown
        self.main_window.after_idle(self.main_window_show_func)

        # Run function if window close button (X) is clicked
        self.main_window.protocol('WM_DELETE_WINDOW', self.main_window_close_button_func)

        # Start main loop for keeping the window on the screen.
        self.main_window.mainloop()


    def main_window_gui_objects(self):
        """
        Main window GUI objects
        """

        # Main Frame
        frame_main = tk.Frame(self.main_window)
        frame_main.rowconfigure(1, minsize=1, weight=1)
        frame_main.columnconfigure(0, minsize=1, weight=1)
        frame_main.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Frame (buttons)
        frame_buttons = tk.Frame(frame_main)
        frame_buttons.rowconfigure(0, minsize=1, weight=1)
        frame_buttons.columnconfigure(1, minsize=1, weight=1)
        frame_buttons.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Button (More...)
        self.button1 = tk.Button(frame_buttons, text="More...", width=5, height=1, command=self.more_button_func)
        self.button1.grid(row=0, column=0, sticky="ew")

        # Button (Settings)
        self.button2 = tk.Button(frame_buttons, text="Settings", width=5, height=1, command=self.settings_button_func)
        self.button2.grid(row=0, column=1, sticky="ew")

        # Button (About)
        self.button3 = tk.Button(frame_buttons, text="About", width=5, height=1, command=self.about_button_func)
        self.button3.grid(row=0, column=2, sticky="ew")

        # Label (for showing graphics)
        self.label1 = tk.Label(frame_main)
        self.label1.grid(row=1, column=0, sticky="nsew")

        # Surface (for showing Cairo context)
        window_size = Config.remember_window_size.split("x")
        self.surface1 = ImageSurface(FORMAT_ARGB32, int(window_size[0]), int(window_size[1]))
        # Cairo Context (for drawing graphics)
        self.context1 = Context(self.surface1)
        # Update label for showing graphics faster on start.
        self.label1.update()


    def more_button_func(self):
        """
        Show "More..." window.
        """

        self.more_window = MoreWindow(self.main_window)


    def settings_button_func(self):
        """
        Show "Settings" window.
        """

        self.settings_window = SettingsWindow(self.main_window)


    def about_button_func(self):
        """
        Show "About" window.
        """

        self.about_window = AboutWindow(self.main_window, self.application_icon)


    def main_window_show_func(self):
        """
        Run code after the main window is shown.
        """

        # Run "Performance" module in order to provide performance data to Performance tab.
        global Performance
        Performance = Performance(self)
        Performance.performance_background_initial_func()

        # Start loop function
        self.main_gui_tab_loop_func()


    def main_window_close_button_func(self):
        """
        Detect clicks on the window close button (X) and exit the application.
        """

        # Save current size of the main window.
        main_window_size_and_position = self.main_window.geometry()
        Config.remember_window_size = main_window_size_and_position.split("+")[0]

        # Delete main window and exit the application.
        self.main_window.destroy()
        sys.exit()


    def main_gui_tab_loop_func(self):
        """
        Repeat running the functions.
        """

        Performance.performance_background_loop_func()

        Performance.performance_summary_chart_draw_func()

        # Wait and run the function again in order to generate a loop. Time is defined in milliseconds (1000 ms = 1 second).
        self.main_window.after(int(Config.update_interval*1000), self.main_gui_tab_loop_func)


class MoreWindow():

    def __init__(self, main_window):

        self.main_window = main_window

        # Window (More...)
        self.window2001 = tk.Toplevel(self.main_window)
        self.window2001.wm_transient(self.main_window)                                        # "wm_transient()" is used in order to keep the about window on top of the main window.
        self.window2001.grab_set()                                                            # "grab_set()" is used in order to prevent usage of the main window.
        self.window2001.resizable(False, False)                                               # Disable window sizing in x and y directions.
        self.window2001.title("More...")

        # "More..." window GUI objects
        self.more_window_gui_objects()


    def more_window_gui_objects(self):
        """
        More window GUI objects
        """

        # Main Frame
        frame_main2001 = tk.Frame(self.window2001)
        frame_main2001.rowconfigure(0, minsize=1, weight=1)
        frame_main2001.columnconfigure(0, minsize=1, weight=1)
        frame_main2001.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Labels
        label2001 = tk.Label(frame_main2001, text="See free and open source 'System Monitoring Center' for more features.")
        label2001.grid(row=0, column=0, sticky="ns", padx=0, pady=0)

        label2002 = tk.Label(frame_main2001, text="Web Page", fg="blue", cursor="hand2")
        label2002.grid(row=1, column=0, sticky="ns", padx=0, pady=0)
        label2002.bind("<Button-1>", self.more_window_web_page_link_func)

        # Label (for showing image)
        self.image2001 = tk.PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) + "/../images/smc_screenshot1.png")
        label2001 = tk.Label(frame_main2001, image=self.image2001)
        label2001.grid(row=2, column=0, sticky="ns", padx=0, pady=0)


    def more_window_web_page_link_func(self, event):
        """
        Open the link in a web browser.
        """

        webbrowser.open_new("https://github.com/hakandundar34coding/system-monitoring-center")


class SettingsWindow():

    def __init__(self, main_window):

        self.main_window = main_window

        # Window (Settings)
        self.window3001 = tk.Toplevel(self.main_window)
        self.window3001.wm_transient(self.main_window)                                        # "wm_transient()" is used in order to keep the about window on top of the main window.
        self.window3001.grab_set()                                                            # "grab_set()" is used in order to prevent usage of the main window.
        self.window3001.resizable(False, False)                                               # Disable window sizing in x and y directions.
        self.window3001.title("Settings")

        # "Settings" window GUI objects
        self.settings_window_gui_objects()


    def settings_window_gui_objects(self):
        """
        Settings window GUI objects
        """

        # Main Frame
        frame_main3001 = tk.Frame(self.window3001)
        frame_main3001.rowconfigure(0, minsize=1, weight=1)
        frame_main3001.columnconfigure(0, minsize=1, weight=1)
        frame_main3001.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Labels
        label3001 = tk.Label(frame_main3001, text="Disk")
        label3001.grid(row=0, column=0, sticky="w")
        label3002 = tk.Label(frame_main3001, text="Network Card")
        label3002.grid(row=1, column=0, sticky="w")

        # Comboboxes
        self.combobox3001_variable = tk.StringVar()
        self.combobox3001 = ttk.Combobox(frame_main3001, textvariable=self.combobox3001_variable)
        self.combobox3001.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.combobox3001['state'] = 'readonly'
        self.combobox3001.bind('<<ComboboxSelected>>', self.settings_disk_selection_func)
        disk_list = Performance.disk_list_system_ordered
        self.combobox3001['values'] = disk_list
        #self.combobox3001.set("")

        self.combobox3002_variable = tk.StringVar()
        self.combobox3002 = ttk.Combobox(frame_main3001, textvariable=self.combobox3002_variable)
        self.combobox3002.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.combobox3002['state'] = 'readonly'
        self.combobox3002.bind('<<ComboboxSelected>>', self.settings_network_card_selection_func)
        network_card_list = Performance.network_card_list
        self.combobox3002['values'] = network_card_list
        #self.combobox3002.set("")

        # Set GUI objects by using user settings.
        self.combobox3002.current(Performance.selected_network_card_number)
        self.combobox3001.current(Performance.selected_disk_number)


    def settings_disk_selection_func(self, event):
        """
        Select disk.
        """

        selected_device = self.combobox3001.get()
        Config.selected_disk = selected_device
        Performance.performance_set_selected_disk_func()


    def settings_network_card_selection_func(self, event):
        """
        Select network card.
        """

        selected_device = self.combobox3002.get()
        Config.selected_network_card = selected_device
        Performance.performance_set_selected_network_card_func()



class AboutWindow():

    def __init__(self, main_window, application_icon):

        # Get main window and icon of the application.
        self.main_window = main_window
        self.application_icon = application_icon

        # Window (About)
        self.window1001 = tk.Toplevel(self.main_window)
        self.window1001.wm_transient(self.main_window)                                        # "wm_transient()" is used in order to keep the about window on top of the main window.
        self.window1001.grab_set()                                                            # "grab_set()" is used in order to prevent usage of the main window.
        self.window1001.resizable(False, False)                                               # Disable window sizing in x and y directions.
        self.window1001.title("About")

        # "About" window GUI objects
        self.about_window_gui_objects()


    def about_window_gui_objects(self):
        """
        Settings window GUI objects
        """

        # Get software version
        try:
            software_version = open(os.path.dirname(os.path.abspath(__file__)) + "/__version__").readline()
        except Exception:
            pass

        # Main Frame
        frame_main1001 = tk.Frame(self.window1001)
        frame_main1001.rowconfigure(0, minsize=1, weight=1)
        frame_main1001.columnconfigure(0, minsize=1, weight=1)
        frame_main1001.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        # Image
        label1001 = tk.Label(frame_main1001, image=self.application_icon)
        label1001.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Labels
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


    def about_window_web_page_link_func(self, event):
        """
        Open the link in a web browser.
        """

        webbrowser.open_new("https://github.com/hakandundar34coding/mini-system-monitor")


    def about_window_license_link_func(self, event):
        """
        Open the link in a web browser.
        """

        webbrowser.open_new("https://www.gnu.org/licenses/gpl-3.0.html")


class Performance:

    def __init__(self, MainWindow):

        self.performance_define_data_unit_converter_variables_func()

        self.MainWindow = MainWindow


    def performance_set_selected_disk_func(self):
        """
        Set selected disk.
        """

        # Set selected disk
        with open("/proc/mounts") as reader:
            proc_mounts_output_lines = reader.read().strip().split("\n")
        system_disk_list = []
        for line in proc_mounts_output_lines:
            line_split = line.split(" ", 2)
            if line_split[1].strip() == "/":
                disk = line_split[0].strip().split("/")[-1]
                # "/dev/root" disk is not listed in "/proc/partitions" file.
                if disk in self.disk_list:
                    system_disk_list.append(disk)
                    break
        # Detect system disk by checking if mount point is "/" on some systems such as some ARM devices. "/dev/root" is the system disk name (symlink) in the "/proc/mounts" file on these systems.
        if system_disk_list == []:
            with open("/proc/cmdline") as reader:
                proc_cmdline = reader.read()
            if "root=UUID=" in proc_cmdline:
                disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
                system_disk_list.append(os.path.realpath(f'/dev/disk/by-uuid/{disk_uuid_partuuid}').split("/")[-1].strip())
            if "root=PARTUUID=" in proc_cmdline:
                disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
                system_disk_list.append(os.path.realpath(f'/dev/disk/by-partuuid/{disk_uuid_partuuid}').split("/")[-1].strip())

        if Config.selected_disk in self.disk_list:
            selected_disk = Config.selected_disk
        else:
            if system_disk_list != []:
                selected_disk = system_disk_list[0]
            else:
                selected_disk = self.disk_list[0]
                # Try to not to set selected disk a loop, ram, zram disk in order to avoid errors if "hide_loop_ramdisk_zram_disks" option is enabled and performance data of all disks are plotted at the same time. loop device may be the first disk on some systems if they are run without installation.
                for disk in self.disk_list:
                    if disk.startswith("loop") == False and disk.startswith("ram") == False and disk.startswith("zram") == False:
                        selected_disk = disk
                        break

        self.system_disk_list = system_disk_list
        self.selected_disk_number = self.disk_list_system_ordered.index(selected_disk)


    def performance_set_selected_network_card_func(self):
        """
        Set selected network card.
        """

        # Set selected network card
        connected_network_card_list = []
        for network_card in self.network_card_list:
            with open(f'/sys/class/net/{network_card}/operstate') as reader:
                sys_class_net_output = reader.read().strip()
            if sys_class_net_output == "up":
                connected_network_card_list.append(network_card)
        # Avoid errors if there is no any network card that connected.
        if connected_network_card_list != []:
            selected_network_card = connected_network_card_list[0]
        else:
            selected_network_card = self.network_card_list[0]
        # "" is predefined network card name before release of the software. This statement is used in order to avoid error, if no network card selection is made since first run of the software.
        if Config.selected_network_card == "":
            selected_network_card_number = self.network_card_list.index(selected_network_card)
        if Config.selected_network_card in self.network_card_list:
            selected_network_card_number = self.network_card_list.index(Config.selected_network_card)
        else:
            selected_network_card_number = self.network_card_list.index(selected_network_card)

        # Definition to access to this variable from other modules.
        self.selected_network_card_number = selected_network_card_number


    def performance_background_initial_func(self):
        """
        Performance initial function.
        """

        self.chart_data_history = Config.chart_data_history

        # Define initial values for CPU usage percent
        self.logical_core_list = []
        self.cpu_time_all_prev = []
        self.cpu_time_load_prev = []
        self.cpu_usage_percent_per_core = []
        self.cpu_usage_percent_ave = [0] * self.chart_data_history

        # Define initial values for RAM usage percent and swap usage percent
        self.ram_usage_percent = [0] * self.chart_data_history
        self.swap_usage_percent = [0] * self.chart_data_history

        # Define initial values for disk read speed and write speed
        # Disk data from /proc/diskstats are multiplied by 512 in order to find values in the form of byte. Disk sector size for all disk device could be found in "/sys/block/[disk device name such as sda]/queue/hw_sector_size". Linux uses 512 value for all disks without regarding device real block size (source: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/types.h?id=v4.4-rc6#n121).
        self.disk_sector_size = 512
        self.disk_list = []
        self.disk_read_data_prev = []
        self.disk_write_data_prev = []
        self.disk_read_speed = []
        self.disk_write_speed = []

        # Define initial values for network receive speed and network send speed
        self.network_card_list = []
        self.network_receive_bytes_prev = []
        self.network_send_bytes_prev =[]
        self.network_receive_speed = []
        self.network_send_speed = []

        # Reset selected hardware if "remember_last_selected_hardware" prefrence is disabled by the user.
        if Config.remember_last_selected_hardware == 0:
            Config.selected_cpu_core = ""
            Config.selected_disk = ""
            Config.selected_network_card = ""


    def performance_background_loop_func(self):
        """
        Performance loop function.
        Get CPU, memory, disk and network usage data.
        """

        # Definition for lower CPU usage because this variable is used multiple times in this function.
        update_interval = Config.update_interval

        # Get CPU core list
        self.logical_core_list_system_ordered = []                                            # "logical_core_list_system_ordered" contains online CPU core numbers in the order of "/proc/stats" file content which is in "ascending" online core number order.
        with open("/proc/stat") as reader:                                                    # "/proc/stat" file contains online logical CPU core numbers (all cores without regarding CPU sockets, physical/logical cores) and CPU times since system boot.
            proc_stat_lines = reader.read().split("intr", 1)[0].strip().split("\n")[1:]       # Trimmed unneeded information in the file
        for line in proc_stat_lines:
            self.logical_core_list_system_ordered.append(line.split(" ", 1)[0])               # Add CPU core names into a temporary list in ascending core number order. This list will be used with logical_core_list in order to track last online-made CPU core. This operations are performed in order to track CPU usage per core continuously even if CPU cores made online/offline.
        self.number_of_logical_cores = len(self.logical_core_list_system_ordered)             # "logical_core_list" list contains online CPU core numbers and ordering changes when online/offline CPU core changes are made. Last online-made core is listed as the last core.
        logical_core_list_prev = self.logical_core_list[:]                                    # Get copy of the list. Otherwise, lists will be linked.
        for i, cpu_core in enumerate(self.logical_core_list_system_ordered):                  # Track the changes if CPU core is made online/offline
            if cpu_core not in self.logical_core_list:                                        # Add new core number into logical_core_list if CPU core is made online. Also CPU time data related to online-made the core is appended into lists.
                self.logical_core_list.append(cpu_core)
                cpu_time = proc_stat_lines[i].split()
                self.cpu_time_all_prev.append(int(cpu_time[1]) + int(cpu_time[2]) + int(cpu_time[3]) + int(cpu_time[4]) + int(cpu_time[5]) + int(cpu_time[6]) + int(cpu_time[7]) + int(cpu_time[8]) + int(cpu_time[9]))
                self.cpu_time_load_prev.append(self.cpu_time_all_prev[-1] - int(cpu_time[4]) - int(cpu_time[5]))
                self.cpu_usage_percent_per_core.append([0] * self.chart_data_history)
        for cpu_core in self.logical_core_list[:]:                                            # Remove core number from logical_core_list if it is made offline. Also CPU time data related to offline-made the core is removed from lists.
            if cpu_core not in self.logical_core_list_system_ordered:
                cpu_core_index_to_remove = self.logical_core_list.index(cpu_core)
                del self.cpu_time_all_prev[cpu_core_index_to_remove]
                del self.cpu_time_load_prev[cpu_core_index_to_remove]
                del self.cpu_usage_percent_per_core[cpu_core_index_to_remove]
                self.logical_core_list.remove(cpu_core)
        if logical_core_list_prev != self.logical_core_list:
            pass
        # Get cpu_usage_percent_per_core, cpu_usage_percent_ave
        cpu_time_all = []
        cpu_time_load = []
        for i, cpu_core in enumerate(self.logical_core_list):                                 # Get CPU core times calculate CPU usage values and append usage values into lists in the core number order listed in logical_core_list.
            cpu_time = proc_stat_lines[self.logical_core_list_system_ordered.index(cpu_core)].split()
            cpu_time_all.append(int(cpu_time[1]) + int(cpu_time[2]) + int(cpu_time[3]) + int(cpu_time[4]) + int(cpu_time[5]) + int(cpu_time[6]) + int(cpu_time[7]) + int(cpu_time[8]) + int(cpu_time[9]))    # All time since boot for the cpu core
            cpu_time_load.append(cpu_time_all[-1] - int(cpu_time[4]) - int(cpu_time[5]))      # Time elapsed during core processing for the core
            if cpu_time_all[-1] - self.cpu_time_all_prev[i] == 0:
                cpu_time_all[-1] = cpu_time_all[-1] + 1                                       # Append 1 CPU time (a negligible value) in order to avoid zeor division error in the first loop after application start or in the first loop of newly online-made CPU core. It is corrected in the next loop.
            self.cpu_usage_percent_per_core[i].append((cpu_time_load[-1] - self.cpu_time_load_prev[i]) / (cpu_time_all[-1] - self.cpu_time_all_prev[i]) * 100)
            del self.cpu_usage_percent_per_core[i][0]
        cpu_usage_average = []
        for cpu_usage_per_core in self.cpu_usage_percent_per_core:
            cpu_usage_average.append(cpu_usage_per_core[-1])
        self.cpu_usage_percent_ave.append(sum(cpu_usage_average) / self.number_of_logical_cores)    # Calculate average CPU usage for all logical cores (summation of CPU usage per core / number of logical cores)
        del self.cpu_usage_percent_ave[0]                                                     # Delete the first CPU usage percent value from the list in order to keep list lenght same. Because a new value is appended in every loop. This list is used for CPU usage percent graphic.        
        self.cpu_time_all_prev = list(cpu_time_all)                                           # Use the values as "previous" data. This data will be used in the next loop for calculating time difference.
        self.cpu_time_load_prev = list(cpu_time_load)

        # Get ram_usage_percent
        with open("/proc/meminfo") as reader:
            memory_info = reader.read()
        self.ram_total = int(memory_info.split("MemTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        self.ram_free = int(memory_info.split("\nMemFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        self.ram_available = int(memory_info.split("\nMemAvailable:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        self.ram_used = self.ram_total - self.ram_available
        self.ram_usage_percent.append(self.ram_used / self.ram_total * 100)
        del self.ram_usage_percent[0]
        # Get swap_usage_percent
        self.swap_total = int(memory_info.split("\nSwapTotal:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        self.swap_free = int(memory_info.split("\nSwapFree:", 1)[1].split("\n", 1)[0].split(" ")[-2].strip()) *1024
        # Calculate values if swap memory exists.
        if self.swap_free != 0:
            self.swap_used = self.swap_total - self.swap_free
            self.swap_usage_percent.append(self.swap_used / self.swap_total * 100)
        # Set values as "0" if swap memory does not exist.
        else:
            self.swap_used = 0
            self.swap_usage_percent.append(0)
        del self.swap_usage_percent[0]

        # Get disk_list
        self.disk_list_system_ordered = []
        proc_diskstats_lines_filtered = []
        with open("/proc/partitions") as reader:
            proc_partitions_lines = reader.read().strip().split("\n")[2:]
        for line in proc_partitions_lines:
            self.disk_list_system_ordered.append(line.split()[3].strip())
        with open("/proc/diskstats") as reader:
            proc_diskstats_lines = reader.read().strip().split("\n")
        for line in proc_diskstats_lines:
            if line.split()[2] in self.disk_list_system_ordered:
                # Disk information of some disks (such a loop devices) exist in "/proc/diskstats" file even if these devices are unmounted. "proc_diskstats_lines_filtered" list is used in order to use disk list without these remaining information.
                proc_diskstats_lines_filtered.append(line)
        disk_list_prev = self.disk_list[:]
        for i, disk in enumerate(self.disk_list_system_ordered):
            if disk not in self.disk_list:
                self.disk_list.append(disk)
                disk_data = proc_diskstats_lines[i].split()
                disk_read_data = int(disk_data[5]) * self.disk_sector_size
                disk_write_data = int(disk_data[9]) * self.disk_sector_size
                self.disk_read_data_prev.append(disk_read_data)
                self.disk_write_data_prev.append(disk_write_data)
                self.disk_read_speed.append([0] * self.chart_data_history)
                self.disk_write_speed.append([0] * self.chart_data_history)
        for disk in reversed(self.disk_list[:]):
            if disk not in self.disk_list_system_ordered:
                disk_index_to_remove = self.disk_list.index(disk)
                del self.disk_read_data_prev[disk_index_to_remove]
                del self.disk_write_data_prev[disk_index_to_remove]
                del self.disk_read_speed[disk_index_to_remove]
                del self.disk_write_speed[disk_index_to_remove]
                self.disk_list.remove(disk)
        if disk_list_prev != self.disk_list:
            self.performance_set_selected_disk_func()
        # Get disk_read_speed, disk_write_speed
        self.disk_read_data = []
        self.disk_write_data = []
        for i, disk in enumerate(self.disk_list):
            disk_data = proc_diskstats_lines_filtered[self.disk_list_system_ordered.index(disk)].split()
            self.disk_read_data.append(int(disk_data[5]) * self.disk_sector_size)
            self.disk_write_data.append(int(disk_data[9]) * self.disk_sector_size)
            self.disk_read_speed[i].append((self.disk_read_data[-1] - self.disk_read_data_prev[i]) / update_interval)
            self.disk_write_speed[i].append((self.disk_write_data[-1] - self.disk_write_data_prev[i]) / update_interval)
            del self.disk_read_speed[i][0]
            del self.disk_write_speed[i][0]
        self.disk_read_data_prev = list(self.disk_read_data)
        self.disk_write_data_prev = list(self.disk_write_data)

        # Get network card list
        self.network_card_list_system_ordered = []
        with open("/proc/net/dev") as reader:
            proc_net_dev_lines = reader.read().strip().split("\n")[2:]
        for line in proc_net_dev_lines:
            self.network_card_list_system_ordered.append(line.split(":", 1)[0].strip())
        network_card_list_prev = self.network_card_list[:]
        for i, network_card in enumerate(self.network_card_list_system_ordered):
            if network_card not in self.network_card_list:
                self.network_card_list.append(network_card)
                network_data = proc_net_dev_lines[i].split()
                self.network_receive_bytes = int(network_data[1])
                self.network_send_bytes = int(network_data[9])
                self.network_receive_bytes_prev.append(self.network_receive_bytes)
                self.network_send_bytes_prev.append(self.network_send_bytes)
                self.network_receive_speed.append([0] * self.chart_data_history)
                self.network_send_speed.append([0] * self.chart_data_history)
        for network_card in reversed(self.network_card_list[:]):
            if network_card not in self.network_card_list_system_ordered:
                network_card_index_to_remove = self.network_card_list.index(network_card)
                del self.network_receive_bytes_prev[network_card_index_to_remove]
                del self.network_send_bytes_prev[network_card_index_to_remove]
                del self.network_receive_speed[network_card_index_to_remove]
                del self.network_send_speed[network_card_index_to_remove]
                self.network_card_list.remove(network_card)
        if network_card_list_prev != self.network_card_list:
            self.performance_set_selected_network_card_func()
        # Get network_receive_speed, network_send_speed
        self.network_receive_bytes = []
        self.network_send_bytes = []
        for i, network_card in enumerate(self.network_card_list):
            network_data = proc_net_dev_lines[self.network_card_list_system_ordered.index(network_card)].split()
            self.network_receive_bytes.append(int(network_data[1]))
            self.network_send_bytes.append(int(network_data[9]))
            self.network_receive_speed[i].append((self.network_receive_bytes[-1] - self.network_receive_bytes_prev[i]) / update_interval)
            self.network_send_speed[i].append((self.network_send_bytes[-1] - self.network_send_bytes_prev[i]) / update_interval)
            del self.network_receive_speed[i][0]
            del self.network_send_speed[i][0]
        self.network_receive_bytes_prev = list(self.network_receive_bytes)
        self.network_send_bytes_prev = list(self.network_send_bytes)


    def performance_summary_chart_draw_func(self):
        """
        Draw graphics.
        """

        # Get widgets from MainWindow.
        widget = self.MainWindow.label1
        ctx = self.MainWindow.context1
        surface1 = self.MainWindow.surface1

        # Get drawingarea size.
        widget.update()
        chart_width = widget.winfo_width()
        chart_height = widget.winfo_height()

        surface1 = ImageSurface(FORMAT_ARGB32, chart_width, chart_height)
        ctx = Context(surface1)

        # Get chart colors of performance tab sub-tab charts.
        chart_line_color_cpu_percent = Config.chart_line_color_cpu_percent
        chart_line_color_memory_percent = Config.chart_line_color_memory_percent
        chart_line_color_disk_speed_usage = Config.chart_line_color_disk_speed_usage
        chart_line_color_network_speed_data = Config.chart_line_color_network_speed_data

        # Get performance data and set text format.
        performance_cpu_usage_percent_precision = 0
        cpu_usage_text = f'{self.cpu_usage_percent_ave[-1]:.{performance_cpu_usage_percent_precision}f}'
        performance_memory_data_precision = 0
        ram_usage_text = f'{self.ram_usage_percent[-1]:.{performance_memory_data_precision}f}'
        processes_number_text = self.cpu_system_up_time_func()
        swap_usage_text = f'{self.swap_usage_percent[-1]:.0f}%'
        selected_disk_number = self.selected_disk_number
        performance_disk_data_precision = 1
        performance_disk_data_unit = Config.performance_disk_data_unit
        performance_disk_speed_bit = Config.performance_disk_speed_bit
        disk_read_speed_text = f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, self.disk_read_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s'
        disk_write_speed_text = f'{self.performance_data_unit_converter_func("speed", performance_disk_speed_bit, self.disk_write_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s'
        selected_network_card_number = self.selected_network_card_number
        performance_network_data_precision = 1
        performance_network_data_unit = Config.performance_network_data_unit
        performance_network_speed_bit = Config.performance_network_speed_bit
        network_download_speed_text = f'{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, self.network_receive_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s'
        network_upload_speed_text = f'{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, self.network_send_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s'


        # Set antialiasing level as "BEST" in order to avoid low quality chart line because of the highlight effect (more than one line will be overlayed for this appearance).
        ctx.set_antialias(cairo.Antialias.BEST)

        # Set line joining style as "LINE_JOIN_ROUND" in order to avoid spikes at the line joints due to high antialiasing level.
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        # Define pi number
        pi_number = 3.14159


        # Get biggest outer frame size. Aspect ratio of this frame is fixed in order to avoid changing aspect ratio of the drawn objects when window size is changed.
        if chart_width > chart_height * 1.384:
            frame_width = chart_height * 1.384
            frame_height = chart_height
        else:
            frame_width = chart_width
            frame_height = chart_width / 1.384


        # Define dimensions, locations, etc. to use them for scalable graphics.
        gauge_outer_radius = frame_height * 0.43
        gauge_circular_center_x = chart_width / 2 - gauge_outer_radius * 0.48
        gauge_inner_radius = gauge_outer_radius * 0.57
        background_upper_lower_band_height = chart_height * 0.1
        background_upper_lower_band_vertex = chart_height * 0.15
        background_upper_lower_band_vertex_width = gauge_outer_radius * 2.26
        shadow_radius = gauge_outer_radius * 0.8
        shadow_center_loc_y = frame_height * 0.485
        gauge_indicator_line_major_thickness = gauge_outer_radius * 0.02
        gauge_indicator_line_minor_thickness = gauge_outer_radius * 0.01
        gauge_indicator_line_major_length = gauge_outer_radius * 0.04
        gauge_indicator_line_minor_length = gauge_outer_radius * 0.026
        gauge_indicator_line_major_move = gauge_outer_radius * 0.053
        gauge_indicator_line_minor_move = gauge_outer_radius * 0.063
        gauge_indicator_text_radius = gauge_outer_radius * 0.73
        gauge_indicator_text_correction = gauge_outer_radius * 0.047
        gauge_indicator_text_move = gauge_outer_radius * 0.027
        gauge_indicator_text_size = gauge_outer_radius * 0.091
        gauge_indicator_text_size_smaller = gauge_indicator_text_size * 0.78
        gauge_cpu_ram_label_text_move = gauge_outer_radius * 0.266
        gauge_cpu_ram_label_text_margin = gauge_outer_radius * 0.07
        gauge_cpu_ram_usage_text_size = gauge_outer_radius * 0.25
        gauge_cpu_ram_usage_text_shadow_move = gauge_outer_radius * 0.014
        gauge_cpu_ram_usage_text_move = gauge_outer_radius * 0.026
        gauge_percentage_label_text_below_cpu_ram_move = gauge_outer_radius * 0.074
        gauge_percentage_label_text_below_cpu_ram_size = gauge_outer_radius * 0.08
        gauge_processes_swap_label_text_size = gauge_indicator_text_size * 0.88
        gauge_processes_swap_label_text_move = gauge_outer_radius * 0.22
        gauge_processes_swap_usage_text_size = gauge_cpu_ram_usage_text_size * 0.45
        gauge_processes_swap_usage_text_move = gauge_outer_radius * 0.34
        gauge_processes_swap_usage_text_shadow_move = gauge_cpu_ram_usage_text_shadow_move * 0.5
        gauge_separator_line_vertical_center_length = gauge_outer_radius * 0.94
        gauge_separator_line_vertical_upper_start = gauge_outer_radius * 0.83
        gauge_separator_line_vertical_upper_length = gauge_outer_radius * 0.23
        gauge_separator_line_vertical_lower_start = gauge_outer_radius * 0.6
        gauge_separator_line_vertical_lower_length = gauge_outer_radius * 0.23
        gauge_right_outer_radius = gauge_outer_radius * 1.05
        gauge_right_move = gauge_outer_radius * 0.938
        gauge_right_upper_lower_edge_thickness = gauge_outer_radius * 0.07
        gauge_right_upper_lower_edge_move_horizontal = gauge_right_outer_radius * 0.027
        gauge_separator_line_horizontal_start = gauge_outer_radius * 0.23
        gauge_separator_line_horizontal_length = gauge_outer_radius * 0.6
        gauge_disk_network_label_text_size = gauge_indicator_text_size * 0.88
        gauge_disk_read_speed_label_text_move_x = gauge_outer_radius * 0.09
        gauge_disk_read_speed_label_text_move_y = gauge_outer_radius * 0.5
        gauge_disk_write_speed_label_text_move_x = gauge_outer_radius * 0.21
        gauge_disk_write_speed_label_text_move_y = gauge_outer_radius * 0.2
        gauge_network_download_speed_label_text_move_x = gauge_outer_radius * 0.21
        gauge_network_download_speed_label_text_move_y = gauge_outer_radius * 0.15
        gauge_network_upload_speed_label_text_move_x = gauge_outer_radius * 0.09
        gauge_network_upload_speed_label_text_move_y = gauge_outer_radius * 0.43
        gauge_disk_network_usage_text_size = gauge_cpu_ram_usage_text_size * 0.4
        gauge_disk_network_usage_text_shadow_move = gauge_outer_radius * 0.009
        gauge_disk_network_usage_text_move_y = gauge_outer_radius * 0.11


        # Save current (default) transformations (translation, rotation, scale, color, line thickness, etc.) to restore back.
        ctx.save()

        # Draw and fill chart background.
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.set_source_rgba(44/255, 60/255, 73/255, 1.0)
        ctx.fill()


        # Draw background upper band.
        ctx.move_to(0, 0)
        ctx.rel_line_to(0, (chart_height - frame_height) / 2)
        ctx.rel_line_to(0, background_upper_lower_band_height)
        ctx.rel_line_to((chart_width - frame_width) / 2, 0)
        ctx.rel_line_to(background_upper_lower_band_vertex_width / 2, background_upper_lower_band_vertex - background_upper_lower_band_height)
        ctx.rel_line_to(background_upper_lower_band_vertex_width / 2, -(background_upper_lower_band_vertex - background_upper_lower_band_height))
        ctx.rel_line_to(frame_width - background_upper_lower_band_vertex_width, 0)
        ctx.rel_line_to((chart_width - frame_width) / 2, 0)
        ctx.rel_line_to(0, -background_upper_lower_band_height)
        ctx.rel_line_to(0, -(chart_height - frame_height) / 2)
        ctx.rel_line_to(-chart_width, 0)
        ctx.close_path()
        background_upper_lower_band_path = ctx.copy_path()
        gradient_pattern = cairo.LinearGradient(0, (chart_height - frame_height) / 2 + background_upper_lower_band_height * 0.66, 0, (chart_height - frame_height) / 2 + background_upper_lower_band_vertex)
        gradient_pattern.add_color_stop_rgba(0, 80/255, 107/255, 137/255, 1)
        gradient_pattern.add_color_stop_rgba(0.10, 85/255, 117/255, 147/255, 1)
        gradient_pattern.add_color_stop_rgba(0.55, 110/255, 187/255, 197/255, 1)
        gradient_pattern.add_color_stop_rgba(0.70, 149/255, 236/255, 251/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 179/255, 236/255, 240/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()

        # Flip (scale), rotate and translate the copied background upper band and draw background lower band.
        ctx.scale(-1, 1)
        ctx.translate(0, chart_height)
        ctx.rotate(180*pi_number/180)
        ctx.append_path(background_upper_lower_band_path)
        ctx.set_source(gradient_pattern)
        ctx.fill()

        # Restore current (default) transformations (translation, rotation, scale, etc.)
        ctx.restore()


        # Translate, rotate and scale coordinate system and draw shadow of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, (chart_height / 2) + shadow_center_loc_y)
        ctx.scale(1, 0.25)
        ctx.arc(0, 0, shadow_radius, 2*pi_number*0.5, 0)
        gradient_pattern = cairo.LinearGradient(0, -shadow_radius/2, 0, 0)
        gradient_pattern.add_color_stop_rgba(0, 50/255, 50/255, 50/255, 0.55)
        gradient_pattern.add_color_stop_rgba(1, 50/255, 50/255, 50/255, 0)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        # Restore default transformations.
        ctx.restore()


        # Draw rectangle part of the background of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90+40)*pi_number/180
        ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
        angle1 = (90-40)*pi_number/180
        ctx.line_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -2*gauge_right_outer_radius*cos(angle1))
        ctx.set_source_rgba(34/255, 52/255, 71/255, 1)
        ctx.fill()
        ctx.restore()


        # Draw circular (partial) part of the background and edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = -40*pi_number/180
        end_angle = 40*pi_number/180

        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        # Draw upper edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90+40)*pi_number/180
        # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
        ctx.move_to(gauge_right_outer_radius*sin(angle1)-gauge_right_upper_lower_edge_move_horizontal, gauge_right_outer_radius*cos(angle1))
        ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)+gauge_right_outer_radius, 0, gauge_right_outer_radius*cos(angle1))
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw lower edge of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        angle1 = (90-40)*pi_number/180
        # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
        ctx.move_to(gauge_right_outer_radius*sin(angle1)-gauge_right_upper_lower_edge_move_horizontal, gauge_right_outer_radius*cos(angle1))
        ctx.rel_move_to(0, -gauge_right_outer_radius*0.07)
        ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
        ctx.rel_line_to(-gauge_right_outer_radius, 0)
        ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)-gauge_right_outer_radius, 0, gauge_right_outer_radius*cos(angle1))
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.93, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.95, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.99, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw fillet on the connection point of the upper right corner of the right gauge for continuous gauge edge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = -90*pi_number/180
        end_angle = -55*pi_number/180
        angle1 = (90-40)*pi_number/180
        ctx.translate(gauge_right_outer_radius*sin(angle1), -gauge_right_outer_radius*cos(angle1))
        ctx.translate(-gauge_right_outer_radius*0.03, gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius*0.07)
        scale_value = 1-0.93
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba((0.93 - 0.93) / scale_value, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba((0.94 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.95 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba((0.98 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.99 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius*0.07, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        # Draw fillet on the connection point of the lower right corner of the right gauge for continuous gauge edge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        start_angle = 55*pi_number/180
        end_angle = 90*pi_number/180
        angle1 = (90+40)*pi_number/180
        ctx.translate(gauge_right_outer_radius*sin(angle1), -gauge_right_outer_radius*cos(angle1))
        ctx.translate(-gauge_right_outer_radius*0.03, -gauge_right_outer_radius*0.07)
        gradient_pattern = cairo.RadialGradient(0, 0, 0, 0, 0, gauge_right_outer_radius*0.07)
        scale_value = 1-0.93
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba((0.93 - 0.93) / scale_value, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba((0.94 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.95 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba((0.98 - 0.93) / scale_value, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba((0.99 - 0.93) / scale_value, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius*0.07, start_angle, end_angle)
        ctx.line_to(0, 0)
        ctx.fill()
        ctx.restore()


        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)

        # Draw white reflection on upper right area of the circular edge of the right gauge.
        for i in range(2):
            start_angle = (305+15)*pi_number/180
            end_angle = (305+25+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_right_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_right_outer_radius*0.992, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_right_outer_radius*0.992, 0, 0, gauge_right_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection on upper area of the upper edge of the right gauge.
        for i in range(2):
            angle1 = (90+40)*pi_number/180
            # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
            ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
            ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
            ctx.rel_line_to(-gauge_right_outer_radius, 0)
            ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
            gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)*0.98, 0, gauge_right_outer_radius*cos(angle1))
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection on lower area of the lower edge of the right gauge.
        for i in range(2):
            angle1 = (90-40)*pi_number/180
            # "gauge_right_upper_lower_edge_move_horizontal" value is used for avoiding overlapping inner sides of the edges of the right gauge at the corners.
            ctx.move_to(gauge_right_outer_radius*sin(angle1), gauge_right_outer_radius*cos(angle1))
            ctx.rel_move_to(0, -gauge_right_outer_radius*0.07)
            ctx.rel_line_to(0, gauge_right_outer_radius*0.07)
            ctx.rel_line_to(-gauge_right_outer_radius, 0)
            ctx.rel_line_to(0, -gauge_right_outer_radius*0.07)
            gradient_pattern = cairo.LinearGradient(0, gauge_right_outer_radius*cos(angle1)*0.98, 0, gauge_right_outer_radius*cos(angle1))
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        ctx.restore()


        # Draw shadow on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + 0, chart_height / 2)
        start_angle = -40*pi_number/180
        end_angle = 40*pi_number/180

        gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius, 0, 0, gauge_right_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 0/255, 0/255, 0/255, 0)
        gradient_pattern.add_color_stop_rgba(0, 0/255, 0/255, 0/255, 0.5)
        gradient_pattern.add_color_stop_rgba(1, 0/255, 0/255, 0/255, 0)
        ctx.set_source(gradient_pattern)
        ctx.arc(0, 0, gauge_right_outer_radius, start_angle, end_angle)
        ctx.rel_line_to(-gauge_right_outer_radius, -gauge_outer_radius*0.067)
        ctx.rel_line_to(0, -gauge_right_outer_radius-gauge_outer_radius*0.333)
        ctx.fill()
        ctx.restore()


        # Draw horizontal separator line on the center of the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        ctx.move_to(gauge_separator_line_horizontal_start, 0)
        ctx.rel_line_to(gauge_separator_line_horizontal_length, 0)
        ctx.set_line_width(1.5)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()
        ctx.restore()


        # Draw circular (partial) line on the left of the disk read/write labels on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        start_angle = -31*pi_number/180
        end_angle = -4*pi_number/180

        ctx.set_line_width(1.5)
        ctx.set_source_rgba(chart_line_color_disk_speed_usage[0], chart_line_color_disk_speed_usage[1], chart_line_color_disk_speed_usage[2], chart_line_color_disk_speed_usage[3])
        ctx.arc(0, 0, gauge_outer_radius * 1.07, start_angle, end_angle)
        ctx.stroke()
        ctx.restore()


        # Draw circular (partial) line on the left of the network download/upload labels on the right gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        start_angle = 4*pi_number/180
        end_angle = 31*pi_number/180

        ctx.set_line_width(1.5)
        ctx.set_source_rgba(chart_line_color_network_speed_data[0], chart_line_color_network_speed_data[1], chart_line_color_network_speed_data[2], chart_line_color_network_speed_data[3])
        ctx.arc(0, 0, gauge_outer_radius * 1.07, start_angle, end_angle)
        ctx.stroke()
        ctx.restore()


        # Draw background and outer circle of the circular gauge.
        ctx.arc(gauge_circular_center_x, chart_height / 2, gauge_outer_radius, 0, 2*pi_number)
        gradient_pattern = cairo.RadialGradient(gauge_circular_center_x, chart_height / 2, 0, gauge_circular_center_x, chart_height / 2, gauge_outer_radius)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.86, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.88, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.90, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(0.96, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()


        # Draw background and inner circle of the circular gauge.
        ctx.arc(gauge_circular_center_x, chart_height / 2, gauge_inner_radius, 0, 2*pi_number)
        gradient_pattern = cairo.RadialGradient(gauge_circular_center_x, chart_height / 2, 0, gauge_circular_center_x, chart_height / 2, gauge_inner_radius)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.94, 34/255, 52/255, 71/255, 1)
        gradient_pattern.add_color_stop_rgba(0.96, 20/255, 26/255, 35/255, 1)
        gradient_pattern.add_color_stop_rgba(0.98, 44/255, 60/255, 79/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 57/255, 68/255, 104/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()


        # Rotate the coordinate system and draw reflection on the background of the inner circle.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.rotate(-45*pi_number/180)
        ctx.arc(0, 0, gauge_inner_radius*0.94, 0, 2*pi_number)
        gradient_pattern = cairo.LinearGradient(0, -gauge_inner_radius*0.94/2, 0, gauge_inner_radius*0.94/2)
        gradient_pattern.add_color_stop_rgba(0, 32/255, 41/255, 49/255, 1)
        gradient_pattern.add_color_stop_rgba(0.5, 72/255, 88/255, 107/255, 1)
        gradient_pattern.add_color_stop_rgba(1, 32/255, 41/255, 49/255, 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Save translations.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)

        # Draw white reflection (on 180 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (180-40-i)*pi_number/180
            end_angle = (180+40+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 305 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (305-20-i)*pi_number/180
            end_angle = (305+20+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 45 degree) on the outer circle of the circular gauge.
        for i in range(4):
            start_angle = (45-20-i)*pi_number/180
            end_angle = (45+20+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_outer_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_outer_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_outer_radius*0.98, 0, 0, gauge_outer_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 270 degree) on the inner circle of the circular gauge.
        for i in range(3):
            start_angle = (270-35-i)*pi_number/180
            end_angle = (270+35+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_inner_radius, end_angle, start_angle)
            ctx.arc(0, 0, gauge_inner_radius*0.98, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius*0.98, 0, 0, gauge_inner_radius*1)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Draw white reflection (on 90 degree) on the inner circle of the circular gauge.
        for i in range(3):
            start_angle = (90-25-i)*pi_number/180
            end_angle = (90+25+i)*pi_number/180
            ctx.arc_negative(0, 0, gauge_inner_radius*0.96, end_angle, start_angle)
            ctx.arc(0, 0, gauge_inner_radius*0.94, start_angle, end_angle)
            gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius*0.94, 0, 0, gauge_inner_radius*0.96)
            gradient_pattern.add_color_stop_rgba(0, 1.0, 1.0, 1.0, 0.0)
            gradient_pattern.add_color_stop_rgba(1, 1.0, 1.0, 1.0, 0.13)
            ctx.set_source(gradient_pattern)
            ctx.fill()

        # Restore translations.
        ctx.restore()


        # Draw percentage indicator lines on the left side.
        for i, angle in enumerate([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
            ctx.save()
            ctx.translate(gauge_circular_center_x, chart_height / 2)
            ctx.rotate(((i*15)+15)*pi_number/180)

            if angle % 20 == 0:
                ctx.rectangle(-gauge_indicator_line_major_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_major_move, gauge_indicator_line_major_thickness, gauge_indicator_line_major_length)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            else:
                ctx.rectangle(-gauge_indicator_line_minor_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_minor_move, gauge_indicator_line_minor_thickness, gauge_indicator_line_minor_length)
                ctx.set_source_rgba(0.5, 0.5, 0.5, 1.0)
            ctx.fill()

            ctx.restore()

            # Draw percentage numbers on the left side if angle value is power of 20 ("gauge_indicator_text_correction" is a correction number for aligning the texts).
            if angle % 20 == 0:
                ctx.save()
                ctx.translate((gauge_circular_center_x)-gauge_indicator_text_correction, (chart_height / 2)+gauge_indicator_text_correction)
                angle1 = -((i*15)+15)*pi_number/180
                ctx.move_to((gauge_indicator_text_radius-gauge_indicator_text_move)*sin(angle1), (gauge_indicator_text_radius-gauge_indicator_text_move)*cos(angle1))
                ctx.set_font_size(gauge_indicator_text_size)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                ctx.show_text(f'{angle}')
                ctx.restore()

        # Draw percentage indicator lines on the right side.
        for i, angle in enumerate([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
            ctx.save()
            ctx.translate(gauge_circular_center_x, chart_height / 2)
            ctx.rotate(-((i*15)+15)*pi_number/180)

            if angle % 20 == 0:
                ctx.rectangle(-gauge_indicator_line_major_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_major_move, gauge_indicator_line_major_thickness, gauge_indicator_line_major_length)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            else:
                ctx.rectangle(-gauge_indicator_line_minor_thickness / 2, gauge_indicator_text_radius+gauge_indicator_line_minor_move, gauge_indicator_line_minor_thickness, gauge_indicator_line_minor_length)
                ctx.set_source_rgba(0.5, 0.5, 0.5, 1.0)
            ctx.fill()

            ctx.restore()

            # Draw percentage numbers on the right side if angle value is power of 20 ("gauge_indicator_text_correction" is a correction number for aligning the texts).
            if angle % 20 == 0:
                ctx.save()
                ctx.translate((gauge_circular_center_x)-gauge_indicator_text_correction, (chart_height / 2)+gauge_indicator_text_correction)
                angle1 = ((i*15)+15)*pi_number/180
                ctx.move_to((gauge_indicator_text_radius-gauge_indicator_text_move)*sin(angle1), (gauge_indicator_text_radius-gauge_indicator_text_move)*cos(angle1))
                ctx.set_font_size(gauge_indicator_text_size)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
                ctx.show_text(f'{angle}')
                ctx.restore()


        # Draw vertical separator line on the center of the inner circle of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.move_to(0, -gauge_separator_line_vertical_center_length / 2)
        ctx.rel_line_to(0, gauge_separator_line_vertical_center_length)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()

        # Draw vertical separator line on the center of the outer circle of the circular gauge (upper side).
        ctx.move_to(0, -gauge_separator_line_vertical_upper_start)
        ctx.rel_line_to(0, gauge_separator_line_vertical_upper_length)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()

        # Draw vertical separator line on the center of the outer circle of the circular gauge (lower side).
        ctx.move_to(0, gauge_separator_line_vertical_lower_start)
        ctx.rel_line_to(0, gauge_separator_line_vertical_lower_length)
        ctx.set_source_rgba(100/255, 113/255, 126/255, 1.0)
        ctx.stroke()


        # Draw "CPU" label on the upper-left side of the inner circle of the circular gauge.
        cpu_text = "CPU"
        ctx.set_font_size(gauge_indicator_text_size)
        text_extends = ctx.text_extents(cpu_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(cpu_text)

        # Draw "RAM" label on the upper-right side of the inner circle of the circular gauge.
        ram_text = "RAM"
        ctx.set_font_size(gauge_indicator_text_size)
        text_extends = ctx.text_extents(ram_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(ram_text)

        # Draw "Processes" label on the lower-left side of the inner circle of the circular gauge.
        processes_text = "Up Time"
        ctx.set_font_size(gauge_processes_swap_label_text_size)
        if len(processes_text) > 9:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        text_extends = ctx.text_extents(processes_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(processes_text)

        # Draw "Swap" label on the upper-right side of the inner circle of the circular gauge.
        ram_text = "Swap"
        ctx.set_font_size(gauge_processes_swap_label_text_size)
        if len(ram_text) > 9:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        text_extends = ctx.text_extents(ram_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_label_text_move)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(ram_text)


        # Draw "%" labels below the CPU and RAM percentages on the inner circle of the circular gauge.
        percentage_text = "%"
        ctx.set_font_size(gauge_percentage_label_text_below_cpu_ram_size)
        text_extends = ctx.text_extents(percentage_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_percentage_label_text_below_cpu_ram_move)
        ctx.set_source_rgba(180/255, 180/255, 180/255, 1.0)
        ctx.show_text(percentage_text)
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_percentage_label_text_below_cpu_ram_move)
        ctx.set_source_rgba(180/255, 180/255, 180/255, 1.0)
        ctx.show_text(percentage_text)


        # Draw lowest layer of the shadow of the CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        text_extends = ctx.text_extents(cpu_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move + 2 * gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(cpu_usage_text)

        # Draw shadow of the CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move + gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(cpu_usage_text)

        # Draw CPU usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), -gauge_cpu_ram_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(cpu_usage_text)

        # Draw lowest layer of the shadow of the RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        text_extends = ctx.text_extents(ram_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move + 2 * gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(ram_usage_text)

        # Draw shadow of the RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move + gauge_cpu_ram_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(ram_usage_text)

        # Draw RAM usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, -gauge_cpu_ram_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_cpu_ram_usage_text_size)
        ctx.show_text(ram_usage_text)

        # Draw lowest layer of the shadow of the Processes label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        text_extends = ctx.text_extents(processes_number_text)
        text_start_x = text_extends.width
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move + 2 * gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(processes_number_text)

        # Draw shadow of the Processes label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move + gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(processes_number_text)

        # Draw Processes label on the left side of the inner circle of the circular gauge.
        ctx.move_to(-(text_start_x + gauge_cpu_ram_label_text_margin), gauge_processes_swap_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(processes_number_text)

        # Draw lowest layer of the shadow of the Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        text_extends = ctx.text_extents(swap_usage_text)
        text_start_x = text_extends.width
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move + 2 * gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(swap_usage_text)

        # Draw shadow of the Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move + gauge_processes_swap_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(swap_usage_text)

        # Draw Swap usage percentage label on the left side of the inner circle of the circular gauge.
        ctx.move_to(gauge_cpu_ram_label_text_margin, gauge_processes_swap_usage_text_move)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_processes_swap_usage_text_size)
        ctx.show_text(swap_usage_text)

        # Reset translating.
        ctx.restore()
        ctx.move_to(0, 0)
        ctx.stroke()


        # Draw CPU usage indicator.
        cpu_usage_angle = self.cpu_usage_percent_ave[-1] / 10
        start_angle = ((0*15)+105)*pi_number/180
        end_angle = ((cpu_usage_angle*15)+105)*pi_number/180

        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.arc_negative(0, 0, gauge_outer_radius*0.86, end_angle, start_angle)
        ctx.arc(0, 0, gauge_inner_radius, start_angle, end_angle)
        gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius, 0, 0, gauge_outer_radius*0.86)
        gradient_pattern.add_color_stop_rgba(0, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 0)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 0.5)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 1)
        gradient_pattern.add_color_stop_rgba(1, chart_line_color_cpu_percent[0], chart_line_color_cpu_percent[1], chart_line_color_cpu_percent[2], chart_line_color_cpu_percent[3] * 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw RAM usage indicator.
        ram_usage_angle = self.ram_usage_percent[-1] / 10
        end_angle = (75-(0*15))*pi_number/180
        start_angle = (75-(ram_usage_angle*15))*pi_number/180

        ctx.save()
        ctx.translate(gauge_circular_center_x, chart_height / 2)
        ctx.arc_negative(0, 0, gauge_outer_radius*0.86, end_angle, start_angle)
        ctx.arc(0, 0, gauge_inner_radius, start_angle, end_angle)
        gradient_pattern = cairo.RadialGradient(0, 0, gauge_inner_radius, 0, 0, gauge_outer_radius*0.86)
        gradient_pattern.add_color_stop_rgba(0, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 0)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 0.5)
        gradient_pattern.add_color_stop_rgba(0.9, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 1)
        gradient_pattern.add_color_stop_rgba(1, chart_line_color_memory_percent[0], chart_line_color_memory_percent[1], chart_line_color_memory_percent[2], chart_line_color_memory_percent[3] * 1)
        ctx.set_source(gradient_pattern)
        ctx.fill()
        ctx.restore()


        # Draw "Read Speed" label on the upper-left side of the inner circle of the circular gauge.
        ctx.save()
        ctx.translate(gauge_circular_center_x + gauge_right_move, chart_height / 2)
        read_speed_text = "Read Speed"
        ctx.set_font_size(gauge_disk_network_label_text_size)
        if len(read_speed_text) > 16:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(read_speed_text)

        # Draw "Write Speed" label on the upper-left side of the inner circle of the circular gauge.
        write_speed_text = "Write Speed"
        ctx.set_font_size(gauge_disk_network_label_text_size)
        if len(write_speed_text) > 16:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(write_speed_text)

        # Draw "Download Speed" label on the upper-left side of the inner circle of the circular gauge.
        download_speed_text = "Download Speed"
        ctx.set_font_size(gauge_disk_network_label_text_size)
        if len(download_speed_text) > 16:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(download_speed_text)

        # Draw "Upload Speed" label on the upper-left side of the inner circle of the circular gauge.
        upload_speed_text = "Upload Speed"
        ctx.set_font_size(gauge_disk_network_label_text_size)
        if len(upload_speed_text) > 16:
            ctx.set_font_size(gauge_indicator_text_size_smaller)
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y)
        ctx.set_source_rgba(188/255, 191/255, 193/255, 1.0)
        ctx.show_text(upload_speed_text)


        # Draw lowest layer of the shadow of the Disk Read Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(disk_read_speed_text)

        # Draw shadow of the Disk Read Speed label on the right gauge.
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_read_speed_text)

        # Draw Disk Read Speed label on the right gauge.
        ctx.move_to(gauge_disk_read_speed_label_text_move_x, -gauge_disk_read_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_read_speed_text)

        # Draw lowest layer of the shadow of the Disk Write Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(disk_write_speed_text)

        # Draw shadow of the Disk Write Speed label on the right gauge.
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_write_speed_text)

        # Draw Disk Write Speed label on the right gauge.
        ctx.move_to(gauge_disk_write_speed_label_text_move_x, -gauge_disk_write_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(disk_write_speed_text)

        # Draw lowest layer of the shadow of the Network Download Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(network_download_speed_text)

        # Draw shadow of the Network Download Speed label on the right gauge.
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_download_speed_text)

        # Draw Network Download Speed label on the right gauge.
        ctx.move_to(gauge_network_download_speed_label_text_move_x, gauge_network_download_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_download_speed_text)

        # Draw lowest layer of the shadow of the Network Upload Speed label on the right gauge.
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + (2 * gauge_disk_network_usage_text_shadow_move))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ctx.show_text(network_upload_speed_text)

        # Draw shadow of the Network Upload Speed label on the right gauge.
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y + gauge_disk_network_usage_text_shadow_move)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.7)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_upload_speed_text)

        # Draw Network Upload Speed label on the right gauge.
        ctx.move_to(gauge_network_upload_speed_label_text_move_x, gauge_network_upload_speed_label_text_move_y + gauge_disk_network_usage_text_move_y)
        ctx.set_source_rgba(232/255, 232/255, 232/255, 1.0)
        ctx.set_font_size(gauge_disk_network_usage_text_size)
        ctx.show_text(network_upload_speed_text)

        ctx.restore()


        # Show Cairo context as image on label.
        image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (chart_width, chart_height), surface1.get_data().tobytes(), "raw", "BGRA", 0, 1))
        # Update label for showing the new image.
        widget.configure(image=image_ref)
        widget.image = image_ref


    def cpu_system_up_time_func(self):
        """
        Get system up time.
        """

        with open("/proc/uptime") as reader:
            sut_read = float(reader.read().split(" ")[0].strip())

        sut_hours_int = int(sut_read/60/60)
        sut_minutes_int = int(sut_read/60)
        sut_minutes_int = sut_minutes_int - (sut_hours_int*60)

        system_up_time = f'{sut_hours_int:02}:{sut_minutes_int:02}'

        return system_up_time


    def performance_define_data_unit_converter_variables_func(self):
        """
        Define values for converting data units and setting value precision.
        Data unit options: 0: Bytes (ISO), 1: Bytes (IEC), 2: bits (ISO), 3: bits (IEC).
        """

        self.data_unit_list = [[0, "B", "B", "b", "b"], [1, "KiB", "KB", "Kib", "Kb"], [2, "MiB", "MB", "Mib", "Mb"],
                              [3, "GiB", "GB", "Gib", "Gb"], [4, "TiB", "TB", "Tib", "Tb"], [5, "PiB", "PB", "Pib", "Pb"]]


    def performance_data_unit_converter_func(self, data_type, data_type_option, data, unit, precision):
        """
        Convert data units and set value precision.
        """

        data_unit_list = self.data_unit_list
        if isinstance(data, str) == True:
            return data

        if unit == 0:
            power_of_value = 1024
            unit_text_index = 1

        if unit == 1:
            power_of_value = 1000
            unit_text_index = 2

        if data_type == "speed":
            if data_type_option == 1:
                data = data * 8
                unit_text_index = unit_text_index + 2

        unit_counter = 0
        while data >= power_of_value:
            unit_counter = unit_counter + 1
            data = data/power_of_value
        unit = data_unit_list[unit_counter][unit_text_index]

        if data == 0:
            precision = 0

        return f'{data:.{precision}f} {unit}'


MainWindow()

