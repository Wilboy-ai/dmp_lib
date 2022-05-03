import rtde_receive
from rtde_receive import RTDEReceiveInterface as RTDEReceive
import time
import sys

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.100")


frequency = 125
dt = 1/frequency
rtde_r = RTDEReceive("192.168.1.100", frequency)
rtde_r.startFileRecording("ForceData.csv", ["actual_TCP_force"])
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

