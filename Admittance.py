import matplotlib.pyplot as plt
import time
import numpy as np
import csv

from Lowpass_filter import lowpassfilter

import rtde_control
import rtde_receive
from rtde_receive import RTDEReceiveInterface as RTDEReceive

def Admittance_con(bias1, bias2, bias3):
    rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.100")
    curr_pos = rtde_r.getActualTCPPose()
    csv_file = open('ForceData_drift.csv', 'w')

    csv_writer = csv.writer(csv_file, delimiter=",")
    rtde_c = rtde_control.RTDEControlInterface("192.168.1.100")

    velocity = 0.7
    acceleration = 0.7
    blend = 0.01

    dt = 1.0 / 125
    lookahead_time = 0.1
    gain = 100


    # Control matrices

    Kp = np.matrix([[5, 0, 0], [0, 5, 0], [0, 0, 5]])
    Dp = np.matrix([[5, 0, 0], [0, 5, 0], [0, 0, 5]])
    Mp_inv = np.matrix([[5, 0, 0], [0, 5, 0], [0, 0, 5]])
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
    pd = np.array([[curr_pos[0]], [curr_pos[1]], [curr_pos[2]]])
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

    data1 = np.array([])
    data2 = np.array([])
    data3 = np.array([])
    data4 = np.array([])
    data5 = np.array([])
    data6 = np.array([])
    try:
        while True:
            #curr_pos_new = rtde_r.getActualTCPPose()
            #pd = np.array([[curr_pos_new[0]], [curr_pos_new[1]], [curr_pos_new[2]]])
            F = rtde_r.getActualTCPForce()
            csv_writer.writerow([F[0], F[1], F[2], F[3], F[4], F[5]])
            #print(f"Fx: {F[0]}")
            #print(f"Fy: {F[1]}")
            #print(f"Fz: {F[2]}")
            Fx = filter_x.lowpass_filter(F[0] + bias1)
            Fy = filter_y.lowpass_filter(F[1] + bias2)
            Fz = filter_z.lowpass_filter(F[2] + bias3)
            #print(F)
            #print(str(F[0]/15) + " | " + str(F[1]/15) + " | " +str(F[2]/15))
            f = np.array([[Fx/20], [Fy/20], [Fz/20]])

            ddpcd = np.dot(Mp_inv, (f - np.dot(Dp, dpcd) - np.dot(Kp, pcd)))
            dpcd = dpcd + tau*ddpcd
            pcd = pcd + tau*dpcd
            pc = pcd + pd

            rtde_c.servoL([pc[0, 0], pc[1, 0], pc[2, 0], 1.755, 2.601, 0.009], velocity, acceleration, dt, lookahead_time, gain)
            time.sleep(0.01)

            posx.append(pc[0, 0])
            posy.append(pc[1, 0])
            posz.append(pc[2, 0])

            if pc[0, 0] == pd[0, 0] and pc[1, 0] == pd[1, 0] and pc[2, 0] == pd[2, 0]:
                break
            if t >= 10000:
                break
            t = t + 1

            curr_pos_new = rtde_r.getActualTCPPose()
            pd = np.array([[curr_pos_new[0]], [curr_pos_new[1]], [curr_pos_new[2]]])


    except KeyboardInterrupt:
        rtde_c.stopScript()
        csv_file.close()
        np.save("data1.npy", data1)
        np.save("data2.npy", data2)
        np.save("data3.npy", data3)
        np.save("data4.npy", data4)
        np.save("data5.npy", data5)
        np.save("data6.npy", data6)
        print("Interrupted")
    rtde_c.stopScript()
    csv_file.close()

    plt.plot(posx, "red")
    plt.plot(posy, "green")
    plt.plot(posz, "blue")
    plt.show()