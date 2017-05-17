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
	pitch_v = 0
        m9a, m9g, m9m = acc.imu.getMotion9()
        acc_v = math.atan2(m9a[0], m9a[2]) * 180 / math.pi
        #pitch_v = (pitch_v + 360) % 360
	#gy_x = m9g[0]
	gy_y = m9g[1]
	dgy_x = gy_y /131.
	pitch_v = (0.95 * (pitch_v + (dgy_x * 1))) + (0.05 * acc_v)
	print dgy_x
	return pitch_v



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
