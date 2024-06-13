import time
import tkinter as tk
from tkinter import ttk
import threading
import serial

serName = "/dev/ttyACM0"
ser = None
lPos = [0,0,0,0,0,0]
jPos = [0,0,0,0,0,0]

def on_button_click(button_label):
    print(f"Button {button_label} clicked")

def on_confirm():
    speed = speed_entry.get()
    print(f"Speed set to {speed}%")

def on_connect_command():
    global ser
    try:
        ser = serial.Serial(serName, 115200, timeout=1)
        print(f"Connected to: {serName}")
        threading.Thread(target=read_from_serial, daemon=True).start()
    except serial.SerialException as e:
        print(f"Failed to connect: {e}")

def on_send_command():
    global ser
    if ser and ser.is_open:
        command = command_entry.get()
        ser.write(f'{command}\n'.encode('utf-8'))
    else:
        print("Serial port not connected.")

def read_from_serial():
    global ser
    while True:
        if ser and ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            if data:
                if(data.startswith("ok")):
                    lPos = parseLineToPositions(data)
                    print(lPos)
                
                print(data)
        time.sleep(0.1)  # 稍微延迟以减少CPU使用率

def parseLineToPositions(line):
    # 解析行并转换为目标位置列表
    parts = line.strip().split()
    positions = []
    for part in parts:
        try:
            positions.append(float(part))
        except ValueError:
            # 忽略无法转换为浮点数的部分
            continue
    return positions

# 创建主窗口
root = tk.Tk()
root.title("界面")
root.geometry("412x400")

# 单轴和联动标签
single_axis_label = tk.Label(root, text="单轴")
single_axis_label.grid(row=0, column=0, columnspan=2)

linkage_label = tk.Label(root, text="联动")
linkage_label.grid(row=0, column=6, columnspan=2)

# 单轴按钮
for i in range(6):
    tk.Button(root, text="<<+", command=lambda i=i: on_button_click(f"J{i+1} +")).grid(row=i+1, column=0)
    tk.Label(root, text=f"J{i+1}").grid(row=i+1, column=1)
    tk.Button(root, text="->>", command=lambda i=i: on_button_click(f"J{i+1} -")).grid(row=i+1, column=2)

# 联动按钮
linkage_labels = ["X", "Y", "Z", "A", "B", "C"]
for i, text in enumerate(linkage_labels):
    tk.Button(root, text="<<+", command=lambda text=text: on_button_click(f"{text} +")).grid(row=i+1, column=6)
    tk.Label(root, text=text).grid(row=i+1, column=7)
    tk.Button(root, text="->>", command=lambda text=text: on_button_click(f"{text} -")).grid(row=i+1, column=8)

# 速度输入和确认按钮
speed_label = tk.Label(root, text="速度")
speed_label.grid(row=7, column=0)

speed_entry = tk.Entry(root, width=5)
speed_entry.grid(row=7, column=1)

percent_label = tk.Label(root, text="%")
percent_label.grid(row=7, column=2)

confirm_button = tk.Button(root, text="确定", command=on_confirm)
confirm_button.grid(row=7, column=3)

# 指令输入和发送按钮
command_label = tk.Label(root, text="指令")
command_label.grid(row=8, column=0)

command_entry = tk.Entry(root, width=20)
command_entry.grid(row=8, column=1, columnspan=3)

send_button = tk.Button(root, text="发送", command=on_send_command)
send_button.grid(row=8, column=4)


connect_button = tk.Button(root, text="连接", command=on_connect_command)
connect_button.grid(row=9, column=0)

connect_button = tk.Button(root, text="开始", command=lambda: ser.write(f'!START\n'.encode('utf-8')))
connect_button.grid(row=9, column=1)

connect_button = tk.Button(root, text="JPos", command=lambda: ser.write(f'#GETJPOS\n'.encode('utf-8')))
connect_button.grid(row=9, column=2)

connect_button = tk.Button(root, text="LPos", command=lambda:ser.write(f'#GETLPOS\n'.encode('utf-8')))
connect_button.grid(row=9, column=3)

# 运行主循环
root.mainloop()
