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
def readAccelGyro2():
	alpha = 0.5
        b = degree_gyro2.acc()
	fxg = 0 
	fyg = 0
	fzg = 0
        global ax,ay,az,gx,gy,gz
        ax2,ay2,az2,gx2,gy2,gz2 =  b.get_data()
	fxg = ax2 * alpha + (fxg * (1.0 - alpha))
	fyg = ay2 * alpha + (fyg * (1.0 - alpha))
    	fzg = az2 * alpha + (fzg * (1.0 - alpha))
	pitch = (math.atan2(fxg, math.sqrt(fyg*fyg + fzg*fzg))*180.0)/3.14
	print "pitch = " ,pitch
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
	acc_pitch = math.atan2(ax, az) * 180 / math.pi * -1
        acc_pitch = (acc_pitch + 360) % 360

def calGyro():
	global prev_pitch
	global dt
	global pitch_gyro 
	global count
	if(count == 0):
		prev_pitch = acc_pitch
	pitch_gyro = prev_pitch + gy * dt
	count += 1

def compFilt():
	global pitch_gyro
	global acc_pitch
	global acc_gyro_pitch
	global que 
	global count2
	acc_gyro_pitch = (0.97 * pitch_gyro) + (0.03 * acc_pitch)
	que.append(acc_gyro_pitch)
	
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
	prev_pitch = acc_gyro_pitch
	print acc_gyro_pitch
	count2 += 1
	time.sleep(0.05)
	readAccelGyro2()
def main():
	print "start"
	setup()
	while(True):
		loop()

if __name__ == '__main__':
	main()

