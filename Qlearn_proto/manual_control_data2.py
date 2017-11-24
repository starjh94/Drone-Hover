import subprocess
subprocess.Popen(["python","degree_process.py"])

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
start_time = 0

## Data numpy value initialize ##
np_gyro_degree = np.array([[0, 0]])
np_acc_degree = np.array([[0, 0]])
np_acc_gyro = np.array([[0, 0]])

np_left_motor = np.array([[0, 0]])
np_right_motor = np.array([[0, 0]])

np_ML_data = np.array([[0, 0, 0, 0, 0, 0]])

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
	global np_ML_data
	global start_time	

	pwm_1 = 1.22
	pwm_2 = 1.1
	print "start"
	a = Servo.servo()
	b = degree_gyro.acc()

	timecheck_list = []
	pitch_aver = acc_gyro_pitch = gyro_pitch_degree = b.pitch()
	
	## matplotlib data initialization ##
	"""
	np_gyro_degree = np.array([[0, gyro_pitch_degree]])
	np_acc_degree = np.array([[0, b.pitch()]])
	np_acc_gyro = np.array([[0, acc_gyro_pitch]])
	np_left_motor = np.array([[0, pwm_1]])
	np_right_motor = np.array([[0, pwm_2]])
	"""
	np_ML_data = np.array([[0, acc_gyro_pitch, b.pitch(), gyro_pitch_degree, pwm_1, pwm_2]])	
	

	manual.daemon = True
	manual.start()
	
	start_time = time.time()
	timecheck_list.append(start_time)
	while True:
                                start_action = raw_input("\nI'm ready\nAre you ready?(Y / N): ")

                                if start_action.upper() == "Y":
                                        print "\nGame will be started! "
                                        break
                                else:
                                        print "\nOK! let me do it again ~"

	while(True):
		timecheck_list.append(time.time())
        	loop_time = timecheck_list[1] - timecheck_list[0]
        	timecheck_list.pop(0)

        	acc_pitch_degree = b.pitch()
        	gyro_pitch_degree = b.gyro_pitch(loop_time, gyro_pitch_degree)
        	get_gyro_degree = b.gyro_pitch(loop_time, acc_gyro_pitch)
        	acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))
		
		## servo part ##
		servo_pwm1 = pwm_1 + (int(period3) - 982) * 0.0005
		servo_pwm2 = pwm_2 + (int(period1) - 982) * 0.0005

        	a.servo_1(servo_pwm1)
        	a.servo_2(servo_pwm2)
		
		## for matplotlib ##
        	data_time = time.time() - start_time
		"""
		np_gyro_degree = np.append(np_gyro_degree, [[data_time, gyro_pitch_degree]], axis=0)
        	np_acc_degree = np.append(np_acc_degree, [[data_time, acc_pitch_degree]], axis=0)
        	np_acc_gyro = np.append(np_acc_gyro, [[data_time, acc_gyro_pitch]], axis=0)
		np_left_motor = np.append(np_left_motor, [[data_time, servo_pwm1]], axis=0)
        	np_right_motor = np.append(np_right_motor, [[data_time, servo_pwm2]], axis=0)		
		"""
		np_ML_data = np.append(np_ML_data, [[data_time, acc_gyro_pitch, acc_pitch_degree, gyro_pitch_degree, servo_pwm1, servo_pwm2]], axis=0)		
		
       		print "<time: %.16s> : degree= %.16s    \tpwm_1= %.5s pwm2= %.5s" % (data_time, acc_gyro_pitch, servo_pwm1, servo_pwm2)
		#print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s" % (servo_pwm1, servo_pwm2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree)	
		time.sleep(0.01)
	
if __name__ == '__main__':
	try :
		main()
	except :
		print("finish")
		"""
		np.save('gyro_degree_Data', np_gyro_degree)
                np.save('acc_degree_Data', np_acc_degree)
                np.save('accGyro_degree_Data', np_acc_gyro)
                np.save('left_motor_Data', np_left_motor)
                np.save('right_motor_Data', np_right_motor)
		"""

		np.save('M_L_Data', np_ML_data)

		print "time: %s, number of numpy data: %s" % (time.time() - start_time, len(np_ML_data))
