Steps to install and run the project :

1. Hardware Setup
Components Required:
Arduino Uno (or similar microcontroller)
Ultrasonic sensors (e.g., HC-SR04) - 2 units
Jumper wires
Breadboard (optional for connections)
USB cable (for connecting the Arduino to the PC) - Mini USB
------------------------------------------------------------------------------------
Connections:

Connect the Ultrasonic Sensors:

For Sensor 1:
VCC → Connect to Arduino 5V
GND → Connect to Arduino GND
Trig Pin → Connect to Arduino digital pin 9
Echo Pin → Connect to Arduino digital pin 10

For Sensor 2:
VCC → Connect to Arduino 5V
GND → Connect to Arduino GND
Trig Pin → Connect to Arduino digital pin 11
Echo Pin → Connect to Arduino digital pin 12

Power the Arduino:
Use a USB cable to connect the Arduino to your PC or a power bank for power and data
transfer.

--------------------------------------------------------------------------------------
Test Connections:
Ensure all connections are firm and that there are no loose wires.
--------------------------------------------------------------------------------------

Software Requirements

Install the following software and libraries:

Arduino IDE: Download and install the Arduino IDE from Arduino Official Website.
             Open the IDE and set up the correct COM port and Board in the Tools menu.
             
Python Environment: Install Python (preferably version 3.9 or higher) from Python.org.
                    Add Python to the system PATH during installation.
                    
Python Libraries: Open a terminal or command prompt and run the following commands:

pip install pyserial
pip install keyboard
pip install tkinter

---------------------------------------------------------------------------------------
Programming the Arduino

Upload Arduino Code:
Open the Arduino IDE.
Copy and paste the Arduino code into a new sketch
Save the sketch with a name (e.g., gesture_control).
Connect your Arduino via USB, select the correct Port and Board in the Arduino IDE, and click Upload.


Setting Up the Python Application

Download and Run the Python Code:
Create a new Python script file (e.g., gesture_control.py).
Copy and paste the Python GUI code into the file.
Replace the arduino_port variable in the code with the appropriate port for your Arduino
(e.g., 'COM3' for Windows or '/dev/ttyUSB0' for Linux/Mac).
Running the System
Start the Python Application:
Open a terminal or command prompt and navigate to the directory where the Python
script is saved.

Run the script: python gesture_control.py

Interacting with the GUI:
Use the GUI sliders to monitor sensor values.
Enable or disable specific sensors using the checkboxes.
Customize key bindings and select different control profiles as needed.
Testing Sensor Responses:
Move your hand near the ultrasonic sensors and observe how gestures trigger media
controls or keyboard inputs based on the defined profiles.

----------------------------------------------------------------------------------------
Debugging Tips

No Serial Data:
Ensure the correct COM port is selected in the Arduino IDE.
IOT Gesture System 38
Check the USB connection between your PC and Arduino.

Incorrect Sensor Readings:
Verify the connections of the ultrasonic sensors.
Ensure the sensors are not obstructed or too close to reflective surfaces.

Python Script Errors:
Ensure all Python libraries (pyserial, keyboard, tkinter) are installed correctly.
Double-check that the arduino_port variable matches your Arduino's COM port.
