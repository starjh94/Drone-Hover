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
	threading.Timer(5, every5sec).start()


def main() :
    	a = Servo.servo()
    	b = degree.acc()
    	count = 0
    	f = open("data.txt", 'w')
    	que = []
    	every5sec()
    	while(True):
		que.append(b.pitch())
		if(len(que) == 10):
    			print sum(que,0.0) /len(que)
			que.pop(0)
if __name__ == '__main__':
    main()
	
	

