import Servo
import degree_gyro
import threading
import time
## Initialize
count = 1
pwm_1 = 1.1
pwm_2 = 1.22
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
	print "\n\n\n\n\n\n\n\n\n!!!!!!!!!!!!!!!!!!!!! 1sec over !!!!!!!!!!!!!!!!!!!!!\n"

	threading.Timer(1, every1sec).start()

def main() :
    	#pitch_aver = 180
	a = Servo.servo()
    	b = degree_gyro.acc()
	global count    	
	ak_count = 0
	#f = open("data.txt", 'w')
 	he = 1   	
	que = []
	timecheck_list = []    	
	#gyro_pitch_degree = b.pitch()		
	#acc_gyro_pitch = b.pitch()
	pitch_aver = acc_gyro_pitch = gyro_pitch_degree = b.pitch()
	ooo = time.time()
#	every5sec()
	every1sec()
	
	timecheck_list.append(time.time())
    	while(True):
		ddk5 = time.time()
		if(ak_count == 0):
			acc_gyro_pitch = b.pitch()
		#a.servo_1(pwm_1)
        	#a.servo_2(pwm_2)
	
		#print "pwm_v1 = %s pwm_v2 = %s degree = %s ---- count : %s" % (pwm_1, pwm_2, b.pitch(), count)
		timecheck_list.append(time.time())
		#print "loop time : %s" % (timecheck_list[1] - timecheck_list[0])
		loop_time = timecheck_list[1] - timecheck_list[0]
		timecheck_list.pop(0)
		ak_count += 1	
		count += 1		

		"""
		data = "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, acc_pitch_degree)
        	f.write(data)
		"""
		acc_pitch_degree = b.pitch()
		gyro_pitch_degree = b.new_gyro_pitch(loop_time -0.05, acc_gyro_pitch )
		#print "G : ",gyro_pitch_degree, "A : ", b.pitch(), kkk2 - kkk
		acc_gyro_pitch = (0.97 * gyro_pitch_degree) + (0.03 * acc_pitch_degree) 
		#print "%s vs %s : %s" % (acc_pitch_degree, gyro_pitch_degree, acc_gyro_pitch)
		ak_count += 1
		que.append((acc_gyro_pitch))
		
		
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
		
		#time.sleep(0.05)
		
if __name__ == '__main__':
    main()
