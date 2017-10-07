import spidev
import time
import argparse
import sys
import mpu9250_gyro_test
import navio.mpu9250
import navio.util
import math
import tt3
class acc:
	def __init__(self):
		self.pitch_V=0.0
		self.pitch_gyro=0.0
		self.m9a=0.0
    		navio.util.check_apm()
    		self.imu = mpu9250_gyro_test.MPU9250()
		#imu = navio.mpu9250.MPU9250()
		self.imu.initialize()
    	def pitch(self):

        	m9a, m9g, m9m = self.imu.getMotion9()
		self.pitch_v = -math.atan2(m9a[0], m9a[2]) * 180 / math.pi
        

	def gyro_pitch(self, loop_time, previous_pitch):
				
		
		m9a, m9g, m9m = self.imu.getMotion9()
		
		pitch_gyro = previous_pitch + m9g[1] * loop_time
		if (pitch_gyro > -180 and pitch_gyro < 180):
			pass
		elif (pitch_gyro <= -180):
			pitch_gyro = 360 + pitch_gyro	## x = 180 - ( abs(x) - 180 )	 	
		else: 	## (pitch_gyro >= 180)
			pitch_gyro = -360 + pitch_gyro 
	def re_gyro(self):
		return self.pitch_v

    	def roll(self):

        	m9a, m9g, m9m = acc.imu.getMotion9()
        	roll_v = math.atan2(m9a[1], m9a[2]) * 180 / math.pi
        	return roll_v
