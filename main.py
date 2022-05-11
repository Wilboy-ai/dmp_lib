import matplotlib.pyplot as plt
import time
import numpy as np
from Lowpass_filter import lowpassfilter

import dmp_lib as dmp
import plot_lib as pl

import rtde_control
import rtde_receive
from rtde_receive import RTDEReceiveInterface as RTDEReceive

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.100")
rtde_c = rtde_control.RTDEControlInterface("192.168.1.100")

def Admittance_con(x, y, z):

    x.reverse()
    y.reverse()
    z.reverse()

    curr_pos = rtde_r.getActualTCPPose()

    velocity = 0.7
    acceleration = 0.7
    blend = 0.01

    dt = 1.0 / 125
    lookahead_time = 0.1
    gain = 100


    # Control matrices

    Kp = np.matrix([[1, 0, 0], [0, 2, 0], [0, 0, 1]])
    Dp = np.matrix([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
    Mp_inv = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    '''
    Kp = np.matrix([[10, 0, 0], [0, 10, 0], [0, 0, 10]])
    Dp = np.matrix([[10, 0, 0], [0, 10, 0], [0, 0, 10]])
    Mp_inv = np.matrix([[10, 0, 0], [0, 10, 0], [0, 0, 10]])
    '''


    # Environment force
    f = np.array([[0], [0], [0]])
    cut_off = 5
    filter_x = lowpassfilter(cut_off, 0.125)
    filter_y = lowpassfilter(cut_off, 0.125)
    filter_z = lowpassfilter(cut_off, 0.125)


    #States
    #(0.097, -0.380, 0.544, 0.020, -3.172, 0.021)

    print(curr_pos[0])
    print(curr_pos[1])
    print(curr_pos[2])


    #pd = np.array([[0.097], [-0.380], [0.544]])
    pd = np.array([[x[0]], [y[0]], [z[0]]])
    pc0 = np.array([[curr_pos[0]], [curr_pos[1]], [curr_pos[2]]])
    pcd = pc0 - pd #np.array([[-0.3], [0], [0.8]])

    dpcd = np.array([[0], [0], [0]])


    # time contraint
    tau = 0.01

    # plotting containers
    posx = []
    posy = []
    posz = []

    t = 0

    f_offset = 20
    try:
        while True:
            F = rtde_r.getActualTCPForce()

            # threshold
            thres_value = 6.0
            fx = 0
            fy = 0
            fz = 0

            F[0] = filter_x.lowpass_filter(F[0])
            F[1] = filter_y.lowpass_filter(F[1])
            F[2] = filter_z.lowpass_filter(F[2])

            if F[0] < -thres_value or F[0] > thres_value:
                fx = F[0] / 20
            if F[1] < -thres_value or F[1] > thres_value:
                fy = F[1] / 20
            if F[2] < -thres_value or F[2] > thres_value:
                fz = F[2] / 20

            f = np.array([[fx], [fy], [fz]])

            ddpcd = np.dot(Mp_inv, (f - np.dot(Dp, dpcd) - np.dot(Kp, pcd)))
            dpcd = dpcd + tau*ddpcd
            pcd = pcd + tau*dpcd
            pc = pcd + pd

            rtde_c.servoL([pc[0, 0], pc[1, 0], pc[2, 0], 1.755, 2.601, 0.009], velocity, acceleration, dt, lookahead_time, gain)
            time.sleep(0.01)

            posx.append(pc[0, 0])
            posy.append(pc[1, 0])
            posz.append(pc[2, 0])

            if abs(abs(pd[0,0]) - abs(pc[0,0])) < 0.001 and abs(abs(pd[1,0]) - abs(pc[1,0])) < 0.001 and abs(abs(pd[2,0]) - abs(pc[2,0])) < 0.001 and t >= len(x) - 1:
                print(f"current point: {rtde_r.getActualTCPPose()[0:3]}")
                print(f"desired point: {pd}")
                print(
                    f"Error: {abs(pd[0, 0]) - abs(pc[0, 0])}, {abs(pd[1, 0]) - abs(pc[1, 0])}, {abs(pd[2, 0]) - abs(pc[2, 0])}")
                break
            if t >= len(x) - 1:
                print(f"current point: {rtde_r.getActualTCPPose()[0:3]}")
                print(f"desired point: {pd}")
                t = t-1
                #break
            t = t + 1

            #curr_pos_new = rtde_r.getActualTCPPose()
            pd = np.array([[x[t]], [y[t]], [z[t]]])

    except KeyboardInterrupt:
        rtde_c.stopScript()
        print("Interrupted")
    rtde_c.stopScript()

    plt.plot(posx, "red")
    plt.plot(posy, "green")
    plt.plot(posz, "blue")
    plt.show()


def main():
    x, y, z = pl.read_T("AdmittanceRecording2.xlsx", 0.001)
    # pl.plot_T(x, y, z, 'Demonstration Trajectory')
    target_pos = rtde_r.getActualTCPPose()[0:3]
    print(target_pos)
    N = 100
    dmp_model_x = dmp.dmp(N)
    dmp_model_y = dmp.dmp(N)
    dmp_model_z = dmp.dmp(N)

    fdx = dmp_model_x.calc_ft(x)
    dmp_model_x.calc_w(x[0], x[len(x) - 1], fdx, len(x))

    fdy = dmp_model_y.calc_ft(y)
    dmp_model_y.calc_w(y[0], y[len(y) - 1], fdy, len(y))

    fdz = dmp_model_z.calc_ft(z)
    dmp_model_z.calc_w(z[0], z[len(z) - 1], fdz, len(z))

    tx0 = dmp_model_x._get_T(x[len(x) - 1], x[0], len(x))
    ty0 = dmp_model_y._get_T(y[len(y) - 1], y[0], len(y))
    tz0 = dmp_model_z._get_T(z[len(z) - 1], z[0], len(z))

    # tx = dmp_model_x._get_T(x[len(x)-1]-0.1, x[0], len(x))
    # ty = dmp_model_y._get_T(y[len(y)-1]+0.01, y[0], len(y))
    # tz = dmp_model_z._get_T(z[len(z)-1], z[0], len(z))

    tx = dmp_model_x._get_T(target_pos[0], x[0], len(x))
    ty = dmp_model_y._get_T(target_pos[1], y[0], len(y))
    tz = dmp_model_z._get_T(z[len(z) - 1], z[0], len(z))

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(x, y, z, 'red')
    ax.plot3D(tx0, ty0, tz0, '--g')
    ax.plot3D(tx, ty, tz, '--b')

    ax.plot3D(0, 0, 0.130, 'xr')
    # plot the plane

    ax.legend(["Demonstration", "Original DMP", 'New position DMP'], loc="lower right")

    xx, yy = np.meshgrid(np.linspace(x[len(x) - 1], x[0], 2), np.linspace(y[len(y) - 1], y[0], 2))
    zz = 0.130 + xx * 0
    ax.plot_surface(xx, yy, zz)

    ax.set_title("DMP Trajectory")
    plt.show()

    Admittance_con(tx0, ty0, tz0)

if __name__ == "__main__":
    main()