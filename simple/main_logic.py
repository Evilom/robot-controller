import time
import serial
import threading

serName = "/dev/ttyACM0"
ser = None
lPos = [0, 0, 0, 0, 0, 0]
jPos = [0, 0, 0, 0, 0, 0]
canGetjPOs = False
canGetLPOs = False

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
        jPos[axis_index] += 1
        print(f"Incrementing J{axis_index+1}")
    elif action == "-":
        jPos[axis_index] -= 1
        print(f"Decrementing J{axis_index+1}")
    else:
        print(f"Invalid action for single axis: {action}")
    print(jPos)
    send_command(formatCommand(jPos))

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
    global ser,canGetjPOs,canGetLPOs
    if ser and ser.is_open:
        ser.write(f'{command}\n'.encode('utf-8'))
        if command == '#GETJPOS':
            canGetjPOs = True
        elif command == '#GETLPOS':
            canGetLPOs = True
    else:
        print("Serial port not connected.")

def formatCommand(positions):
    command_str = "&{},{}".format(",".join(map(str, positions)), 5)
    return command_str

def read_serial_data():
    global ser,jPos,canGetLPOs,canGetjPOs
    while True:
        if ser and ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            if data:
                if data.startswith("ok") and canGetjPOs:
                    jPos = parse_line_to_positions(data)
                    canGetjPOs = False
                    print(jPos)
                elif data.startswith("ok") and canGetLPOs:
                    lPos = parse_line_to_positions(data)
                    canGetLPOs = False
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
