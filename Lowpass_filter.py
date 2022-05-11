import csv

import math

class lowpassfilter:
    def __init__(self, cutt_off_frequency, delta_time):
        self.previus_output = -1
        self.delta_time = delta_time
        self.tau = 1/(2*math.pi*cutt_off_frequency*delta_time)
        #self.tau = 1 / (2 * math.pi * cutt_off_frequency)

    def lowpass_filter(self, input):
        if self.previus_output == -1:
            self.previus_output = input
            return self.previus_output

        self.previus_output = (self.tau/(self.delta_time + self.tau)) * self.previus_output + (self.delta_time/(self.delta_time + self.tau)) * input
        return self.previus_output

'''
force1 = np.array([])
force2 = np.array([])
force3 = np.array([])
force4 = np.array([])
force5 = np.array([])
force6 = np.array([])

csv_reader = csv.reader(open('ForceData.csv'), delimiter=',')
line_count = 0
for row in csv_reader:
    if line_count == 0:
        # Remove first line
        line_count += 1
    else:
        force1 = np.append(force1, float(row[0]))
        force2 = np.append(force2, float(row[1]))
        force3 = np.append(force3, float(row[2]))
        force4 = np.append(force4, float(row[3]))
        force5 = np.append(force5, float(row[4]))
        force6 = np.append(force6, float(row[5]))
        line_count += 1

force1 = force1[:100]
force2 = force2[:100]
force3 = force3[:100]
force4 = force4[:100]
force5 = force5[:100]
force6 = force6[:100]

frequency_force1 = fft(force1)
frequency_force2 = fft(force2)
frequency_force3 = fft(force3)
frequency_force4 = fft(force4)
frequency_force5 = fft(force5)
frequency_force6 = fft(force6)

filter = lowpassfilter(40, 0.125)

filtered_force1 = np.array([])
filtered_force2 = np.array([])
filtered_force3 = np.array([])
filtered_force4 = np.array([])
filtered_force5 = np.array([])
filtered_force6 = np.array([])

for x in range(len(force1)):
    filtered_force1 = np.append(filtered_force1, filter.lowpass_filter(force1[x]))
    filtered_force2 = np.append(filtered_force2, filter.lowpass_filter(force2[x]))
    filtered_force3 = np.append(filtered_force3, filter.lowpass_filter(force3[x]))
    filtered_force4 = np.append(filtered_force4, filter.lowpass_filter(force4[x]))
    filtered_force5 = np.append(filtered_force5, filter.lowpass_filter(force5[x]))
    filtered_force6 = np.append(filtered_force6, filter.lowpass_filter(force6[x]))

fig, grid = plt.subplots(6,3)

print(len(force1))

#x_axis = np.linspace(0, len(force1), len(force1))

grid[0,0].plot(force1, label="FFT Force sensor 1")
grid[1,0].plot(force2, label="FFT Force sensor 2")
grid[2,0].plot(force3, label="FFT Force sensor 3")
grid[3,0].plot(force4, label="FFT Force sensor 4")
grid[4,0].plot(force5, label="FFT Force sensor 5")
grid[5,0].plot(force6, label="FFT Force sensor 6")

grid[0,1].plot(frequency_force1, label="Force sensor 1")
grid[1,1].plot(frequency_force2, label="Force sensor 2")
grid[2,1].plot(frequency_force3, label="Force sensor 3")
grid[3,1].plot(frequency_force4, label="Force sensor 4")
grid[4,1].plot(frequency_force5, label="Force sensor 5")
grid[5,1].plot(frequency_force6, label="Force sensor 6")

grid[0,2].plot(filtered_force1, label="Better Force sensor 1")
grid[1,2].plot(filtered_force2, label="Better Force sensor 2")
grid[2,2].plot(filtered_force3, label="Better Force sensor 3")
grid[3,2].plot(filtered_force4, label="Better Force sensor 4")
grid[4,2].plot(filtered_force5, label="Better Force sensor 5")
grid[5,2].plot(filtered_force6, label="Better Force sensor 6")

plt.show()

'''