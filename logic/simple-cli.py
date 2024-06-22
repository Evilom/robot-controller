import serial
import time
import sys
import cmd
import os

TOLERANCE = 0.1 
filename = "record.txt"
sername = "/dev/ttyACM0"
ser = ''
a = [35, 146, 52, 0, 0, 0]
d = [0, 0, 0, 115, 0, 72]
p = [222, 0, 198, 0, 90, 0]
t = [0, 0, 0, 0, 0, 0]
pu = [0, 0, 90, 0, 0, 0]


def test(args):
    if len(args) < 6:
        raise ValueError("args must have at least 6 elements.")
    print(f"@{args[0]},{args[1]},{args[2]},{args[3]},{args[4]},{args[5]}\n")
    if checkSerial() == -1:
        return
    message = f"@{args[0]},{args[1]},{args[2]},{args[3]},{args[4]},{args[5]},15\n"
    ser.write(message.encode('utf-8'))

def custom(args):
    if checkSerial() == -1:
        return
    ser.write(args[0])


def start():
    global ser
    ser = serial.Serial(sername, 115200, timeout=1)
    while True:
        print("starting...")
        ser.write(b'!START\n')
        time.sleep(1)
        data = ser.readline().decode()
        if "Started ok" in data:
            print("Dummy started")
            break


def checkSerial():
    if ser == '':
        print("Please run start command first!")
        return -1
    if not ser.is_open:
        print("Port is closed, run start command first")
        return -1
    try:
        ser.read()  # Attempt to read from port
    except serial.SerialException:
        print("Port device disconnected, run start command again")
        return -1
    except AttributeError:
        print("Port not open yet, run start command first")
        return -1
    return 0


def stop():
    while True:
        print("stopping...")
        ser.write(b'!DISABLE\n')
        time.sleep(1)
        data = ser.readline().decode()
        print(data)
        if "ok" in data:
            print("Dummy stopped")
            break


def homing():
    while True:
        print("homing...")
        ser.write(b'!HOME\n')
        time.sleep(1)
        data = ser.readline().decode()
        print(data)
        if "ok" in data:
            print("Dummy homing done")
            break


def calibrate():
    while True:
        print("calibratiing...")
        ser.write(b'#CMDMODE 1\n')
        ser.write(b'!CALIBRATION\n')
        time.sleep(1)
        data = ser.readline().decode()
        print(data)
        if "ok" in data:
            print("Dummy calibratiing done")
            break


def reset():
    while True:
        print("resetting...")
        ser.write(b'#CMDMODE 1\n')
        ser.write(b'!RESET\n')
        time.sleep(1)
        data = ser.readline().decode()
        print(data)
        if "ok" in data:
            print("Dummy resetting done")
            break


def recPosition():
    # ser.write(b'#CMDMODE 3\n')
    # f = open(filename,'w')
    # f.close()
    if checkSerial() == -1:
        return
    data = ser.readline().decode()
    data = ser.readline().decode()
    if not os.path.exists(filename):
        f = open(filename, 'w')
        f.close()
    with open(filename, 'a') as f:
        ser.write(b'#GETLPOS\n')
        while True:
            data = ser.readline().decode()
            if "ok" in data:
                print(data)
                f.write(data)
                break


def dce_kp(node, kp):
    if checkSerial() == -1:
        return
    s = '#SET_DCE_KP ' + node + ' ' + kp + '\n'
    data = s.encode('utf-8')
    ser.write(data)


def dce_ki(node, kp):
    if checkSerial() == -1:
        return
    s = '#SET_DCE_KI ' + node + ' ' + kp + '\n'
    data = s.encode('utf-8')
    ser.write(data)


def dce_kd(node, kp):
    if checkSerial() == -1:
        return
    s = '#SET_DCE_KD ' + node + ' ' + kp + '\n'
    data = s.encode('utf-8')
    ser.write(data)


def node_reboot(node):
    if checkSerial() == -1:
        return
    s = '#REBOOT ' + node + '\n'
    data = s.encode('utf-8')
    ser.write(data)


def playPosition(count):
    # if checkSerial() == -1:
    #     return
    for i in range(count):
        if i == count:
            break
        print("Playing %d " % i)
        with open(filename) as f:
            for line in f:
                target_positions = parseLineToPositions(line)
                command = formatCommand(target_positions)
                print(command)
                ser.write(b'#CMDMODE 0\n')
                ser.write(command)
                waitPosition(target_positions)

def waitPosition(target_positions):
    ser.write(b'#GETLPOS\n')
    data = ser.readline().decode().strip()
    while True:
        if data.startswith('o'):
            time.sleep(0.1)
            if checkPositionReached(data, target_positions):
                print(data)
                break
            ser.write(b'#GETLPOS\n')
        data = ser.readline().decode().strip()



def checkPositionReached(data, target_positions):
    # 解析当前机器人位置
    current_positions = parseLineToPositions(data)
    # 检查每个轴是否在目标位置范围内
    for current, target in zip(current_positions, target_positions):
        if abs(current - target) > TOLERANCE:
            return False
    return True

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

def formatCommand(positions):
    command_str = "@{},{}\n".format(",".join(map(str, positions)), 5)
    return command_str.encode()

def readCurrent():
    # ser1 = serial.Serial("/dev/tty.usbserial-1130", 115200, timeout=1)
    time.sleep(1)
    while True:
        time.sleep(0.5)
        ser.write(b'#GETJCUR\n')
        data = ser.readline().decode()
        print(data)




def weight():
    if checkSerial() == -1:
        return
    # ser.write(b'#CMDMODE 1\n')
    ser.write(b'&0,0,90,0,0,0,160\n')
    waitPosition("0.00 90.00 0.00")
    time.sleep(2)
    ser.write(b'&0,61,45,0,0,0,160\n')


def weight2():
    if checkSerial() == -1:
        return
    # ser.write(b'#CMDMODE 1\n')
    ser.write(b'&0,0,90,0,0,0,10\n')
    waitPosition("0.00 90.00 0.00")


# ok -29.39 21.69 90.02 -0.01 -40.10 0.00


def measure(count):
    if checkSerial() == -1:
        return
    for i in range(count):
        if i == count:
            break
        print("Loop %d " % i)
        ser.write(b'#CMDMODE 3\n')
        ser.write(b'&-34,29,66,-60,-60,0,50\n')
        ser.write(b'&-34,29,66,-30,-1.5,0,50\n')
        # time.sleep(10)
        ser.write(b'&-34,29,66,-30,-60,0,50\n')
        ser.write(b'&0,0,90,0,0,0,60\n')
        # time.sleep(10)


def loop(count):
    if checkSerial() == -1:
        return
    for i in range(count):
        if i == count:
            break
        print("Loop %d " % i)
        ser.write(b'#CMDMODE 1\n')
        ser.write(b'&0,0,90,0,0,0,50\n')
        waitPosition("0.00 90.00 0.00")

        ser.write(b'&-120,72,50,0,-100,0,\n')
        waitPosition("129.22 0.00")

        ser.write(b'&-120,72,50,30,0,0,\n')
        waitPosition("60.00")

        ser.write(b'&0,72,50,30,0,0,\n')
        time.sleep(3.9)
        ser.write(b'&0,0,90,0,0,0,\n')
        waitPosition("0.00 90.00 0.00")

        ser.write(b'&0,-73,180,0,0,0,\n')
        waitPosition("-73.00 180.00")


def home():
    if checkSerial() == -1:
        return
    ser.write(b'#CMDMODE 1\n')
    ser.write(b'&0,-71,180,0,0,0,30\n')


def loop2(count):
    for i in range(count):
        if i == count:
            break
        print("Loop %d " % i)
        # ser.write(b'#CMDMODE 1\n')
        # ser.write(b'&0,0,90,0,0,0,160\n')
        # waitPosition("0.00 90.00 0.00")

        # ser.write(b'&-120,73,129,0,0,0,\n')
        # waitPosition("129.22 0.00")

        ser.write(b'&-120,73.15,50,160,0,0,\n')
        waitPosition("60.00")
        time.sleep(2)

        # ser.write(b'&0,0,90,0,0,0,\n')
        # waitPosition("0.00 90.00 0.00")

        ser.write(b'&0,-71,180,0,0,0,\n')
        waitPosition("-71.00 180.00")
        time.sleep(2)


class DummyCLI(cmd.Cmd):
    completekey = 'tab'
    prompt = 'Dummy-> '

    def do_test(self, args):
        print("Testing dummy....")
        test_args = args.split()
        test(test_args)

    def do_custom(self, args):
        print("Testing dummy....")
        test_args = args.split()
        custom(test_args)

    def do_start(self, args):
        print("starting dummy ...")
        start()

    def do_stop(self, args):
        print("stopping dummy ...")
        stop()

    def do_homing(self, args):
        print("homing dummy ...")
        homing()

    def do_calibrate(self, args):
        print("calibrating dummy ...")
        calibrate()

    def do_reset(self, args):
        print("resetting dummy ...")
        reset()

    def do_loop(self, args):
        if args == '':
            print("You have to enter loop times")
        else:
            times = int(args)
            print("looping dummy activities %d times" % times)
            loop(times)

    def do_position(self, args):
        print("get currently position ...")
        recPosition()

    def do_play(self, args):
        if args == '':
            print("You have to enter play times")
            return
        print("Playing currently position ...")
        times = int(args)
        playPosition(times)

    def do_home(self, args):
        print("return to home position ...")
        home()

    def do_weight(self, args):
        weight()

    def do_weight2(self, args):
        weight2()

    def do_kp(self, args):
        numbers = args.split()
        if len(numbers) < 2:
            print("Usage: kp node p_value")
            return

        dce_kp(numbers[0], numbers[1])

    def do_ki(self, args):
        numbers = args.split()
        if len(numbers) < 2:
            print("Usage: ki node i_value")
            return

        dce_ki(numbers[0], numbers[1])

    def do_kd(self, args):
        numbers = args.split()
        if len(numbers) < 2:
            print("Usage: kd node d_value")
            return

        dce_kd(numbers[0], numbers[1])

    def do_reboot(self, args):
        numbers = args.split()
        if len(numbers) < 1:
            print("Usage: reboot node")
            return

        node_reboot(numbers[0])

    def do_measure(self, args):
        if args == '':
            print("You have to enter measurement loop times")
        else:
            times = int(args)
            print("looping dummy activities %d times" % times)
            measure(times)

    def do_current(self, args):
        readCurrent()

    def do_rgb(self, args):
        if args == '':
            print("You have to enter rgb ring parameters (rgb on/off)")
        else:
            times = args
            if args == 'on':
                print("turn on rgb ring")
                measure(times)
                ser.write(b'#RGB 1\n')
            else:
                print("turn off rgb ring")
                measure(times)
                ser.write(b'#RGB 0\n')

    def do_man(self, args):
        print("manufacturing testing....")
        # ser.write(b'#CMDMODE 3\n')
        # ser.write(b'&-3.21,49.90,66.62,0.26,54.13,0.00,60')
        # ser.write(b'&-3.17,2.88,81.79,0.26,54.10,0.00,60\n')
        # ser.write(b'&32.08,43.00,81.79,0.26,54.10,0.00,60\n')
        # ser.write(b'&0,0,90,0,0,0,\n')
        tp = "#CMDMODE 3"
        ser.write(tp.encode('utf-8'))
        ser.write(b'\n')
        ser.write(b'&-3.21,49.90,66.62,0.26,54.13,0.00,60\n')
        ser.write(b'&-3.17,2.88,81.79,0.26,54.10,0.00,60\n')
        ser.write(b'&32.08,43.00,81.79,0.26,54.10,0.00,60\n')
        ser.write(b'&0,0,90,0,0,0,\n')
        # waitPosition("0.00 90.00 0.00")
        # ser.write(b'&0,0,90,0,0,0,160\n')

    def do_quit(self, args):
        return True

    def do_help(self, arg):
        print("""
        Welcome to Dummy simple command tool!
        Type help to see available commands.
        """)
        super().do_help(arg)


def main(args):
    cli = DummyCLI()
    cli.cmdloop()


if __name__ == '__main__':
    main(sys.argv)
