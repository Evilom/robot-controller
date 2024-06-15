import tkinter as tk
from tkinter import ttk
from main_logic import handle_button_click, confirm_speed, connect_to_serial, send_command, get_serial_ports, set_move_step

def main():
    root = tk.Tk()
    root.title("Robot Control Panel")
    root.geometry("550x720")  # 设置初始窗口大小
    root.configure(bg='white')  # 设定背景颜色为白色

    # 标题
    title_label = tk.Label(root, text="Robot Control Interface", font=("Arial", 16), bg='white')
    title_label.pack(pady=10)

    # COM端口选择部分
    com_frame = tk.Frame(root, bg='white')
    com_frame.pack(pady=10)

    com_label = tk.Label(com_frame, text="COM Port:", font=("Arial", 12), bg='white')
    com_label.pack(side=tk.LEFT, padx=5)

    # 获取可用的COM端口列表
    ports = get_serial_ports()
    com_value = tk.StringVar()
    com_dropdown = ttk.Combobox(com_frame, textvariable=com_value, values=ports, state='readonly', width=10)
    com_dropdown.pack(side=tk.LEFT, padx=5)

    # 步进设置部分
    step_frame = tk.Frame(root, bg='white')
    step_frame.pack(pady=10)

    step_label = tk.Label(step_frame, text="Step (units):", font=("Arial", 12), bg='white')
    step_label.pack(side=tk.LEFT, padx=5)

    # 可选择的步进值
    step_options = ['0.1', '1', '5', '10']
    step_value = tk.StringVar(value=step_options[1])  # 默认设置为1
    for option in step_options:
        tk.Radiobutton(step_frame, text=option,command=lambda opt=option: set_move_step(opt), variable=step_value,value=option, bg='white').pack(side=tk.LEFT)

    # 单轴和联动按钮布局
    buttons_frame = tk.Frame(root, bg='white')
    buttons_frame.pack(pady=20)

    # 单轴按钮
    single_axis_label = tk.Label(buttons_frame, text="Single Axis", font=("Arial", 12), bg='white')
    single_axis_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    for i in range(6):
        tk.Button(buttons_frame, text=f"J{i+1} +", command=lambda i=i: handle_button_click(f"J{i+1} +"), width=8, height=1).grid(row=i+1, column=0, padx=5, pady=5)
        tk.Button(buttons_frame, text=f"J{i+1} -", command=lambda i=i: handle_button_click(f"J{i+1} -"), width=8, height=1).grid(row=i+1, column=1, padx=5, pady=5)

    # 联动按钮
    linkage_label = tk.Label(buttons_frame, text="Linkage", font=("Arial", 12), bg='white')
    linkage_label.grid(row=0, column=2, columnspan=2, pady=(0, 10))

    linkage_labels = ["X", "Y", "Z", "A", "B", "C"]
    for i, label in enumerate(linkage_labels):
        tk.Button(buttons_frame, text=f"{label} +", command=lambda l=label: handle_button_click(f"{l} +"), width=8, height=1).grid(row=i+1, column=2, padx=5, pady=5)
        tk.Button(buttons_frame, text=f"{label} -", command=lambda l=label: handle_button_click(f"{l} -"), width=8, height=1).grid(row=i+1, column=3, padx=5, pady=5)

    # 速度控制部分
    speed_frame = tk.Frame(root, bg='white')
    speed_frame.pack(pady=10)

    speed_label = tk.Label(speed_frame, text="Speed (%)", font=("Arial", 12), bg='white')
    speed_label.pack(side=tk.LEFT, padx=5)

    speed_entry = tk.Entry(speed_frame, width=10)
    speed_entry.pack(side=tk.LEFT, padx=5)

    confirm_button = tk.Button(speed_frame, text="Confirm", command=lambda: confirm_speed(speed_entry.get()), width=10, height=1)
    confirm_button.pack(side=tk.LEFT, padx=10)

    # 指令输入部分
    command_frame = tk.Frame(root, bg='white')
    command_frame.pack(pady=10)

    command_label = tk.Label(command_frame, text="Command", font=("Arial", 12), bg='white')
    command_label.pack(side=tk.LEFT, padx=5)

    command_entry = tk.Entry(command_frame, width=30)
    command_entry.pack(side=tk.LEFT, padx=5)

    send_button = tk.Button(command_frame, text="Send", command=lambda: send_command(command_entry.get()), width=10, height=1)
    send_button.pack(side=tk.LEFT, padx=10)

    # 底部按钮
    bottom_frame = tk.Frame(root, bg='white')
    bottom_frame.pack(pady=10)

    buttons = [
        ("Connect", lambda: connect_to_serial(com_value.get())),
        ("Start", lambda: send_command('!START')),
        ("Home", lambda: send_command('!HOME')),
        ("Reset", lambda: send_command('!RESET')),
        ("Stop", lambda: send_command('!DISABLE')),
        ("JPos", lambda: send_command('#GETJPOS')),
        ("LPos", lambda: send_command('#GETLPOS')),
    ]

    for idx, (text, cmd) in enumerate(buttons):
        tk.Button(bottom_frame, text=text, command=cmd, width=10, height=1).grid(row=int(idx/4), column=idx%4, padx=(5 if idx else 0), pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()