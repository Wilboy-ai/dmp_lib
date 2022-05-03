import rtde_control
import time

rtde_c = rtde_control.RTDEControlInterface("192.168.1.100", 125)

velocity = 0.1
acceleration = 0.1
blend = 0.1

#point_start = [0.097, -0.380, 0.544, 0.020, -3.172, 0.021, velocity, acceleration, blend]
#path = [point_start]
#point = [0.097, -0.380, 0.544, 0.020, -3.172, 0.021, velocity, acceleration, blend]

#print(len(path))

# Send a linear path with blending in between - (currently uses separate script)

dt = 1.0 / 1
lookahead_time = 0.1
gain = 100

point_start = (0.097, -0.380, 0.544, 0.020, -3.172, 0.021)

for i in range(1, 100):
    start = time.time()
    rtde_c.servoL(point_start, velocity, acceleration, dt, lookahead_time, gain)
    end = time.time()
    duration = end - start
    if duration < dt:
        time.sleep(dt - duration)

rtde_c.servoStop()
rtde_c.stopScript()



