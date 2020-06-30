#!/usr/bin/python3
# -*- coding:utf-8 -*-

import numpy as np


class Ball_2D:
    def __init__(self, m, v, loc, r=0.3):
        self.m = m
        self.v = v
        self.loc = loc
        self.r = r


def threeD2twoD(threeDarray):
    return np.array([threeDarray[0], threeDarray[1]])


def twoD2threeD(twoDarray):
    return np.array([twoDarray[0], twoDarray[1], 0])


def normalize(twoDarray):  # 二维向量正则化
    len_ = get_changdu(twoDarray)
    return np.array([twoDarray[0] / len_, twoDarray[1] / len_])
    # return np.array([twoDarray[0]/np.sqrt(np.square(twoDarray[0])+np.square(twoDarray[1])), twoDarray[1]/np.sqrt(np.square(twoDarray[0])+np.square(twoDarray[1]))])


def get_loc(ball, t):
    return ball.loc + ball.v * t


def get_neiji(x, y):
    return x[0] * y[0] + x[1] * y[1]


def get_changdu(twoDarray):
    return np.sqrt(np.square(twoDarray[0])+ np.square(twoDarray[1]))


def set_loc0(v1, v2, r):
    rotate = (np.random.rand() - 0.5) * 0.6 * np.pi  # 随机角度碰撞
    mat = [[np.cos(rotate), -np.sin(rotate)], [np.sin(rotate), np.cos(rotate)]]  # 逆时针旋转rotate
    v = normalize(threeD2twoD(v1 - v2))
    loc = np.dot(v, mat)
    loc1 = twoD2threeD(loc * (-r))
    loc2 = twoD2threeD(loc * r)
    return [loc1, loc2]


def balls_meet_(ball11, ball21):  # r一定
    f_vector = normalize(threeD2twoD(ball21.loc - ball11.loc))
    # f_vector顺时针旋转t°，与x轴重合,  f_vector向量顺时针旋转t° -> 点顺时针旋转t° -> 坐标系逆时针旋转t°
    # 坐标系逆时针转t°，即[[cost,-sint],[sint,cost]],坐标系顺时针转t°，即[[cost,sint],[-sint,cost]]
    rotate_matrix = np.array([[f_vector[0], -f_vector[1]], [f_vector[1], f_vector[0]]])  # 任何向量与该矩阵相乘得到旋转后的坐标
    rotate_matrix_re = np.array([[f_vector[0], f_vector[1]], [-f_vector[1], f_vector[0]]])  # 旋转后的坐标中任何向量与该矩阵相乘得到旋转前的坐标

    new_v1 = np.dot(threeD2twoD(ball11.v), rotate_matrix)
    new_v2 = np.dot(threeD2twoD(ball21.v), rotate_matrix)

    vx_still = new_v1[0] * ball11.m / (ball11.m + ball21.m) + new_v2[0] * ball21.m / (ball11.m + ball21.m)  # 质心速度
    v1_x = 2 * vx_still - new_v1[0]
    v2_x = 2 * vx_still - new_v2[0]

    v1_y = new_v1[1]
    v2_y = new_v2[1]

    # 组装坐标
    v1_after_2D = np.dot(np.array([v1_x, v1_y]), rotate_matrix_re)
    v2_after_2D = np.dot(np.array([v2_x, v2_y]), rotate_matrix_re)

    ball12 = Ball_2D(ball11.m, twoD2threeD(v1_after_2D), ball11.loc, ball11.r)
    ball22 = Ball_2D(ball21.m, twoD2threeD(v2_after_2D), ball21.loc, ball21.r)
    return ball12, ball22


if __name__ == '__main__':
    # ball1 = Ball_(1,np.array([1, 1, 0]),np.array([0, 0, 0]))
    # ball2 = Ball_(1,np.array([-1, 0, 0]),np.array([1, 0, 0]))
    # ball3,ball4=balls_meet_(ball1,ball2)
    # print(ball3.v)
    # print(ball4.v)

    print(set_loc0(np.array([1, 0, 0]), np.array([-1, 0, 0]), 0.5))
    l=[1,2,3,4,5,6]
    for i in l:
        print(i)
