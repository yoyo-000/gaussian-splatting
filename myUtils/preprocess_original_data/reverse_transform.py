import numpy as np
from scipy.spatial.transform import Rotation as RT

def quaternion_to_rotation_matrix(quaternion):
    """将四元数转换为旋转矩阵"""
    w, x, y, z = quaternion
    R = np.array(
        [
            [1 - 2 * (y**2 + z**2), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x**2 + z**2), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x**2 + y**2)],
        ]
    )
    return R

def transform_to_world_quaternion(quaternion_prime, t_prime):
    R_T = quaternion_to_rotation_matrix(quaternion_prime)

    # 计算世界空间的旋转矩阵 R_world
    R_world = R_T.T
    T_world = -np.dot(R_world, t_prime)

    # 计算世界空间的四元数
    quaternion_world = RT.from_matrix(R_world).as_quat(scalar_first=True)

    return quaternion_world, T_world


quaternion_prime = np.array([0.3928474941367159 ,-0.3928474941367159, 0.5879377912249756, 0.5879377912249756  ])
t_prime = np.array([-0.0030732534787048685 ,-4.650953542620706e-09, 0.3997314340967971 ])
a,b = transform_to_world_quaternion(quaternion_prime, t_prime)
print(a)
print(b)