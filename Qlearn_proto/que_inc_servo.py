import Servo
import degree
import threading
import time
## Initialize
pwm_1 = 1.1
pwm_2 = 1.22

## Using threading Timer
def every5sec() :
    	b = degree.acc()
    
    	global pwm_1
    	pwm_1 += 0.01
    
    	#print "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, b.pitch())
    	print "\n\n\n\n\n\n\n\n\n---------------------motor up---------------------"
	threading.Timer(5, every5sec).start()


def main() :
        a = Servo.servo()
        b = degree.acc()

        f = open("data.txt", 'w')
	count = 0
	que = []
	que_time = []
        every5sec()
        while(True):
	        a.servo_1(pwm_1)
                a.servo_2(pwm_2)
                que.append(b.pitch())
                que_time.append(time.time())
		if(count >=1):
			print "sensor time == " , que_time[count]-que_time[count-1]
		count +=1
                if(len(que) == 100):
                        average_pitch = sum(que,0.0) /len(que)
        		print "pwm_v1 = %s pwm_v2 = %s degree = %s " % (pwm_1, pwm_2, average_pitch)
               	 	data = "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, average_pitch)
                 	f.write(data)
	                #que.pop(0)
			que[0:10] = []

                #pitch_v = b.pitch
                #print b.pitch()    

if __name__ == '__main__':
    main()
	
	

