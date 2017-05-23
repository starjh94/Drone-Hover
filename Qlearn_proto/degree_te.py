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
	t = acc.imu.read_gyro() 
	acc_v = math.atan2(m9a[0], m9a[2]) * 180 / math.pi
        t1 =m9g[0] * 180/math.pi
	print "kkk=",t1
	t1 = t1 * 0.98 + acc_v * 0.02
	print "Aaaa",t1
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
