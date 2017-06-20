import numpy as np
import matplotlib.pyplot as plt

"""
x = np.arange(0.0, 10 * np.pi, 0.1)
print x

sin_y = np.sin(x)
cos_y = np.cos(x)
"""
arr1 = np.load('/Users/Taewoo/Desktop/project/Drone-Hover/Qlearn_proto/gyro_degree_Data.npy')
arr2 = np.load('/Users/Taewoo/Desktop/project/Drone-Hover/Qlearn_proto/acc_degree_Data.npy')
arr3 = np.load('/Users/Taewoo/Desktop/project/Drone-Hover/Qlearn_proto/accGyro_degree_Data.npy')
print arr1

plt.ylim(-120, 120)

plt.plot(arr1[:, 0], arr1[:, 1], 'r.', label = 'Gyro Degree')
plt.plot(arr2[:, 0], arr2[:, 1], 'b.', label = 'Acc Degree')
plt.plot(arr3[:, 0], arr3[:, 1], 'g*', label = 'Complementary Degree')


plt.legend(loc='upper left')
plt.show()