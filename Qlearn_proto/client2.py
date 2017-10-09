import sysv_ipc
import time
import subprocess 
#proc = subprocess.Popen(["python","thread_test7.py"])
subprocess.Popen(["python","thread_test8.py"])
memory = sysv_ipc.SharedMemory( 1234)
memory2 = sysv_ipc.SharedMemory( 1)
a = time.time()
count = 0
while(True):
	vari = memory.read()
	vari2 =momory2.read()
	b = time.time()
	print count,;print b-a ,; print(vari),;print(vari2)
	count = count +1
	time.sleep(0.01)

