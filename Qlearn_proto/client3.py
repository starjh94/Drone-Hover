import sysv_ipc
import time
import subprocess 
#proc = subprocess.Popen(["python","thread_test7.py"])
subprocess.Popen(["python","thread_test9.py"])
memory = sysv_ipc.SharedMemory( 1234)
a = time.time()
count = 0
while(True):
	vari = memory.read()
	b = time.time()
	print count,;print b-a ,; print(vari)
	count = count +1
	time.sleep(0.01)

