import Servo
import degree
import threading

## Initialize
pwm_1 = 1.4
pwm_2 = 1.4
count = 0
## Using threading Timer


def main() :
	global pwm_1
        global count
	a = Servo.servo()
        b = degree.acc()

        f = open("data.txt", 'w')

	que = []

        while(True):
	        a.servo_1(pwm_1)
                a.servo_2(pwm_2)
		if(pwm_1 < 1.43):
           		if(count == 200):
				pwm_1 += 0.001
				print pwm_1
				count = 0
		count += 1
if __name__ == '__main__':
    main()
	
	

