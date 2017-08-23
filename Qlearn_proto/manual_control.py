import sys, time

import navio.rcinput
import navio.util
import navio.pwm


import Servo
import threading

## Initialize
period1 = 0
period3 = 0
 ## Using threading Timer
def getRCvalue() :
	global period1 
        global period3 
	rcin = navio.rcinput.RCInput()

	period1 = rcin.read(0)
	period3 = rcin.read(2)         
	print period1
	print period3
	threading.Timer(1, getRCvalue).start()
def main() :
	global period1 
        global period3
	pwm_1 = 1.22
	pwm_2 = 1.1
	print "start"
	bperiod1 =0
	bperiod3 =0
 	a = Servo.servo()

    	
    
        getRCvalue()
        while(True):
		
   			a.servo_1(pwm_1 + (int(period1) - 982) * 0.00049 )
			a.servo_2(pwm_2 + (int(period3) - 982) * 0.00049 )
        		print "pwm_1=%s pwm2=%s" % (pwm_1 + (int(period1) - 982) * 0.00049 ,pwm_2 + (int(period3) - 982 )* 0.00049)
			time.sleep(0.01)
		
        
        
    		#pitch_v = b.pitch
    		#print b.pitch()
    
if __name__ == '__main__':
    main()
	
	

