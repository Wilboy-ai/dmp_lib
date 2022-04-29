import rtde_receive
from rtde_receive import RTDEReceiveInterface as RTDEReceive
import time
import sys

#rtde_c = rtde_control.RTDEControlInterface("192.168.1.100")
#rtde_c.moveL([0.097, -0.380, 0.544, 0.020, -3.172, 0.021], 0.5, 0.3)
#rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.100")
#actual_q = rtde_r.getActualQ()
#print(actual_q)


frequency = 125
dt = 1/frequency
rtde_r = RTDEReceive("192.168.1.100", frequency)
rtde_r.startFileRecording("trajectory_02.csv", ["actual_TCP_pose"])
print("Data recording started, press [Ctrl-C] to end recording.")

i = 0
try:
    while True:
        start = time.time()
        if i % 10 == 0:
            sys.stdout.write("\r")
            sys.stdout.write("{:3d} samples.".format(i))
            sys.stdout.flush()
        end = time.time()
        duration = end - start

        if duration < dt:
            time.sleep(dt - duration)
        i += 1

except KeyboardInterrupt:
    rtde_r.stopFileRecording()
    print("\nData recording stopped.")

