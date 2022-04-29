import dmp_lib as dmp
import plot_lib as pl

import matplotlib.pyplot as plt

#x,y,z = pl.read_T("T.xlsx")
x,y,z = pl.read_T("Position_testing_2.xlsx")
#pl.plot_T(x, y, z, 'Demonstration Trajectory')


dmp_model_x = dmp.dmp(150)
dmp_model_y = dmp.dmp(150)
dmp_model_z = dmp.dmp(150)


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

tx = dmp_model_x._get_T(x[len(x)-1], x[0] + 0.1, len(x))
ty = dmp_model_y._get_T(y[len(y)-1], y[0] + 0.1, len(y))
tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))



fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z, 'red')
ax.plot3D(tx, ty, tz, '--b')
ax.set_title("DMP")
plt.show()


