import Servo
import degree
import time
a = Servo.servo()
b = degree.acc()
pitch_v = 0
start_time = 0
end_time = 0
pwm_1 = 1.1
pwm_2 = 1.22
f = open("data.txt", 'w')

while(True):
        a.servo_1(pwm_1)
        a.servo_2(pwm_2)
	data = "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, b.pitch())
	f.write(data)

	if(start_time == 0):
        	start_time = time.time()
       # print b.pitch()
        end_time = time.time()
        
	if(end_time - start_time >= 5):
        	pwm_1 += 0.01
		start_time = 0
		start_time = 0
		print pwm_1
	pitch_v = b.pitch
#	print b.pitch()
	
	
