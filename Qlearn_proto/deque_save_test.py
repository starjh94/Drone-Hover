from collections import deque
import pickle

d = deque([10, 20, 30, 40, 50])
f = open("./Deque_Data/save_data.txt", 'w')

pickle.dump(d, f)
f.close()

