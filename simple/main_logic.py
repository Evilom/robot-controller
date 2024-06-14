import time
import serial
import threading

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
    send_command(formatCommand(lPos))

def handle_linkage_axis(axis, action):
    if action == "+":
        print(f"Incrementing {axis}")
    elif action == "-":
        print(f"Decrementing {axis}")
    else:
        print(f"Invalid action for linkage axis: {action}")

def confirm_speed(speed):
    print(f"Speed set to {speed}%")

def connect_to_serial():
    global ser
    try:
        ser = serial.Serial(serName, 115200, timeout=1)
        print(f"Connected to: {serName}")
        threading.Thread(target=read_serial_data, daemon=True).start()
    except serial.SerialException as e:
        print(f"Failed to connect: {e}")

def send_command(command):
    global ser
    if ser and ser.is_open:
        ser.write(f'{command}\n'.encode('utf-8'))
    else:
        print("Serial port not connected.")

def formatCommand(positions):
    command_str = "@{},{}\n".format(",".join(map(str, positions)), 5)
    return command_str.encode()

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
