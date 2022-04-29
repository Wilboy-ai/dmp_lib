import urx
import math
import dmp_lib as dmp
import plot_lib as pl
import time
import numpy as np

import matplotlib.pyplot as plt


def create_T(x,y,z, reverse=False):
    #fixed orientation
    FO = (0.020, -3.172, 0.021)

    T = []
    for i in range(0, len(x)-1):
        point = (x[i], y[i], z[i], FO[0], FO[1], FO[2])
        T.append(point)

    if reverse:
        T.reverse()
    return T

def run_robot(T):

    ans = input("Run Trajectory? y/n:\n")

    if ans != "y":
        return -1

    a = 0.3
    v = 0.3
    r = 0.01

    rob = urx.Robot('192.168.1.100')
    print("Connected to robot!")
    time.sleep(0.3)

    try:
        rob.movels(T, acc=a, vel=v, radius=r, wait=True, threshold=0.1)

        time.sleep(1.5)
        print("Returning home")
        rob.movel((0.097, -0.380, 0.544, 0.020, -3.172, 0.021), a, v, wait=True)

        rob.close()
        print("Trajectory Finished!")
    except:
        rob.close()
        print("Error! Stopped the robot!")



rob = urx.Robot('192.168.1.100')
target_pos = rob.getl(wait=True)
#rob.movel((0.097, -0.380, 0.544, 0.020, -3.172, 0.021), 0.3, 0.3, wait=True)
rob.close()


print(target_pos)
print(target_pos[0])
print(target_pos[1])
print(target_pos[2])

#x,y,z = pl.read_T("T.xlsx")
x,y,z = pl.read_T("trajectory_02.xlsx", 0.001)
#pl.plot_T(x, y, z, 'Demonstration Trajectory')

N = 100
dmp_model_x = dmp.dmp(N)
dmp_model_y = dmp.dmp(N)
dmp_model_z = dmp.dmp(N)

fdx = dmp_model_x.calc_ft(x)
dmp_model_x.calc_w(x[0], x[len(x)-1], fdx, len(x))

fdy = dmp_model_y.calc_ft(y)
dmp_model_y.calc_w(y[0], y[len(y)-1], fdy, len(y))

fdz = dmp_model_z.calc_ft(z)
dmp_model_z.calc_w(z[0], z[len(z)-1], fdz, len(z))

tx0 = dmp_model_x._get_T(x[len(x)-1], x[0], len(x))
ty0 = dmp_model_y._get_T(y[len(y)-1], y[0], len(y))
tz0 = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))

#tx = dmp_model_x._get_T(x[len(x)-1]-0.1, x[0], len(x))
#ty = dmp_model_y._get_T(y[len(y)-1]+0.01, y[0], len(y))
#tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))

tx = dmp_model_x._get_T(target_pos[0], x[0], len(x))
ty = dmp_model_y._get_T(target_pos[1], y[0], len(y))
tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))


#tx = dmp_model_x._get_T(0.386, x[0], len(x))
#ty = dmp_model_y._get_T(0.139, y[0], len(y))
#tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))

#tx = dmp_model_x._get_T(0.187, x[0], len(x))
#ty = dmp_model_y._get_T(-0.623, y[0], len(y))
#tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))


#tx = dmp_model_x._get_T(x[len(x)-1], x[0], len(x))
#ty = dmp_model_y._get_T(y[len(y)-1], y[0], len(y))
#tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z, 'red')
ax.plot3D(tx0, ty0, tz0, '--g')
ax.plot3D(tx, ty, tz, '--b')

ax.plot3D(0, 0, 0.130, 'xr')
# plot the plane

ax.legend(["Demonstration", "Original DMP", 'New position DMP'], loc ="lower right")

xx, yy = np.meshgrid(np.linspace(x[len(x)-1], x[0], 2), np.linspace(y[len(y)-1], y[0], 2))
zz = 0.130 + xx*0
ax.plot_surface(xx, yy, zz)

ax.set_title("DMP Trajectory")
plt.show()




T1 = create_T(tx,ty,tz, True)
run_robot(T1)

T = create_T(tx0,ty0,tz0, True)
run_robot(T)









'''
import rtde_control

rtde_c = rtde_control.RTDEControlInterface("192.168.1.100")

velocity = 0.2
acceleration = 0.2

blend = 0.2

point_start = [0.097, -0.380, 0.544, 0.020, -3.172, 0.021, velocity, acceleration, blend]

path = [point_start]

for i in range(0, len(tx0)-1):
    point = [tx0[i], ty0[i], tz0[i], 0.020, -3.172, 0.021, velocity, acceleration, blend]
    path.append(point)
path.append(point_start)

print(len(path))


# Send a linear path with blending in between - (currently uses separate script)
rtde_c.moveL(path)
rtde_c.stopScript()
'''

