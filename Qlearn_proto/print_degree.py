import Servo
import numpy as np
import print_degree_gyro
import threading
import time

## Initialize
count = 1
init_pwm_1 = 1.22
init_pwm_2 = 1.1
#pwm_1 = 1.15
#pwm_2 = 1.3
l_plus_pwm = 0.37
r_plus_pwm = 0.42

"""
np_gyro_degree = np.array([[0, 0]])
np_acc_degree = np.array([[0, 0]])
np_acc_gyro = np.array([[0, 0]])

np_left_motor = np.array([[0, 0]])
np_right_motor = np.array([[0, 0]])
"""
np_acc_degree = np.array([[0, 0]])
np_acc_Xdata = np.array([[0, 0]])
np_acc_Zdata = np.array([[0, 0]])

f = open("data.txt", 'w')

## Using threading Timer
def every5sec() :
    	b = print_degree_gyro.acc()
    
    	global init_pwm_1
    	init_pwm_1 += 0.01
    
    	#print "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, b.pitch())
    	print "\n\n\n\n\n\n\n\n\n---------------------motor up---------------------\n"
	threading.Timer(5, every5sec).start()

def every1sec() :
	global count
	global f
	
	data = "%s sensor data / sec \n" % count
	f.write(data)
	count = 1
	#print "\n\n\n\n\n\n\n\n\n!!!!!!!!!!!!!!!!!!!!! 1sec over !!!!!!!!!!!!!!!!!!!!!\n"

	threading.Timer(1, every1sec).start()

def main() :
    	#pitch_aver = 180
	a = Servo.servo()
    	b = print_degree_gyro.acc()
	global count
	global init_pwm_1
	global init_pwm_2
        global np_gyro_degree
        global np_acc_degree
        global np_acc_gyro
        global np_left_motor
        global np_right_motor
	
	global np_acc_Xdata
	global np_acc_Zdata    	
	###ak_count = 0
	#f = open("data.txt", 'w')
    	
	que = []
	acc_que = []
	timecheck_list = []    	
	#gyro_pitch_degree = b.pitch()		
	#acc_gyro_pitch = b.pitch()
	pitch_aver = acc_gyro_pitch = gyro_pitch_degree = b.pitch()	
	pwm_1 = init_pwm_1
	pwm_2 = init_pwm_2
	
	start_time = time.time() 
        
	
	## matplotlib data initialization ##
	"""
	np_gyro_degree = np.array([[0, gyro_pitch_degree]])
        np_acc_degree = np.array([[0, b.pitch()]])
	np_acc_gyro = np.array([[0, acc_gyro_pitch]])

	np_left_motor = np.array([[0, init_pwm_1]])
	np_right_motor = np.array([[0, init_pwm_2]])
	"""
	acc_x, acc_z, _ = b.pitchMore()
	np_acc_degree = np.array([[0, b.pitch()]])
	np_acc_Xdata = np.array([[0, acc_x]])
	np_acc_Zdata = np.array([[0, acc_z]])	

	#every5sec()
	every1sec()
	
	timecheck_list.append(time.time())
    	while(True):
		"""
		if(ak_count == 0):
			acc_gyro_pitch = b.pitch()
		"""
		#a.servo_1(pwm_1)
        	#a.servo_2(pwm_2)
	
		#print "pwm_v1 = %s pwm_v2 = %s degree = %s ---- count : %s" % (pwm_1, pwm_2, b.pitch(), count)
		timecheck_list.append(time.time())
		#print "loop time : %s" % (timecheck_list[1] - timecheck_list[0])
		
		loop_time = timecheck_list[1] - timecheck_list[0]
		timecheck_list.pop(0)
			
		#count += 1		

		"""
		data = "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, acc_pitch_degree)
        	f.write(data)
		"""
		
		acc_x, acc_z, acc_pitch_degree = b.pitchMore()
		axis3_info, acc_3axis = b.pitch_3axis()		
		"""	
		acc_que.append(acc_pitch_degree)
		if(len(acc_que) == 10):
			acc_pitch_degree = sum(acc_que, 0.0)/len(acc_que)
			acc_que.pop(0)
		"""
		"""
		gyro_pitch_degree = b.gyro_pitch(loop_time, acc_gyro_pitch)
		acc_gyro_pitch = (0.97 * gyro_pitch_degree) + (0.03 * acc_pitch_degree) 
		"""
		gyro_pitch_degree = b.gyro_pitch(loop_time, acc_gyro_pitch)
                acc_gyro_pitch = (0.97 * b.gyro_pitch(loop_time, acc_gyro_pitch)) + (0.03 * acc_pitch_degree) 
		#print "%s vs %s : %s" % (acc_pitch_degree, gyro_pitch_degree, acc_gyro_pitch)
		time_count = time.time()
		#que.append((acc_gyro_pitch))
		
		## for matplotlib ##
                """
		np_gyro_degree = np.append(np_gyro_degree, [[time.time() - start_time, gyro_pitch_degree]], axis=0)
                np_acc_degree = np.append(np_acc_degree, [[time.time() - start_time, acc_pitch_degree]], axis=0)
                np_acc_gyro = np.append(np_acc_gyro, [[time.time() - start_time, acc_gyro_pitch]], axis=0)
		
		np_left_motor = np.append(np_left_motor, [[time.time() - start_time, pwm_1]], axis=0)
		np_right_motor = np.append(np_right_motor, [[time.time() - start_time, pwm_2]], axis=0)		
		"""
		np_acc_degree = np.append(np_acc_degree, [[time.time() - start_time, acc_pitch_degree]], axis=0)
		np_acc_Xdata = np.append(np_acc_Xdata, [[time.time() - start_time, acc_x]], axis=0)
        	np_acc_Zdata = np.append(np_acc_Zdata, [[time.time() - start_time, acc_z]], axis=0)
		

		#print "degree = C: %s\t<-\tG: %s vs A: %s .=. A_3: %s    //    X/Z: %s---- count : %s" % (acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree, acc_3axis ,acc_x/acc_z ,count)
		print "A: %s .=. A_3: %s    //    X: %s , Z: %s , X/Z: %s vs 3axis-info: %s ---- count: %s" % ( acc_pitch_degree, acc_3axis ,acc_x, acc_z ,acc_x/acc_z, axis3_info ,count)

		
		count += 1
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
		np.save('acc_degree_Data', np_acc_degree)
		np.save('acc_X_Data', np_acc_Xdata)
		np.save('acc_Z_Data', np_acc_Zdata)
