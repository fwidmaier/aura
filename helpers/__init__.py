import numpy as np


def normalize(x):
    x /= np.linalg.norm(x)
    return x


def rotate_y(x, alpha):
    alpha=np.radians(alpha)
    ry = np.array([[np.cos(alpha), 0., np.sin(alpha)], [0., 1., 0.], [-np.sin(alpha), 0., np.cos(alpha)]])
    return np.dot(ry, x)


def rotate_x(x, alpha):
    alpha = np.radians(alpha)
    rx = np.array([[1., 0., 0.], [0., np.cos(alpha), -np.sin(alpha)], [0., np.sin(alpha), np.cos(alpha)]])
    return np.dot(rx, x)


def rotate_z(x, alpha):
    alpha = np.radians(alpha)
    rz = np.array([[np.cos(alpha), -np.sin(alpha), 0.], [np.sin(alpha), np.cos(alpha), 0.], [0., 0., 1.]])
    return np.dot(rz, x)
