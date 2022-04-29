import urx
import math
import dmp_lib as dmp
import plot_lib as pl
import time
import numpy as np

import matplotlib.pyplot as plt


def create_T(x,y,z):
    #fixed orientation
    FO = (0.020, -3.172, 0.021)

    T = []
    for i in range(0, len(x)-1):
        point = (x[i], y[i], z[i], FO[0], FO[1], FO[2])
        T.append(point)
    return T

def run_robot(T):
    a = 0.1
    v = 0.1
    r = 0.1
    thres = 0.01

    rob = urx.Robot('192.168.1.100')
    print("Connected to robot!")
    time.sleep(0.3)

    try:
        rob.movels(T, acc=a, vel=v, radius=r, wait=True, threshold=thres)
        # rob.movel((0.047, -0.341, 0.519, 0.020, -3.172, 0.021), a, v, wait=True)

        rob.close()
        print("Stopped the robot!")
    except:
        rob.close()
        print("Error! Stopped the robot!")

#x,y,z = pl.read_T("T.xlsx")
x,y,z = pl.read_T("Position_testing_2.xlsx", 0.001)
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

#tx = dmp_model_x._get_T(x[len(x)-1], x[0], len(x))
#ty = dmp_model_y._get_T(y[len(y)-1], y[0], len(y))
#tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))

#tx = dmp_model_x._get_T(x[len(x)-1]-0.1, x[0], len(x))
#ty = dmp_model_y._get_T(y[len(y)-1]+0.01, y[0], len(y))
#tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))

tx = dmp_model_x._get_T(-0.090, x[0], len(x))
ty = dmp_model_y._get_T(-0.574, y[0], len(y))
tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z, 'red')
ax.plot3D(tx, ty, tz, '--b')

ax.plot3D(0, 0, 0.130, 'xr')
# plot the plane

xx, yy = np.meshgrid(np.linspace(x[len(x)-1], x[0], 9), np.linspace(y[len(y)-1], y[0], 9))
zz = 0.130 + xx*0
ax.plot_surface(xx, yy, zz)


ax.set_title("DMP Trajectory")
plt.show()


T = create_T(tx,ty,tz)
#T = create_T(x,y,z)
#run_robot(T)











