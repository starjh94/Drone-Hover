import degree
import time
a = degree.acc()

while(True):
	
	v = 0 
	for _ in range(10):
		v +=a.pitch()
	print v/10
	time.sleep(0.1)
