import rtde_receive
from rtde_receive import RTDEReceiveInterface as RTDEReceive
import time
import multiprocessing
import sys

from Admittance import Admittance_con

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.100")


def recording():
    time.sleep(2)
    frequency = 125
    dt = 1/frequency
    rtde_r = RTDEReceive("192.168.1.100", frequency)
    rtde_r.startFileRecording("AdmittanceRecording2.csv", ["actual_TCP_pose"])
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


if __name__ == "__main__":

    p1 = multiprocessing.Process(name='p1', target=Admittance_con)
    p = multiprocessing.Process(name='p', target=recording)
    p1.start()
    p.start()

