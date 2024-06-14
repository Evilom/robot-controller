import time
import tkinter as tk
from tkinter import ttk
import threading
import serial

serName = "/dev/ttyACM0"
ser = None
lPos = [0, 0, 0, 0, 0, 0]
jPos = [0, 0, 0, 0, 0, 0]

def handle_button_click(button_label):
    axis, action = button_label.split(" ")
    if axis.startswith("J"):
        handle_single_axis(axis, action)
    elif axis in ["X", "Y", "Z", "A", "B", "C"]:
        handle_linkage_axis(axis, action)
    else:
        print(f"Unsupported axis: {axis}")

def handle_single_axis(axis, action):
    axis_index = int(axis[1:]) - 1
    if action == "+":
        lPos[axis_index] += 1
        print(f"Incrementing J{axis_index+1}")
    elif action == "-":
        lPos[axis_index] -= 1
        print(f"Decrementing J{axis_index+1}")
    else:
        print(f"Invalid action for single axis: {action}")

def handle_linkage_axis(axis, action):
    if action == "+":
        print(f"Incrementing {axis}")
    elif action == "-":
        print(f"Decrementing {axis}")
    else:
        print(f"Invalid action for linkage axis: {action}")

def confirm_speed():
    speed = speed_entry.get()
    print(f"Speed set to {speed}%")

def connect_to_serial():
    global ser
    try:
        ser = serial.Serial(serName, 115200, timeout=1)
        print(f"Connected to: {serName}")
        threading.Thread(target=read_serial_data, daemon=True).start()
    except serial.SerialException as e:
        print(f"Failed to connect: {e}")

def send_command():
    global ser
    if ser and ser.is_open:
        command = command_entry.get()
        ser.write(f'{command}\n'.encode('utf-8'))
    else:
        print("Serial port not connected.")

def read_serial_data():
    global ser
    while True:
        if ser and ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            if data:
                if data.startswith("ok"):
                    lPos = parse_line_to_positions(data)
                    print(lPos)
                print(data)
        time.sleep(0.1)

def parse_line_to_positions(line):
    parts = line.strip().split()
    positions = []
    for part in parts:
        try:
            positions.append(float(part))
        except ValueError:
            continue
    return positions

# GUI setup
root = tk.Tk()
root.title("Interface")
root.geometry("412x400")

# Labels and buttons setup
single_axis_label = tk.Label(root, text="Single Axis")
single_axis_label.grid(row=0, column=0, columnspan=2)

linkage_label = tk.Label(root, text="Linkage")
linkage_label.grid(row=0, column=6, columnspan=2)

for i in range(6):
    tk.Button(root, text="<<+", command=lambda i=i: handle_button_click(f"J{i+1} +")).grid(row=i+1, column=0)
    tk.Label(root, text=f"J{i+1}").grid(row=i+1, column=1)
    tk.Button(root, text="->>", command=lambda i=i: handle_button_click(f"J{i+1} -")).grid(row=i+1, column=2)

linkage_labels = ["X", "Y", "Z", "A", "B", "C"]
for i, text in enumerate(linkage_labels):
    tk.Button(root, text="<<+", command=lambda text=text: handle_button_click(f"{text} +")).grid(row=i+1, column=6)
    tk.Label(root, text=text).grid(row=i+1, column=7)
    tk.Button(root, text="->>", command=lambda text=text: handle_button_click(f"{text} -")).grid(row=i+1, column=8)

speed_label = tk.Label(root, text="Speed")
speed_label.grid(row=7, column=0)

speed_entry = tk.Entry(root, width=5)
speed_entry.grid(row=7, column=1)

percent_label = tk.Label(root, text="%")
percent_label.grid(row=7, column=2)

confirm_button = tk.Button(root, text="Confirm", command=confirm_speed)
confirm_button.grid(row=7, column=3)

command_label = tk.Label(root, text="Command")
command_label.grid(row=8, column=0)

command_entry = tk.Entry(root, width=20)
command_entry.grid(row=8, column=1, columnspan=3)

send_button = tk.Button(root, text="Send", command=send_command)
send_button.grid(row=8, column=4)

connect_button = tk.Button(root, text="Connect", command=connect_to_serial)
connect_button.grid(row=9, column=0)

start_button = tk.Button(root, text="Start", command=lambda: ser.write(f'!START\n'.encode('utf-8')))
start_button.grid(row=9, column=1)

jpos_button = tk.Button(root, text="JPos", command=lambda: ser.write(f'#GETJPOS\n'.encode('utf-8')))
jpos_button.grid(row=9, column=2)

lpos_button = tk.Button(root, text="LPos", command=lambda: ser.write(f'#GETLPOS\n'.encode('utf-8')))
lpos_button.grid(row=9, column=3)

root.mainloop()
