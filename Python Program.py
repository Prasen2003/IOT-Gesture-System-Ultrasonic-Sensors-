import tkinter as tk
import keyboard
import time
import serial

# Dictionary to hold profiles with customizable key bindings for sensors
profiles = {
    "Media Controls": {"sensor1_key": "volume up", "sensor2_key": "volume down"},
    "Profile 1": {"sensor1_key": "up", "sensor2_key": "down"},
}

current_profile = "Media Controls"  # Set "Media Controls" as the default profile

last_play_pause_time = 0  # Track time for play/pause delay
last_volume_change_time = 0  # Track time for volume change delay
last_navigation_time = 0  # Track time for backward/forward delay

# Create the main window
root = tk.Tk()
root.title("Virtual Sensor Input")

# Create Tkinter variables after initializing root
sensor1_enabled = tk.BooleanVar(value=False)  # Default state is 'off'
sensor2_enabled = tk.BooleanVar(value=False)  # Default state is 'off'
both_sensors_enabled = tk.BooleanVar(value=True)  # Default state is 'on' (both sensors enabled)

# Connect to the Arduino's serial port
arduino_port = 'COM3'  # Replace with your Arduino's serial port (e.g., COM3 on Windows)
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

# Keep track of the last few readings for each sensor (moving average)
sensor1_history = []
sensor2_history = []
max_history_size = 5  # Number of readings to average
threshold = 1  # Define a threshold for significant change

def moving_average(sensor_history, new_value):
    sensor_history.append(new_value)
    if len(sensor_history) > max_history_size:
        sensor_history.pop(0)
    return sum(sensor_history) / len(sensor_history)

# Process sensor data and map to keyboard inputs based on the selected profile
def process_sensor_data(sensor1, sensor2):
    global last_play_pause_time, last_volume_change_time, last_navigation_time
    profile = profiles[current_profile]
    sensor1_key = profile["sensor1_key"]
    sensor2_key = profile["sensor2_key"]

    current_time = time.time()

    # Reflect sensor values in the sliders
    if abs(sensor1_slider.get() - sensor1) > threshold:
        sensor1_slider.set(sensor1)
    if abs(sensor2_slider.get() - sensor2) > threshold:
        sensor2_slider.set(sensor2)

    # Only process sensors if both sensors are enabled
    if both_sensors_enabled.get():
        # Media control profile: Play/Pause on both sensor input
        if current_profile == "Media Controls":
            # Play/Pause if both sensors are active
            if sensor1 < 10 and sensor2 < 10:
                if current_time - last_play_pause_time > 2:
                    keyboard.press_and_release('space')  # Simulate play/pause with space key
                    last_play_pause_time = current_time
                    print("Play/Pause triggered")
                return

            # Volume control with sensor 1
            if sensor1_enabled.get() and sensor1 <= 3:
                # Decrease volume faster when sensor1 < 3 (no delay or very short delay)
                if current_time - last_volume_change_time > 0.1:
                    keyboard.press_and_release('volume down')
                    last_volume_change_time = current_time
                    print("Volume Down triggered (fast)")

            elif sensor1_enabled.get() and 4 <= sensor1 <= 10:
                if current_time - last_volume_change_time > 0.15:
                    keyboard.press_and_release('volume down')
                    last_volume_change_time = current_time
                    print("Volume Down triggered (normal)")

            # Slow Volume Up if sensor1 is between 11 and 20
            elif sensor1_enabled.get() and 11 <= sensor1 <= 20:
                if current_time - last_volume_change_time > 0.2:
                    keyboard.press_and_release('volume up')
                    last_volume_change_time = current_time
                    print("Volume Up triggered")

            # Control with sensor 2 (backward/forward navigation) with 0.5 seconds delay
            if sensor2_enabled.get() and sensor2 < 10:
                if current_time - last_navigation_time > 0.5:
                    keyboard.press_and_release('left')
                    last_navigation_time = current_time
                    print("Backward (left arrow) triggered")

            elif sensor2_enabled.get() and 11 <= sensor2 <= 20:
                if current_time - last_navigation_time > 0.5:
                    keyboard.press_and_release('right')
                    last_navigation_time = current_time
                    print("Forward (right arrow) triggered")

    print(f"Sensor1: {sensor1}, Sensor2: {sensor2} | Keys: {sensor1_key}, {sensor2_key}")

# Read actual sensor values from Arduino
def read_from_arduino():
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            sensor1_value, sensor2_value = map(int, data.split(','))
            return sensor1_value, sensor2_value
        except:
            return 20, 20  # Default values if there's an error
    return 20, 20

# Update sensor values and process them
def update_sensors():
    if both_sensors_enabled.get():
        sensor1_value, sensor2_value = read_from_arduino()

        # Apply moving averages
        averaged_sensor1 = moving_average(sensor1_history, sensor1_value)
        averaged_sensor2 = moving_average(sensor2_history, sensor2_value)

        if not sensor1_enabled.get():
            averaged_sensor1 = 20
        if not sensor2_enabled.get():
            averaged_sensor2 = 20

        process_sensor_data(averaged_sensor1, averaged_sensor2)
    root.after(100, update_sensors)  # Keep 100ms update interval

# Function to open the key binding customization window
def open_key_binding_window():
    def save_key_bindings():
        sensor1_key = sensor1_key_entry.get()
        sensor2_key = sensor2_key_entry.get()
        profiles[current_profile]["sensor1_key"] = sensor1_key
        profiles[current_profile]["sensor2_key"] = sensor2_key
        key_binding_window.destroy()

    key_binding_window = tk.Toplevel(root)
    key_binding_window.title("Customize Key Bindings")

    window_width = 400
    window_height = 300
    key_binding_window.geometry(f"{window_width}x{window_height}")
    key_binding_window.update_idletasks()

    screen_width = key_binding_window.winfo_screenwidth()
    screen_height = key_binding_window.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    key_binding_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    tk.Label(key_binding_window, text=f"Customizing Profile: {current_profile}").pack(pady=10)

    tk.Label(key_binding_window, text="Sensor 1 Key Binding:").pack(pady=5)
    sensor1_key_entry = tk.Entry(key_binding_window)
    sensor1_key_entry.insert(0, profiles[current_profile]["sensor1_key"])
    sensor1_key_entry.pack(pady=5)

    tk.Label(key_binding_window, text="Sensor 2 Key Binding:").pack(pady=5)
    sensor2_key_entry = tk.Entry(key_binding_window)
    sensor2_key_entry.insert(0, profiles[current_profile]["sensor2_key"])
    sensor2_key_entry.pack(pady=5)

    save_button = tk.Button(key_binding_window, text="Save", command=save_key_bindings)
    save_button.pack(pady=20)

# Function to change the current profile
def change_profile(new_profile):
    global current_profile
    current_profile = new_profile
    profile_label.config(text=f"Current Profile: {current_profile}")

tk.Label(root, text="Sensor 1").pack()
sensor1_slider = tk.Scale(root, from_=0, to=20, orient='horizontal')
sensor1_slider.pack()

sensor1_switch = tk.Checkbutton(root, text="Enable Sensor 1", variable=sensor1_enabled)
sensor1_switch.pack()

tk.Label(root, text="Sensor 2").pack()
sensor2_slider = tk.Scale(root, from_=0, to=20, orient='horizontal')
sensor2_slider.pack()

sensor2_switch = tk.Checkbutton(root, text="Enable Sensor 2", variable=sensor2_enabled)
sensor2_switch.pack()

both_sensors_switch = tk.Checkbutton(root, text="Enable Both Sensors", variable=both_sensors_enabled)
both_sensors_switch.pack()

tk.Label(root, text="Select Profile").pack()
profile_var = tk.StringVar(value="Media Controls")
profile_dropdown = tk.OptionMenu(root, profile_var, *profiles.keys(), command=change_profile)
profile_dropdown.pack()

profile_label = tk.Label(root, text=f"Current Profile: {current_profile}")
profile_label.pack()

customize_button = tk.Button(root, text="Customize Key Bindings", command=open_key_binding_window)
customize_button.pack()

# Start updating the sensors
update_sensors()

# Run the GUI loop
root.mainloop()
