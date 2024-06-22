import numpy as np
from numpy import cos, sin, deg2rad

def pose_to_transformation(px, py, pz, roll, pitch, yaw):
    roll, pitch, yaw = deg2rad([roll, pitch, yaw])
    R_x = np.array([[1, 0, 0],
                    [0, cos(roll), -sin(roll)],
                    [0, sin(roll), cos(roll)]])
    
    R_y = np.array([[cos(pitch), 0, sin(pitch)],
                    [0, 1, 0],
                    [-sin(pitch), 0, cos(pitch)]])
    
    R_z = np.array([[cos(yaw), -sin(yaw), 0],
                    [sin(yaw), cos(yaw), 0],
                    [0, 0, 1]])
    
    R = R_z @ R_y @ R_x
    T = np.array([[px],
                  [py],
                  [pz]])
    
    transformation = np.vstack((np.hstack((R, T)), [0, 0, 0, 1]))
    return transformation

def rotation_matrix_to_euler_angles(R):
    assert(is_rotation_matrix(R))
    
    sy = np.sqrt(R[0,0] ** 2 + R[1,0] ** 2)
    
    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(R[2,1], R[2,2])
        y = np.arctan2(-R[2,0], sy)
        z = np.arctan2(R[1,0], R[0,0])
    else:
        x = np.arctan2(-R[1,2], R[1,1])
        y = np.arctan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])

def is_rotation_matrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# 不带工具的位姿
pose_no_tool = [224.57, -10.5, 21.11, 180.0, -0.02, 179.99]
# 携带工具的位姿
pose_with_tool = [186.99, -8.01, 111.99, -90.0, -65.92, -89.99]

# 计算齐次变换矩阵
T_no_tool = pose_to_transformation(*pose_no_tool)
T_with_tool = pose_to_transformation(*pose_with_tool)

# 计算工具的变换矩阵
T_tool = np.linalg.inv(T_no_tool) @ T_with_tool

# 提取位置和旋转矩阵
position = T_tool[0:3, 3]
orientation_matrix = T_tool[0:3, 0:3]

# 提取和转换为欧拉角
euler_angles = rotation_matrix_to_euler_angles(orientation_matrix)
euler_angles_degrees = np.degrees(euler_angles)

print("Position:", position.flatten())
print("Orientation matrix:\n", orientation_matrix)
print("Euler angles (degrees):", euler_angles_degrees)
