import sysv_ipc
import time
import subprocess 
#proc = subprocess.Popen(["python","thread_test7.py"])
subprocess.Popen(["python","thread_test10.py"])
time.sleep(3)
memory = sysv_ipc.SharedMemory(600)
smp = sysv_ipc.Semaphore(22)
a = time.time()
count = 0
while(True):
	smp.acquire(10)
	vari = memory.read()
	smp.release()
	b = time.time()
	if vari.count('.') >=2:
		break
	if vari.count('-') >=1:
		break
	print count,;print b-a ,; print(vari)
	count = count +1
	time.sleep(0.01)
