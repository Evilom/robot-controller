import tkinter as tk
from tkinter import ttk
from main_logic import handle_button_click, confirm_speed, connect_to_serial, send_command

def main():
    root = tk.Tk()
    root.title("Robot Control Panel")
    root.geometry("550x550")  # 设置初始窗口大小
    root.configure(bg='white')  # 设定背景颜色为白色

    # 标题
    title_label = tk.Label(root, text="Robot Control Interface", font=("Arial", 16), bg='white')
    title_label.pack(pady=10)

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

    connect_button = tk.Button(bottom_frame, text="Connect", command=connect_to_serial, width=10, height=1)
    connect_button.pack(side=tk.LEFT, padx=10)

    start_button = tk.Button(bottom_frame, text="Start", command=lambda: send_command('!START'), width=10, height=1)
    start_button.pack(side=tk.LEFT, padx=10)

    jpos_button = tk.Button(bottom_frame, text="JPos", command=lambda: send_command('#GETJPOS'), width=10, height=1)
    jpos_button.pack(side=tk.LEFT, padx=10)

    lpos_button = tk.Button(bottom_frame, text="LPos", command=lambda: send_command('#GETLPOS'), width=10, height=1)
    lpos_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()
