import time
import serial
import threading

import serial.tools.list_ports

serName = "/dev/ttyACM0"
ser = None
lPos = [0, 0, 0, 0, 0, 0]
jPos = [0, 0, 0, 0, 0, 0]
lLabels = ["X", "Y", "Z", "A", "B", "C"]
moveStep = 1
moveSpeed = 5
canGetJPOs = False
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
        jPos[axis_index] += moveStep
        print(f"Incrementing J{axis_index+1}")
    elif action == "-":
        jPos[axis_index] -= moveStep
        print(f"Decrementing J{axis_index+1}")
    else:
        print(f"Invalid action for single axis: {action}")
    print(jPos)
    send_command(formatCommand(jPos))

def set_move_step(step):
    global moveStep
    moveStep = float(step)
    print(f'{moveStep}')

def handle_linkage_axis(axis, action):
    axis_index = lLabels.index(axis)
    if action == "+":
        lPos[axis_index] += moveStep
        print(f"Incrementing {axis}")
    elif action == "-":
        lPos[axis_index] -= moveStep
        print(f"Decrementing {axis}")
    else:
        print(f"Invalid action for linkage axis: {action}")
    print(lPos)
    send_command(formatCommand(lPos,'@'))

def confirm_speed(speed):
    global moveSpeed
    moveSpeed = speed
    print(f"Speed set to {speed}%")

def get_serial_ports():
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    return ports

def connect_to_serial(comport):
    global ser
    try:
        ser = serial.Serial(comport, 115200, timeout=1)
        print(f"Connected to: {comport}")
        threading.Thread(target=read_serial_data, daemon=True).start()
    except serial.SerialException as e:
        print(f"Failed to connect: {e}")

def send_command(command):
    global ser,canGetJPOs,canGetLPOs
    if ser and ser.is_open:
        ser.write(f'{command}\n'.encode('utf-8'))
        if command == '#GETJPOS':
            canGetJPOs = True
        elif command == '#GETLPOS':
            canGetLPOs = True
    else:
        print("Serial port not connected.")

def formatCommand(positions,type='&'):
    command_str = "{},{}".format(",".join(map(str, positions)), moveSpeed)
    command_str = type+command_str
    return command_str

def read_serial_data():
    global ser,jPos,canGetLPOs,canGetJPOs
    while True:
        if ser and ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            if data:
                if data.startswith("ok") and canGetJPOs:
                    jPos = parse_line_to_positions(data)
                    canGetJPOs = False
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
