#!/usr/bin/env python3

# Import modules
import os


# Define class
class Config:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Define configration file and directory. "XDG_CONFIG_HOME" is used by Flatpak but this environment variable may not be defined on several distributions.
        current_user_configdir = os.environ.get('XDG_CONFIG_HOME')
        if current_user_configdir == None or current_user_configdir == "":
            current_user_homedir = os.environ.get('HOME')
            self.config_folder_path = current_user_homedir + "/.config/mini-system-monitor/"
        else:
            self.config_folder_path = current_user_configdir + "/mini-system-monitor/"
        self.config_file_path = self.config_folder_path + "config.txt"

        # Read settings
        self.config_read_func()


    # ----------------------- Called for reading settings (when the application is started) from the configration file -----------------------
    def config_read_func(self):

        # Define variables to read config data
        self.config_variables = []
        self.config_values = []

        # Read the config file
        try:
            with open(self.config_file_path) as reader:
                config_lines = reader.read().split("\n")
        except Exception:
            # Generate config folder if it does not exist.
            if os.path.exists(self.config_folder_path) == False:
                os.makedirs(self.config_folder_path)
            # Read/reset default config data and save to file
            self.config_default_reset_all_func()
            self.config_save_func()
            return

        # Add config names and values into separate lists
        for line in config_lines:
            if " = " in line:
                line_split = line.split(" = ")
                self.config_variables.append(line_split[0])
                self.config_values.append(line_split[1])

        # Read/reset default config data before getting values from the lists which is read from file because some new settings may be added and they may not be present in the config file.
        # Default values are read and modified by the user defined values if they are available.
        self.config_default_reset_all_func()

        # Get config data from the lists which is read from file
        try:
            self.config_get_values_func()
        except Exception:
            pass


    # ----------------------- Called for default all settings -----------------------
    def config_default_reset_all_func(self):

        self.config_default_general_general_func()


    # ----------------------- Called for default general settings -----------------------
    def config_default_general_general_func(self):

        self.remember_last_selected_hardware = 0
        self.selected_disk = ""
        self.selected_network_card = ""

        # Read-only settings.
        self.update_interval = 0.75
        self.chart_data_history = 10
        self.remember_window_size = "550x430"
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


    # ----------------------- Called for reading settings from the configration file -----------------------
    def config_get_values_func(self):

        config_variables = self.config_variables
        config_values = self.config_values

        self.remember_last_selected_hardware = int(config_values[config_variables.index("remember_last_selected_hardware")])
        self.selected_disk = config_values[config_variables.index("selected_disk")]
        self.selected_network_card = config_values[config_variables.index("selected_network_card")]


    # ----------------------- Called for writing settings into the configration file -----------------------
    def config_save_func(self):

        config_write_text = ""
        config_write_text = config_write_text + "remember_last_selected_hardware = " + str(self.remember_last_selected_hardware) + "\n"
        config_write_text = config_write_text + "selected_disk = " + str(self.selected_disk) + "\n"
        config_write_text = config_write_text + "selected_network_card = " + str(self.selected_network_card) + "\n"

        with open(self.config_file_path, "w") as writer:
            writer.write(config_write_text)


# Generate object
Config = Config()

