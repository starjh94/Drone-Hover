import sys, time

import navio.rcinput
import navio.util
import navio.pwm
import degree_gyro
import numpy as np

import Servo
import threading
period1 = 0
period3 = 0

## Data numpy value initialize ##
np_gyro_degree = np.array([[0, 0]])
np_acc_degree = np.array([[0, 0]])
np_acc_gyro = np.array([[0, 0]])

np_left_motor = np.array([[0, 0]])
np_right_motor = np.array([[0, 0]])

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
	global np_gyro_degree
	global np_acc_degree
	global np_acc_gyro
	global np_left_motor
	global np_right_motor

	pwm_1 = 1.22
	pwm_2 = 1.1
	print "start"
	a = Servo.servo()
	b = degree_gyro.acc()

	timecheck_list = []
	pitch_aver = acc_gyro_pitch = gyro_pitch_degree = b.pitch()
	
	## matplotlib data initialization ##
	np_gyro_degree = np.array([[0, gyro_pitch_degree]])
	np_acc_degree = np.array([[0, b.pitch()]])
	np_acc_gyro = np.array([[0, acc_gyro_pitch]])

	np_left_motor = np.array([[0, pwm_1]])
	np_right_motor = np.array([[0, pwm_2]])
	
	manual.daemon = True
	manual.start()
	
	start_time = time.time()
	timecheck_list.append(start_time)
	while(True):
		timecheck_list.append(time.time())
        	loop_time = timecheck_list[1] - timecheck_list[0]
        	timecheck_list.pop(0)

        	acc_pitch_degree = b.pitch()
        	gyro_pitch_degree = b.gyro_pitch(loop_time, gyro_pitch_degree)
        	get_gyro_degree = b.gyro_pitch(loop_time, acc_gyro_pitch)
        	acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))

		
        	a.servo_1(pwm_1 + (int(period3) - 982) * 0.00049 )
        	a.servo_2(pwm_2 + (int(period1) - 982) * 0.00049 )
       		print "pwm_1=%s pwm2=%s" % (pwm_1 + (int(period3) - 982) * 0.00049 ,pwm_2 + (int(period1) - 982 )* 0.00049)

		## for matplotlib ##
        	np_gyro_degree = np.append(np_gyro_degree, [[time.time() - start_time, gyro_pitch_degree]], axis=0)
        	np_acc_degree = np.append(np_acc_degree, [[time.time() - start_time, acc_pitch_degree]], axis=0)
        	np_acc_gyro = np.append(np_acc_gyro, [[time.time() - start_time, acc_gyro_pitch]], axis=0)

		np_left_motor = np.append(np_left_motor, [[time.time() - start_time, pwm_1 + (int(period3) - 982) * 0.00049]], axis=0)
        	np_right_motor = np.append(np_right_motor, [[time.time() - start_time, pwm_2 + (int(period1) - 982) * 0.00049]], axis=0)		

		time.sleep(0.01)
	
if __name__ == '__main__':
	try :
		main()
	except :
		print("finish")
		np.save('gyro_degree_Data', np_gyro_degree)
                np.save('acc_degree_Data', np_acc_degree)
                np.save('accGyro_degree_Data', np_acc_gyro)

                np.save('left_motor_Data', np_left_motor)
                np.save('right_motor_Data', np_right_motor)
