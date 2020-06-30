#!/usr/bin/python3
# -*- coding:utf-8 -*-

import numpy as np

def m2r_(m):
    return pow(m,1/3)

def get_instance_(point1,point2):
    a=point1[0]-point2[0]
    b=point1[1]-point2[1]
    c=point1[2]-point2[2]
    return np.sqrt(np.square(a)+np.square(b)+np.square(c))



if __name__=="__main__":
    # print(m2r(8))
    print(get_instance_(np.array([-1,0,0]),np.array([1,0,0])))