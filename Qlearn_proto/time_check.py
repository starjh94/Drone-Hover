import Servo
import degree
import time
import timer
a = Servo.servo()
b = degree.acc()
t = timer.timer()
pitch_v = 0
while(True):
	if(t.timer_s == 0):
		t.time_start()
	
	print b.pitch()
	t.time_end()
	if(t.time_r() > 5):
		break	
	
#while(True):
#	pitch_v = b.pitch
#	print pitch_v
#	a.servo_2(1.22)
 #       a.servo_1(1.0)	

	
