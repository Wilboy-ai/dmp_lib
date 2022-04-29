import rtde_control

rtde_c = rtde_control.RTDEControlInterface("192.168.1.100")

velocity = 0.1
acceleration = 0.1

blend = 0.1

point_start = [0.097, -0.380, 0.544, 0.020, -3.172, 0.021, velocity, acceleration, blend]

path = [point_start]


point = [0.097, -0.380, 0.544, 0.020, -3.172, 0.021, velocity, acceleration, blend]



print(len(path))




# Send a linear path with blending in between - (currently uses separate script)
rtde_c.moveL(path)
rtde_c.stopScript()