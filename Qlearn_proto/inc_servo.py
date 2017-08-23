import Servo
import degree
import threading

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
	threading.Timer(2, every5sec).start()


def main() :
        a = Servo.servo()
        b = degree.acc()

        f = open("data.txt", 'w')

	que = []

        every5sec()
        while(True):
	        a.servo_1(pwm_1)
                a.servo_2(pwm_2)
                
                que.append(b.pitch())
                
                if(len(que) == 100):
                        average_pitch = sum(que,0.0) /len(que)
        		print "pwm_v1 = %s pwm_v2 = %s degree = %s" % (pwm_1, pwm_2, average_pitch)
               	 	data = "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, average_pitch)
                 	f.write(data)
	                #que.pop(0)
			que[0:10] = []

                #pitch_v = b.pitch
                #print b.pitch()    

if __name__ == '__main__':
    main()
	
	

