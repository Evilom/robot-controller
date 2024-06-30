import sys

import numpy as np
sys.path.append(".")
import time
import serial
import threading

import serial.tools.list_ports

from core.ik6r import deg2pul, ikine

serName = "/dev/ttyACM0"
ser = None
lPos = [0, 0, 0, 0, 0, 0]
jPos = [0, 0, 0, 0, 0, 0]
a = [35, 146, 52, 0, 0, 0]
d = [0, 0, 0, 115, 0, 72]
t = [0,0,0,0,0,0]
pu = [0, 0, 90, 0, 0, 0]
lLabels = ["X", "Y", "Z", "A", "B", "C"]
moveStep = 1
moveSpeed = 5
ikMethod = 'default'
canGetJPOs = False
canGetLPOs = False
x_offset = 180
y_offset = 0
z_offset = 200

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

def auto_run(path):
    threading.Thread(target=auto_run_func, args=(path,), daemon=True).start()

def auto_run_func(path):
    global jPos, lPos, x_offset, y_offset, z_offset, ikMethod,t,moveSpeed
    with open(path, "r") as file:
        lines = file.readlines()
    
    # 初始化轨迹列表
    trajectory_points = []
    
    # 假设的速度和时间步长
    speed = 5  # 速度，单位：m/s
    time_step = 0.05  # 时间步长，单位：s
    
    for i, line in enumerate(lines):
        parts = line.split()
        if len(parts) != 7:
            raise ValueError("Invalid line format")
        
        lPos = [float(parts[1]) + x_offset, float(parts[2]) + y_offset, float(parts[3]) + z_offset, float(parts[4]), float(parts[5]), float(parts[6])]
        
        # 如果是第一行，直接添加到轨迹列表
        if i == 0:
            trajectory_points.append(lPos)
        else:
            # 只在common模式下进行插值
            if ikMethod == 'common':
                prev_lPos = np.array(trajectory_points[-1][:3])  # 转换为NumPy数组
                current_lPos = np.array(lPos[:3])  # 转换为NumPy数组
                distance = np.linalg.norm(current_lPos - prev_lPos)
                num_steps = int(distance / speed / time_step)
                
                for j in range(num_steps):
                    ti = j / num_steps
                    intermediate_position = prev_lPos + ti * (current_lPos - prev_lPos)
                    intermediate_lPos = list(intermediate_position) + lPos[3:]  # 复制姿态部分
                    trajectory_points.append(intermediate_lPos)
        
        # 如果是最后一行，直接添加到轨迹列表
        if i == len(lines) - 1:
            trajectory_points.append(lPos)
    
    # 发送轨迹点
    for pos in trajectory_points:
        time.sleep(1)
        if ikMethod == 'default':
            # 在default模式下不发送命令
            pass
        elif ikMethod == 'common':
            p = pos.copy()
            p[2] -= 109
            jPos = ikine(a, d, p, t, 1)
            jPos = deg2pul(jPos, pu)
            send_command(formatCommand(jPos))

def set_move_step(step):
    global moveStep
    moveStep = float(step)
    print(f'{moveStep}')

def set_ik_method(method):
    global ikMethod
    ikMethod = method
    print(f'{method}')

def handle_linkage_axis(axis, action):
    global ikMethod,lPos,jPos
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
    if(ikMethod == 'default'):
        send_command(formatCommand(lPos,'@'))
    elif (ikMethod == 'common'):
        p = lPos.copy()
        p[2] -= 109
        jPos = ikine(a, d, p, t, 1)
        jPos = deg2pul(jPos,pu)
        print(jPos)
        send_command(formatCommand(jPos))


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
        if(comport == ""):
            comport = "/dev/ttyACM0"
        ser = serial.Serial(comport, 115200, timeout=1)
        print(f"Connected to: {comport}")
        threading.Thread(target=read_serial_data, daemon=True).start()
    except serial.SerialException as e:
        print(f"Failed to connect: {e}")

def send_command(command):
    global ser,canGetJPOs,canGetLPOs,lPos,jPos
    print(command)
    if ser and ser.is_open:
        ser.write(f'{command}\n'.encode('utf-8'))
        if command == '#GETJPOS':
            canGetJPOs = True
        elif command == '#GETLPOS':
            canGetLPOs = True
        elif command == '!HOME':
            lPos = [222,0,307,0,90,0]
            jPos = [0,0,90,0,0,0]
        elif command == '!START' or command == '!RESET':
            lPos = [89.41,-0,146.74,180.0,73.0,180.0]
            jPos = [0.0,-73.0,180,0,0,0]
    else:
        print("Serial port not connected.")

def formatCommand(positions,type='&'):
    command_str = "{},{}".format(",".join(map(str, positions)), moveSpeed)
    command_str = type+command_str
    return command_str

def read_serial_data():
    global ser,jPos,lPos,canGetLPOs,canGetJPOs
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
