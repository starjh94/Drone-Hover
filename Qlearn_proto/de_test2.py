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
    		navio.util.check_apm()
    		self.imu = mpu9250_gyro_test.MPU9250()
		#imu = navio.mpu9250.MPU9250()
		self.imu.initialize()
    	def pitch(self):

        	m9a, m9g, m9m = self.imu.getMotion9()
        	return m9a

	def re_gyro(self):
		return self.pitch_v

