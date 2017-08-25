import sys, time

import navio.rcinput
import navio.util
import navio.pwm


import Servo
import threading
period1 = 0
period3 = 0

class Manual_control(threading.Thread):
        def run(self):
                global period1
                global period3

                rcin = navio.rcinput.RCInput()

                while(True):
                        period1 = rcin.read(0)
                        period3 = rcin.read(2)

def main():

	manual = Manual_control(name='recv_rc')
	global period1
	global period3
	pwm_1 = 1.22
	pwm_2 = 1.1
	print "start"
	a = Servo.servo()

	manual.daemon = True
	manual.start()
	while(True):
        	a.servo_1(pwm_1 + (int(period3) - 982) * 0.00049 )
        	a.servo_2(pwm_2 + (int(period1) - 982) * 0.00049 )
       		print "pwm_1=%s pwm2=%s" % (pwm_1 + (int(period3) - 982) * 0.00049 ,pwm_2 + (int(period1) - 982 )* 0.00049)
        	time.sleep(0.01)

if __name__ == '__main__':
    main()

