import time
from math import sin, cos, asin, atan2, sqrt, degrees, radians
from numpy import array, vstack, hstack
from numpy.linalg import inv

workm = array([[[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
               [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
               [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
               [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
               [[0, -1, 0], [1, 0, 0], [0, 0, 1]]])


def roz(de):
    r = array([[cos(de), -sin(de), 0],
                  [sin(de), cos(de), 0],
                  [0, 0, 1]])
    return r


def roy(de):
    r = array([[cos(de), 0, sin(de)],
                  [0, 1, 0],
                  [-sin(de), 0, cos(de)]])
    return r


def rox(de):
    r = array([[1, 0, 0],
                  [0, cos(de), -sin(de)],
                  [0, sin(de), cos(de)]])
    return r


def work_method(dp, mk):
    global workm
    d_s = array(dp[0:3])
    d_l = d_s@workm[mk]
    dp[0:3] = d_l[0:3][:]


def ikine(al, dl, dp, tp, mk):
    px = dp[0]
    py = dp[1]
    pz = dp[2]
    rx = radians(dp[3])
    ry = radians(dp[4])
    rz = radians(dp[5])
    tx = radians(tp[3])
    ty = radians(tp[4])
    tz = radians(tp[5]+180)
    ppos = array([[px], [py], [pz]])
    tpos = array([[-tp[0]], [-tp[1]], [tp[2]]])
    tran = array([0, 0, 0, 1])
    tpp = vstack([hstack([roz(rz)@roy(ry)@rox(rx), ppos]), tran])
    tt = vstack([hstack([roz(tz)@roy(ty)@rox(tx), tpos]), tran])
    td = tpp @ inv(tt)
    ox = td[0][1]
    ax = td[0][2]
    oy = td[1][1]
    ay = td[1][2]
    oz = td[2][1]
    az = td[2][2]
    x = td[0][3]
    y = td[1][3]
    z = td[2][3]
    q1 = atan2((y - dl[5] * ay), (x - dl[5] * ax))
    A2 = ((x-ax*dl[5])*cos(q1)+(y-ay*dl[5])*sin(q1))-al[0]
    B2 = z-az*dl[5]
    C2 = A2*A2+B2*B2+al[1]*al[1]-al[2]*al[2]-dl[3]*dl[3]
    D2 = 2*A2*al[1]
    E2 = 2*B2*al[1]
    q2 = asin(C2/sqrt(D2*D2+E2*E2))-atan2(E2, D2)
    A3 = sin(q2)*((x-ax*dl[5])*cos(q1)+(y-ay*dl[5])*sin(q1))+((z-az*dl[5])*cos(q2)-al[0]*sin(q2))-al[1]
    B3 = cos(q2)*((x-ax*dl[5])*cos(q1)+(y-ay*dl[5])*sin(q1))+(az*dl[5]-z)*sin(q2)-al[0]*cos(q2)
    q3 = atan2((B3*al[2]-A3*dl[3]), (A3*al[2]+B3*dl[3]))
    A4 = sin(q2+q3)*(ax*cos(q1)+ay*sin(q1))+cos(q2+q3)*az
    B4 = ay*cos(q1)-ax*sin(q1)
    q4 = atan2(-B4*mk, A4*mk)
    A5 = az*cos(q2+q3)*cos(q4)-sin(q4)*(ay*cos(q1)-ax*sin(q1))+sin(q2+q3)*cos(q4)*(ax*cos(q1)+ay*sin(q1))
    B5 = cos(q2+q3)*(ax*cos(q1)+ay*sin(q1))-az*sin(q2+q3)
    q5 = atan2(-A5, B5)
    A6 = cos(q5)*(oz*cos(q2+q3)*cos(q4)-sin(q4)*(oy*cos(q1)-ox*sin(q1))+sin(q2+q3)*cos(q4)*(ox*cos(q1)+oy*sin(q1)))+sin(q5)*(ox*cos(q2+q3)*cos(q1)-oz*sin(q2+q3)+oy*cos(q2+q3)*sin(q1))
    B6 = cos(q4)*(oy*cos(q1)-ox*sin(q1))+oz*cos(q2+q3)*sin(q4)+sin(q2+q3)*sin(q4)*(ox*cos(q1)+oy*sin(q1))
    q6 = atan2(A6, B6)
    return [degrees(q1), degrees(q2), degrees(q3), degrees(q4), degrees(q5), degrees(q6)]


def deg2pul(dp, pul):
    k1 = pul[0] + dp[0]
    k2 = pul[1] + dp[1]
    k3 = pul[2] + dp[2]
    k4 = pul[3] + dp[3]
    k5 = pul[4] + dp[4]
    k6 = pul[5] + dp[5]
    # 将每个元素格式化为小数点后两位
    return [round(k1, 2), round(k2, 2), round(k3, 2), round(k4, 2), round(k5, 2), round(k6, 2)]


def process_line(line, x_offset, y_offset, z_offset):
    parts = line.split()
    if len(parts) != 7:
        raise ValueError("Invalid line format")
    
    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
    # 应用偏移量
    x += x_offset
    y += y_offset
    z += z_offset
    
    # 根据需要，使用 x, y, z 进行你的计算
    a = [35, 146, 52, 0, 0, 0]
    d = [0, 0, 0, 115, 0, 72]
    p = [x, y, z, -90, 70, -90]
    t = [0, 0, 0, 0, 0, 0]
    Q = ikine(a, d, p, t, 1)
    result = deg2pul(Q, [0, 0, 90, 0, 0, 0])
    
    # 生成与原始格式一致的输出
    result_line = f"ok {result[0]} {result[1]} {result[2]} {result[3]} {result[4]} {result[5]}\n"
    return result_line

def main():
    start = time.process_time()

    # 偏移量
    x_offset = 75
    y_offset = -75
    z_offset = 100

    # 读取文件
    with open("input.txt", "r") as file:
        lines = file.readlines()

    results = []
    for line in lines:
        # 处理每一行
        result = process_line(line.strip(), x_offset, y_offset, z_offset)
        results.append(result)
        
    # 将结果写入文件
    with open("output.txt", "w") as file:
        file.writelines(results)
        
    end = time.process_time()
    print("final is in ", end - start)

if __name__ == '__main__':
    main()