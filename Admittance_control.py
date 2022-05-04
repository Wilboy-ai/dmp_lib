import matplotlib.pyplot as plt
import time
import numpy as np
import math

import rtde_control
import rtde_receive
from rtde_receive import RTDEReceiveInterface as RTDEReceive

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.100")
curr_pos = rtde_r.getActualTCPPose()


rtde_c = rtde_control.RTDEControlInterface("192.168.1.100")

velocity = 0.7
acceleration = 0.7
blend = 0.01

dt = 1.0 / 125
lookahead_time = 0.1
gain = 100


# Control matrices
Kp = np.matrix([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
Dp = np.matrix([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
Mp_inv = np.matrix([[2, 0, 0], [0, 2, 0], [0, 0, 2]])

# Environment force
f = np.array([[0], [0], [0]])

#States
#(0.097, -0.380, 0.544, 0.020, -3.172, 0.021)

print(curr_pos[0])
print(curr_pos[1])
print(curr_pos[2])

#curr_pos = rtde_r.getActualTCPPose()
#pd = np.array([[curr_pos[0]], [curr_pos[1]], [curr_pos[2]]])

pd = np.array([[0.097], [-0.380], [0.544]])
pc0 = np.array([[curr_pos[0]], [curr_pos[1]], [curr_pos[2]]])
pcd =  pc0 - pd #np.array([[-0.3], [0], [0.8]])

dpcd = np.array([[0], [0], [0]])


# time contraint
tau = 0.01

# plotting containers
posx = []
posy = []
posz = []

t = 0

f_offset = 20

#while True:
while True:
    F = rtde_r.getActualTCPForce()

    #f = np.array([[F[0]], [F[1]], [F[2]]])
    print(F)
    print(str(F[0]/15) + " | " + str(F[1]/15) + " | " +str(F[2]/15))
    f = np.array([[F[0]/20], [F[1]/20], [F[2]/20]])

    ddpcd = np.dot(Mp_inv, (f - np.dot(Dp, dpcd) - np.dot(Kp, pcd)))
    dpcd = dpcd + tau*ddpcd
    pcd = pcd + tau*dpcd
    pc = pcd + pd

    #rtde_c.moveL([pc[0, 0], pc[1, 0], pc[2, 0], 0.020, -3.172, 0.021], velocity, acceleration, blend)
    rtde_c.servoL([pc[0, 0], pc[1, 0], pc[2, 0], 0.020, -3.172, 0.021], velocity, acceleration, dt, lookahead_time, gain)
    time.sleep(0.01)

    posx.append(pc[0, 0])
    posy.append(pc[1, 0])
    posz.append(pc[2, 0])

    if pc[0, 0] == pd[0, 0] and pc[1, 0] == pd[1, 0] and pc[2, 0] == pd[2, 0]:
        break
    if t >= 10000:
        break
    t = t + 1


 #   curr_pos = rtde_r.getActualTCPPose()
 #   pd = np.array([[curr_pos[0]], [curr_pos[1]], [curr_pos[2]]])

rtde_c.stopScript()

plt.plot(posx, "red")
plt.plot(posy, "green")
plt.plot(posz, "blue")
plt.show()




