import sysv_ipc
import time
import subprocess 
#proc = subprocess.Popen(["python","thread_test7.py"])
subprocess.Popen(["python","thread_test7.py"])
time.sleep(3)
memory_degree = sysv_ipc.SharedMemory(600)
memory_ang_vel = sysv_ipc.SharedMemory(1234)
a = time.time()
count = 0
while(True):
	degree = memory_degree.read()
	ang_vel = memory_ang_vel.read()
	b = time.time()
	print repr(ang_vel)
	print count,;print b-a ,; print float(degree.rstrip('\x00')),; print float(ang_vel.rstrip('\x00'))
	count = count +1
	time.sleep(0.01)
