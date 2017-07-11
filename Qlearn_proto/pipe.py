import Servo
import degree
import threading
import subprocess
## Initialize
proc = subprocess.Popen("/home/pi/Navio2/C++/Examples/AHRS/./AHRS", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
    
    	f = open("datatt.txt", 'w')
	inpuk = "hello \n"
	every5sec()
    	while(True):
 		#proc.stdin.write(inpuk )
		c = proc.stdout.readline().rstrip("\n")    
        	print "pwm_v1 = %s pwm_v2 = %s degree = %s" % (pwm_1, pwm_2, c)
		data = "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, c)
        	f.write(data)
        
    
if __name__ == '__main__':
    main()
	
	

