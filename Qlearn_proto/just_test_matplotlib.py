import Servo
import degree_gyro
import threading
import time
import numpy as np

## Initialize
count = 1
#pwm_1 = 1.1
#pwm_2 = 1.22
pwm_1 = 1.15
pwm_2 = 1.3
l_plus_pwm = 0.42
r_plus_pwm = 0.37
f = open("data.txt", 'w')

## Using threading Timer
def every5sec() :
    	b = degree_gyro.acc()
    
    	global pwm_1
    	pwm_1 += 0.01
    
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
    	b = degree_gyro.acc()
	global count    	
	###ak_count = 0
	#f = open("data.txt", 'w')
    	
	que = []
	acc_que = []
	timecheck_list = []
	#gyro_pitch_degree = b.pitch()		
	#acc_gyro_pitch = b.pitch()
	pitch_aver = acc_gyro_pitch = gyro_pitch_degree = b.pitch()
	
	time_count = time.time()
	
	np_gyro_degree = np.array([[0, gyro_pitch_degree]])
	np_acc_degree = np.array([[0, b.pitch()]])
	np_acc_gyro = np.array([[0, acc_gyro_pitch]])    	

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
		
		acc_pitch_degree = b.pitch()
		
		acc_que.append(acc_pitch_degree)
		if(len(acc_que) == 10):
			acc_pitch_degree = sum(acc_que, 0.0)/len(acc_que)
			acc_que.pop(0)
	
		gyro_pitch_degree = b.gyro_pitch(loop_time, acc_gyro_pitch)
		acc_gyro_pitch = (0.97 * gyro_pitch_degree) + (0.03 * acc_pitch_degree) 
		#print "%s vs %s : %s" % (acc_pitch_degree, gyro_pitch_degree, acc_gyro_pitch)
		#que.append((acc_gyro_pitch))
		

		## for matplotlib ##
		np_gyro_degree = np.append(np_gyro_degree, [[time.time() - time_count, gyro_pitch_degree]], axis=0)
        	np_acc_degree = np.append(np_acc_degree, [[time.time() - time_count, acc_pitch_degree]], axis=0)
        	np_acc_gyro = np.append(np_acc_gyro, [[time.time() - time_count, acc_gyro_pitch]], axis=0)
		
		time_count = time.time()

		np.save('gyro_degree_Data', np_gyro_degree)
		np.save('acc_degree_Data', np_acc_degree)
		np.save('accGyro_degree_Data', np_acc_gyro)
		
		"""
		## <Control Code> Use Queue & Degree : 0 ~ 360 ##

		if(len(que) == 10):
			pitch_aver = sum(que,0.0)/len(que)
    			#print "pwm_v1 = %s pwm_v2 = %s degree = %s ---- count : %s" % (pwm_1, pwm_2, pitch_aver, count)
			count += 1
			que.pop(0)
		if(pitch_aver <=180 and pitch_aver >5):
			a.servo_1(pwm_1 + (1.0 / 81000.0) * pow(pitch_aver, 2))
			a.servo_2(pwm_2)
			print "pwm_v1 = %s pwm_v2 = %s \t\t  degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 + (1.0 / 81000.0) * pow(pitch_aver, 2), pwm_2, pitch_aver, gyro_pitch_degree, acc_pitch_degree, count)
			#print "180down"
		elif(pitch_aver >180 and pitch_aver < 355):
			a.servo_1(pwm_1)
			a.servo_2(pwm_2 + (7.0 / 648000.0) * pow(360-pitch_aver, 2))
			print "pwm_v1 = %s pwm_v2 = %s \t\t degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2 + (7.0 / 648000.0) * pow(360-pitch_aver, 2), pitch_aver, gyro_pitch_degree, acc_pitch_degree, count)
			#print "180up"
		else:
		        a.servo_1(pwm_1)
                        a.servo_2(pwm_2)
			print "pwm_v1 = %s pwm_v2 = %s \t\t degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2, pitch_aver, gyro_pitch_degree, acc_pitch_degree, count)
		"""		
		"""
		## <Control Code> NO Queue & Degree : 0 ~ 360 ##
		
		if(acc_gyro_pitch <=180 and acc_gyro_pitch >5):
                        a.servo_1(pwm_1 + (1.0 / 81000.0) * pow(acc_gyro_pitch, 2))
                        a.servo_2(pwm_2)
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 + (1.0 / 81000.0) * pow(acc_gyro_pitch, 2), pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180down"
                elif(acc_gyro_pitch >180 and acc_gyro_pitch < 355):
                        a.servo_1(pwm_1)
                        a.servo_2(pwm_2 + (7.0 / 648000.0) * pow(360-acc_gyro_pitch, 2))
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2 + (7.0 / 648000.0) * pow(360-acc_gyro_pitch, 2), acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180up"
                else:
                        a.servo_1(pwm_1)
                        a.servo_2(pwm_2)
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree, count)
		"""


		"""

		## <Basic_Control Code> NO Queue & Degree : -180 ~ 180 ##

                if(acc_gyro_pitch >= -70 and acc_gyro_pitch < -5):
                        a.servo_1(pwm_1 + (0.42 / 4900.0) * pow(abs(acc_gyro_pitch), 2))
                        a.servo_2(pwm_2)
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 + (0.42 / 4900.0) * pow(abs(acc_gyro_pitch), 2), pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180down"
		elif(acc_gyro_pitch < -70 and acc_gyro_pitch >= -180):
			a.servo_1(pwm_1 + l_plus_pwm)
                        a.servo_2(pwm_2)
			print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 + l_plus_pwm, pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                elif(acc_gyro_pitch <= 70 and acc_gyro_pitch > 5):
                        a.servo_1(pwm_1)
                        a.servo_2(pwm_2 + (0.37 / 4900.0) * pow(acc_gyro_pitch, 2))
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2 + (0.37 / 4900.0) * pow(acc_gyro_pitch, 2), acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180up"
		elif(acc_gyro_pitch < 180 and acc_gyro_pitch > 90):
			a.servo_1(pwm_1)
                        a.servo_2(pwm_2 + r_plus_pwm)
			print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2 + r_plus_pwm, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree, count)
                else:
                        a.servo_1(pwm_1)
                        a.servo_2(pwm_2)
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree, count)
		time_count2 = time.time()

		"""
		"""
		## <Test_Control Code> NO Queue & Degree : -180 ~ 180 ##

                if(acc_gyro_pitch >= -180 and acc_gyro_pitch < -5):
                        a.servo_1(pwm_1 + (0.4 / 32400.0) * pow(abs(acc_gyro_pitch), 2))
                        a.servo_2(pwm_2 - (0.18 / 32400.0) * pow(abs(acc_gyro_pitch),2))
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 + (1.0 / 81000.0) * pow(abs(acc_gyro_pitch), 2), pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180down"
                elif(acc_gyro_pitch <= 180 and acc_gyro_pitch > 5):
                        a.servo_1(pwm_1 - (0.2 / 32400.0) * pow(acc_gyro_pitch, 2))
                        a.servo_2(pwm_2 + (0.35 / 32400.0) * pow(acc_gyro_pitch, 2))
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2 + (7.0 / 648000.0) * pow(acc_gyro_pitch, 2), acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180up"
                else:
                        a.servo_1(pwm_1)
                        a.servo_2(pwm_2)
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree, count)
		"""
		"""
		## <Test2_Control Code> NO Queue & Degree : -180 ~ 180 ##
		time_count1 = time.time()
                if(acc_gyro_pitch >= -180 and acc_gyro_pitch < -5):
                        a.servo_1(pwm_1 + (0.4 / 32400.0) * pow(abs(acc_gyro_pitch), 2))
                        a.servo_2(pwm_2)
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 + (1.0 / 81000.0) * pow(abs(acc_gyro_pitch), 2), pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180down"
                elif(acc_gyro_pitch <= 180 and acc_gyro_pitch > 5):
                        a.servo_1(pwm_1)
                        a.servo_2(pwm_2 + (0.35 / 32400.0) * pow(acc_gyro_pitch, 2))
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2 + (7.0 / 648000.0) * pow(acc_gyro_pitch, 2), acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180up"
                else:
                        a.servo_1(pwm_1)
                        a.servo_2(pwm_2)
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree, count)
		"""
                ## <Basic_Control Code> NO Queue & Degree : -180 ~ 180 ##

                if(acc_gyro_pitch < 0 ):
                        a.servo_1(pwm_1 - 0.5 * acc_gyro_pitch/90 )
                        a.servo_2(pwm_2)
                        print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 - 0.5 * acc_gyro_pitch/90 , pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
                        #print "180down"
                else:
                        a.servo_1(pwm_1 )
                        a.servo_2(pwm_2 )
			print "pwm_v1 = %s pwm_v2 = %s degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 , pwm_2 + 0.15, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree ,count)
		count += 1
		time.sleep(0.05)

if __name__ == '__main__':
    main()