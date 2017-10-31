from collections import deque
import pickle


f = open("./Deque_Data/save_data.txt", 'r')

r_d = pickle.load(f)

print r_d

r_d.append(221921991)

print r_d
