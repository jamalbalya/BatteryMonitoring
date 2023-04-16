# BatteryMonitoring

The code is a Python program that creates a simple GUI (graphical user interface) using the Tkinter library. The GUI is a battery monitor that pops up a message when the battery level of the computer is below a certain threshold or above another threshold.

The program consists of a class called BatteryMonitorUI which contains methods for initializing the GUI, validating user input, and monitoring the battery level.

The GUI is created by defining a main window using tk.Tk(), setting its title, size and position using title(), geometry() and winfo_screenwidth() and winfo_screenheight(), and adding labels, text entry fields, and buttons using Label(), Entry(), and Button().

The text-to-speech engine is initialized using the pyttsx3 library.

User input validation is performed using the validate and validatecommand options of the Entry widget. These options call the validate_low_entry() and validate_high_entry() methods respectively to ensure that the input is valid.

The monitoring of the battery level is done by defining a nested function called monitor_battery_level(). This function retrieves the battery level using the psutil library, compares it to the low and high thresholds, and pops up a message using the text-to-speech engine if necessary. The after() method is used to call the monitor_battery_level() function every minute.

Finally, the mainloop() method is called to start the event loop and display the GUI.
