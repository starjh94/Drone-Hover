import spidev
import time
import argparse
import sys
import navio.mpu9250
import navio.util
import math
class acc:

    	navio.util.check_apm()

    	imu = navio.mpu9250.MPU9250()
    	imu.initialize()

    	def pitch(self):

        	m9a, m9g, m9m = acc.imu.getMotion9()
        	pitch_v = math.atan2(m9a[0], m9a[2]) * 180 / math.pi
        	#print "pitch_v", pitch_v
	
	
	
		pitch_v = (pitch_v + 360) % 360
	
		return pitch_v

	def gyro_pitch(self, loop_time, previous_pitch):
		m9a, m9g, m9m = acc.imu.getMotion9()
		pitch_gyro = previous_pitch + m9g[1] * loop_time
		return pitch_gyro 

    	def roll(self):

        	m9a, m9g, m9m = acc.imu.getMotion9()
        	roll_v = math.atan2(m9a[1], m9a[2]) * 180 / math.pi
        	return roll_v
"""
        def roll(self):
                        m9a, m9g, m9m = abc.imu.getMotion9()
                        return math.atan(m9a[1]/m9a[2])

        def get_zangle(self):
                        m9a, m9g, m9m = abc.imu.getMotion9()
                        return m9a[2]

"""
