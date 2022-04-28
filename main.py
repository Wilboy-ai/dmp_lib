import dmp_lib as dmp
import plot_lib as pl

import matplotlib.pyplot as plt


dmp_model_x = dmp.dmp(100)

print(dmp_model_x.Ci)
print(dmp_model_x.hi)


x,y,z = pl.read_T("Position_testing_2.xlsx")
#pl.plot_T(x, y, z, 'Position Testing 2')


fdx = dmp_model_x.calc_ft(x)
dmp_model_x.calc_w(x[0], x[len(x)-1], fdx, len(x))


tx = dmp_model_x._get_T(x[len(x)-1], x[0], len(x))


pl.plot_t(x, 'dmp')
pl.plot_t(tx, 'dmp')
#pl.plot_t(ty, 'dmp')
#pl.plot_t(tz, 'dmp')


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z, 'red')
#ax.plot3D(tx, ty, tz, '--b')
ax.set_title("DMP")
plt.show()


