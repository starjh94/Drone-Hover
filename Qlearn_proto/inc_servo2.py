import Servo
import degree
import threading

## Initialize
pwm_1 = 1.1
pwm_2 = 1.22

## Using threading Timer
def every5sec() :
    	b = degree.acc()
    
    	global pwm_2
    	pwm_2 += 0.01
    
    	#print "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, b.pitch())
    	print "\n\n\n\n\n\n\n\n\n---------------------motor up---------------------"
	threading.Timer(5, every5sec).start()


def main() :
    	a = Servo.servo()
    	b = degree.acc()
    
    	f = open("data.txt", 'w')
    
    	every5sec()
    	while(True):
        	a.servo_1(pwm_1)
        	a.servo_2(pwm_2)
        
        	print "pwm_v1 = %s pwm_v2 = %s degree = %s" % (pwm_1, pwm_2, b.pitch())
		data = "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, b.pitch())
        	f.write(data)
        
    		#pitch_v = b.pitch
    		#print b.pitch()
    
if __name__ == '__main__':
    main()
	
	

