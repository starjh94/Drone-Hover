import Servo
import degree_gyro2
import threading
import time
import math

## Initialize
count = 1
count2 = 0
pwm_1 = 1.1
pwm_2 = 1.22
ax = 0.0 
ay = 0.0
az = 0.0
gx = 0.0
gy = 0.0
gz = 0.0
count = 0 
f = open("data.txt", 'w')
t_now = 0
dt = 0
t_prev = 0
prev_pitch = 0.0
acc_pitch = 0.0
pitch_gyro = 0.0
pitch_gyro2 = 0.0
que = []
acc_gyro_pitch = 0.0

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
	
def readAccelGyro():
	b = degree_gyro2.acc()
	
	global ax,ay,az,gx,gy,gz 
	ax,ay,az,gx,gy,gz =  b.get_data()

def cacdt():
	global t_now ,dt,t_prev
	t_now = time.time()
	dt = t_now - t_prev
	t_prev = t_now

def initDt():
	global t_prev
	t_prev = time.time()

def calAccel():
	global ax,ay,az,gx,gy,gz
	global acc_pitch 
	acc_pitch = math.atan2(ax, az) * 180 / math.pi 
        acc_pitch = (acc_pitch + 360) % 360

def calGyro():
	global prev_pitch
	global dt
	global pitch_gyro 
	global count
	global pitch_gyro2
	if(count == 0):
		prev_pitch = acc_pitch
	pitch_gyro = prev_pitch + gy * dt
	pitch_gyro2 = gy * dt
	count += 1

def compFilt():
	global pitch_gyro
	global acc_pitch
	global acc_gyro_pitch
	global que 
	global count2
	acc_gyro_pitch = (0.97 * pitch_gyro) + (0.03 * acc_pitch)
	que.append(acc_gyro_pitch)
	if(len(que) == 10):
		"""
		if(count2 == 100):
			print "C : ", acc_gyro_pitch, "G : ", pitch_gyro, "A : ", acc_pitch
			count2 = 0
		"""
		print "C : ", sum(que,0.0)/len(que) , "G : ", pitch_gyro2, "A : ", acc_pitch
		que.pop(0)
def servoCont():
	global que
	
	a = Servo.servo()
	
	if(acc_gyro_pitch <=180 and acc_gyro_pitch > 5):
		a.servo_1(pwm_1 + (1.0 / 81000.0) * pow(acc_gyro_pitch, 2))
		a.servo_2(pwm_2)
		print "pwm_v1 = %s pwm_v2 = %s \t\t  degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1 + (1.0 / 81000.0) * pow(pitch_aver, 2), pwm_2, acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree, count)
		#print "180down"
	elif(acc_gyro_pitch >180 and acc_gyro_pitch < 355):
		a.servo_1(pwm_1)
		a.servo_2(pwm_2 + (7.0 / 648000.0) * pow(360-acc_gyro_pitch, 2))
		print "pwm_v1 = %s pwm_v2 = %s \t\t degree = C: %s\t<-\tG: %s vs A: %s ---- count : %s" % (pwm_1, pwm_2 + (7.0 / 648000.0) * pow(360-pitch_aver, 2), acc_gyro_pitch, gyro_pitch_degree, acc_pitch_degree, count)
		#print "180up"
	else:
		a.servo_1(pwm_1)
		a.servo_2(pwm_2) 
def setup():
	initDt()

def loop():
	global count
	global count2
	global acc_gyro_pitch
	global prev_pitch
	readAccelGyro()
	cacdt()
	calAccel() 
	calGyro()
	compFilt()
	#servoCont()
	prev_pitch = acc_gyro_pitch
	count2 += 1

def main():
	print "start"
	setup()
	while(True):
		loop()

if __name__ == '__main__':
	main()


