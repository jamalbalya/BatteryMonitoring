# """
# ------------------------------------------------------------------------
# Copyright (c) 2023, Jamal Balya
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name Jamal Balya nor the names of its contributors may be
#   used to endorse or promote products derived from this software without
#   specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# """

import tkinter as tk
import pyttsx3
import psutil

class BatteryMonitorUI:
    def __init__(self, master):
        self.master = master
        master.title("Battery Monitoring JamalBalya v1.1.1")

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)

        # Create labels and entry fields
        low_label = tk.Label(master, text="Low Battery Level max 56%:")
        low_label.grid(row=0, column=0)

        vcmd = (master.register(self.validate_low_entry), '%P')
        self.low_entry = tk.Entry(master, validate="key", validatecommand=vcmd)
        self.low_entry.grid(row=0, column=1)

        high_label = tk.Label(master, text="High Battery Level max 99%:")
        high_label.grid(row=1, column=0)

        vcmd = (master.register(self.validate_high_entry), '%P')
        self.high_entry = tk.Entry(master, validate="key", validatecommand=vcmd)
        self.high_entry.grid(row=1, column=1)

        # Create save button
        save_button = tk.Button(master, text="Save", command=self.start_monitoring, font=("Helvetica", 10))
        save_button.config(width=10, pady=5, padx=10)
        save_button.grid(row=2, column=0)

        # Create close button
        close_button = tk.Button(master, text="Close", command=self.close_app, font=("Helvetica", 10))
        close_button.config(width=10, pady=5, padx=10)
        close_button.grid(row=2, column=1)

    def validate_low_entry(self, value):
        if value.isdigit() and len(value) <= 2 and int(value) <= 56 or value == "":
            return True
        else:
            return False

    def validate_high_entry(self, value):
        if value.isdigit() and len(value) <= 2 and int(value) <= 99 or value == "":
            return True
        else:
            return False

    def start_monitoring(self):
        # Retrieve low and high battery level values from entry fields
        low_battery_level = int(self.low_entry.get())
        high_battery_level = int(self.high_entry.get())

        # Minimize the window
        self.master.iconify()

        # Define the function to monitor the battery level and pop-up messages
        def monitor_battery_level():
            try:
                battery_level = psutil.sensors_battery().percent
            except:
                # Handle errors gracefully
                self.engine.say("Failed to retrieve battery level")
                self.engine.runAndWait()
                return

            if battery_level <= low_battery_level:
                # Show low battery message
                self.engine.say(f"The battery level is at {battery_level}%. Please connect the charger.")
                self.engine.runAndWait()
                self.master.deiconify()
            elif battery_level >= high_battery_level:
                # Show high battery message
                self.engine.say(f"The battery level is at {battery_level}%. Please unplug the charger.")
                self.engine.runAndWait()
                self.master.deiconify()

            # Wait for 1 minute before checking again
            self.master.after(60000, monitor_battery_level)

        # Start monitoring
        monitor_battery_level()

    def close_app(self):
        self.master.deiconify()
        self.master.destroy()

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y position to center the window
x = int((screen_width / 2) - (375 / 2)) # 600 is the default width of the window
y = int((screen_height / 2) - (90 / 2)) # 250 is the default height of the window

# Set the window position
root.geometry(f"375x90+{x}+{y}")

# Create the battery monitor UI
monitor_ui = BatteryMonitorUI(root)

# Start the main event loop
root.mainloop()
