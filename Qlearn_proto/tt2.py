import spidev
import time
import argparse
import sys
import navio.mpu9250
import navio.util
import math
import tt3
a = tt3.comp_filt()
navio.util.check_apm()

imu = navio.mpu9250.MPU9250()
imu.initialize()


while(True):
	m9a, m9g, m9m = imu.getMotion9()
	imu.read_gyro()
	#print m9g[0],m9g[1], m9g[2]
	#a.attitude3(float(m9a[0]),float(m9a[1]),float(m9a[2]),float(m9g[0]),float(m9g[1]),float(m9g[2]),float(m9m[0]),float(m9m[1]),float(m9m[2]))
	#pitch = 180 * math.atan(m9a[1]/math.sqrt(m9a[0]*m9a[0] + m9a[2]*m9a[2]))/ math.pi
	#print "!!!!!!!!!!!==",pitch 
	print m9a[0] , m9a[1], m9a[2]
