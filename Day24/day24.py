import re
import numpy as np
from sympy import Matrix

def read_input(data):
    lines = data.split('\n')
    pos_list = []
    vel_list = []
    for line in lines:
        pos, vel = line.split('@')
        x, y, z = pos.split(',')
        vx, vy, vz = vel.split(',')
        pos_list.append((int(x), int(y), int(z)))
        vel_list.append((int(vx), int(vy), int(vz)))
    return pos_list, vel_list

def find_intersection(p1, p2, v1, v2): #
    x1, y1, _ = p1
    x3, y3, _ = p2
    vx1, vy1, _ = v1
    vx3, vy3, _ = v2

    x2, y2 = x1 + vx1, y1 + vy1
    x4, y4 = x3 + vx3, y3 + vy3

    x_numerator = (x1 * y2 - y1 * x2)*(x3 - x4) - (x1 - x2)*(x3 * y4 - y3 * x4)
    y_numerator = (x1 * y2 - y1 * x2)*(y3 - y4) - (y1 - y2)*(x3 * y4 - y3 * x4)
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denom != 0:
        return x_numerator / denom, y_numerator / denom
    else:
        return False, False

def determine_test(p1, p2, v1, v2, min = 200000000000000, max = 400000000000000):
    x_int, y_int = find_intersection(p1, p2, v1, v2)
    
    t1 = (x_int - p1[0]) / v1[0]
    t2 = (x_int - p2[0]) / v2[0]

    if x_int is False and y_int is False:
        return False
    elif t1 < 0 or t2 < 0:
        return False
    elif x_int <= min or y_int <= min or x_int >= max or y_int >= max:
        return False
    else:
        return True

def test_all_pairs(data, min = 200000000000000, max = 400000000000000):
    pos, vel = read_input(data)
    n = len(pos)
    count = 0
    for i, p1 in enumerate(pos):
        for j, p2 in enumerate(pos):
            if i < j:
                v1, v2 = vel[i], vel[j]
                if determine_test(p1, p2, v1, v2, min, max):
                    count += 1
                
    
    return count

def find_min_max(data):
    pos, vel = read_input(data)
    minimum, maximum, min_n, max_n = min_max_helper(pos, vel, 0)
    print("x min: ", min_n, f'{minimum:,}')
    print("x max: ", max_n, f'{maximum:,}')
    minimum, maximum, min_n, max_n = min_max_helper(pos, vel, 1)
    print("y min: ", min_n, f'{minimum:,}')
    print("y max: ", max_n, f'{maximum:,}')
    minimum, maximum, min_n, max_n = min_max_helper(pos, vel, 2)
    print("z min: ", min_n, f'{minimum:,}')
    print("z max: ", max_n, f'{maximum:,}')


def min_max_helper(pos, vel, coord):
    minimum = 1000000000000000000
    maximum = 0 
    min_n = 0
    max_n = 0
    for i in range(len(pos)):
        t = pos[i][coord]
        tv = vel[i][coord]
        if tv < 0:
            if t < minimum:
                minimum = t
                min_n = i
        elif tv >= 0:
            if t > maximum:
                maximum = t
                max_n = i
    return minimum, maximum, min_n, max_n

def solve_for_rock(data, e0, e1, e2, e3):
    #pxn*vyn - pyn*vxn - pxn*vb + pyn*va - vyn*a + vxn*b + vb*a - va*b = 0
    #pxn*vzn - pzn*vxn - pxn*vc + pzn*va - vzn*a + vxn*c + vc*a - va*c = 0
    #eliminate last two terms
    #pxn*vyn - pyn*vxn - pxm*vym + pym*vxm + (pxm - pxn)*vb + (pyn - pym)*va + (vym - vyn)*a + (vxn - vxm)*b
    #pxn*vzn - pzn*vxn - pxm*vzm + pzm*vxm + (pxm - pxn)*vc + (pzn - pzm)*va + (vzm - vzn)*a + (vxn - vxm)*c
    pos, vel = read_input(data)
    px0, py0, pz0 = pos[e0]
    vx0, vy0, vz0 = vel[e0]
    px1, py1, pz1 = pos[e1]
    vx1, vy1, vz1 = vel[e1]
    px2, py2, pz2 = pos[e2]
    vx2, vy2, vz2 = vel[e2]
    px3, py3, pz3 = pos[e3]
    vx3, vy3, vz3 = vel[e3]
    X = np.array([[vy0 - vy1, vx1 - vx0, 0, py1 - py0, px0 - px1, 0],
         [vz0 - vz1, 0, vx1 - vx0, pz1 - pz0, 0, px0 - px1],
         [vy0 - vy2, vx2 - vx0, 0, py2 - py0, px0 - px2, 0],
         [vz0 - vz2, 0, vx2 - vx0, pz2 - pz0, 0, px0 - px2],
         [vy0 - vy3, vx3 - vx0, 0, py3 - py0, px0 - px3, 0],
         [vz0 - vz3, 0, vx3 - vx0, pz3 - pz0, 0, px0 - px3]
    ])
    B = np.array([[py1*vx1 + px0*vy0 - px1*vy1 - py0*vx0, pz1*vx1 + px0*vz0 - px1*vz1 - pz0*vx0,
        py2*vx2 + px0*vy0 - px2*vy2 - py0*vx0, pz2*vx2 + px0*vz0 - px2*vz2 - pz0*vx0,
        py3*vx3 + px0*vy0 - px3*vy3 - py0*vx0, pz3*vx3 + px0*vz0 - px3*vz3 - pz0*vx0]])
    
    aug = Matrix(np.concatenate((X, np.transpose(B)), axis=1))
    aug2 = np.array(aug.rref()[0])
    sol = aug2.T[6]
    return sol, np.matmul(np.linalg.inv(X), B.T)

def main():
    data = open("./Day24/day24.txt").read()  # read the file
    # data = open("./Day24/day24Sample.txt").read()  # read the file
    pos, vel = read_input(data)
    # print(test_all_pairs(data, 7, 27))
    print(test_all_pairs(data))
    sol1, sol2 = solve_for_rock(data, 0, 1, 2, 3)
    print(sol1[:3], sum(sol1[:3]))

main()