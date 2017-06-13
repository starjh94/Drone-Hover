import spidev
import time
import argparse
import sys
import mpu9250_gyro_test
import navio.util
import math
import tt3
a = tt3.comp_filt()
navio.util.check_apm()

imu = mpu9250_gyro_test.MPU9250()
imu.initialize()
count = 0

while(True):
	m9a, m9g, m9m = imu.getMotion9()
	a.attitude2(m9a[0],m9a[1],m9a[2],m9g[0],m9g[1],m9g[2])
