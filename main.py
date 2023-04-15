import tkinter as tk
import subprocess

class BatteryMonitorUI:
    def __init__(self, master):
        self.master = master
        master.title("Battery Monitor")

        # Create labels and entry fields
        low_label = tk.Label(master, text="Low Battery Level:")
        low_label.grid(row=0, column=0)

        vcmd = (master.register(self.validate_low_entry), '%P')
        self.low_entry = tk.Entry(master, validate="key", validatecommand=vcmd)
        self.low_entry.grid(row=0, column=1)

        high_label = tk.Label(master, text="High Battery Level:")
        high_label.grid(row=1, column=0)

        vcmd = (master.register(self.validate_high_entry), '%P')
        self.high_entry = tk.Entry(master, validate="key", validatecommand=vcmd)
        self.high_entry.grid(row=1, column=1)

        # Create save button
        save_button = tk.Button(master, text="Save", command=self.start_monitoring)
        save_button.grid(row=2, column=0)

        # Create close button
        close_button = tk.Button(master, text="Close", command=self.close_app)
        close_button.grid(row=2, column=1)

    def validate_low_entry(self, value):
        if value.isdigit() and len(value) <= 2 and int(value) >= 1 or value == "":
            return True
        else:
            return False

    def validate_high_entry(self, value):
        if value.isdigit() and len(value) <= 3 and int(value) >= 1 or value == "":
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
                battery_info = subprocess.check_output(['pmset', '-g', 'batt']).decode("utf-8").strip()
                battery_level = int(battery_info.split()[5].replace('%;', ''))
            except (ValueError, subprocess.CalledProcessError):
                # Handle errors gracefully
                tk.messagebox.showerror("Error", "Failed to retrieve battery level")
                return

            if battery_level <= low_battery_level:
                # Show low battery message
                tk.messagebox.showwarning("Low Battery Warning",
                                          f"The battery level is at {battery_level}%. Please connect the charger.")
            elif battery_level >= high_battery_level:
                # Show high battery message
                tk.messagebox.showinfo("High Battery Alert",
                                       f"The battery level is at {battery_level}%. Please unplug the charger.")

            # Wait for 1 minute before checking again
            self.master.after(60000, monitor_battery_level)

    def close_app(self):
        self.master.deiconify()
        self.master.destroy()


# Create the main window
root = tk.Tk()

# Create the battery monitor UI
monitor_ui = BatteryMonitorUI(root)

# Start the main event loop
root.mainloop()
