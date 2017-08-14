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

    	navio.util.check_apm()
    	imu = mpu9250_gyro_test.MPU9250()
	#imu = navio.mpu9250.MPU9250()
	imu.initialize()
	previous_pitch = 0
	count = 0
	timecheck_list = []
    	def pitch(self):

        	m9a, m9g, m9m = acc.imu.getMotion9()
		"""
		if (m9a[2] == 0):
			if (m9a[0] > 0):
				pitch_v = -90
			elif (m9a[0] < 0):
				pitch_v = +90
			else:
				pitch_v = 0
		else:
			pitch_v = math.atan(m9a[0]/m9a[2]) * 180 / math.pi
			
			if (m9a[0] > 0):
				pitch_v = -abs(pitch_v)
			else:
				pitch_v = abs(pitch_v)		
		"""
		pitch_v = -math.atan2(m9a[0], m9a[2]) * 180 / math.pi
		#sqrt_v = math.sqrt( pow(m9a[0],2) + pow(m9a[2],2))
		#pitch_v = math.atan2(m9a[2],sqrt_v) * 180 / math.pi
		#pitch_v = (pitch_v + 360) % 360
		
		#print "\n%s, %s => %s\n" % (m9a[0], m9a[2], pitch_v)		
		return pitch_v
        


	def pitchMore(self):

                m9a, m9g, m9m = acc.imu.getMotion9()
		pitch_v = -math.atan2(m9a[0], m9a[2]) * 180 / math.pi
                #sqrt_v = math.sqrt( pow(m9a[0],2) + pow(m9a[2],2))
                #pitch_v = math.atan2(m9a[2],sqrt_v) * 180 / math.pi
                #pitch_v = (pitch_v + 360) % 360
                #print "\n%s, %s => %s\n" % (m9a[0], m9a[2], pitch_v)           
                return m9a[0], m9a[2], pitch_v
	
	def pitch_3axis(self):

                m9a, m9g, m9m = acc.imu.getMotion9()
                #pitch_v = -math.atan2(m9a[0], m9a[2]) * 180 / math.pi
                sqrt_v = math.sqrt(pow(m9a[1],2) + pow(m9a[2],2))
		pitch_v = -math.atan2(m9a[0], sqrt_v) * 180 / math.pi
                #pitch_v = math.atan2(m9a[2],sqrt_v) * 180 / math.pi
                #pitch_v = (pitch_v + 360) % 360
                #print "\n%s, %s => %s\n" % (m9a[0], m9a[2], pitch_v)           
                return m9a[0]/sqrt_v, pitch_v

	"""
	def new_gyro_pitch(self, loop_time,previous_pitch):
        #       b = tt3.comp_filt()
                m9a, m9g, m9m = acc.imu.getMotion9()
                mm = acc.imu.read_gyro()
		#pitch_gyro = previous_pitch + (180 / math.pi) * m9g[1] * loop_time
                test_pitch = m9g[1] * loop_time
		pitch_gyro = previous_pitch + test_pitch
		#pitch_gyro = previous_pitch + m9g[1] * loop_time
                print test_pitch 
		#print "m9g[1] : %s, loop_time : %s, old : %s, new : %s" % (m9g[1], loop_time, previous_pitch, pitch_gyro)
                #pitch_gyro = m9g[a1]
        #       b.attitude2(m9a[0],m9a[1],m9a[2],m9g[0],m9g[1],m9g[2])
                return pitch_gyro
	"""

	def gyro_pitch(self, loop_time, previous_pitch):
				
		
		m9a, m9g, m9m = acc.imu.getMotion9()
		#pitch_gyro = previous_pitch + (180 / math.pi) * m9g[1] * loop_time
		pitch_gyro = previous_pitch + m9g[1] * loop_time
		#print "m9g[1] : %s, loop_time : %s, old : %s, new : %s" % (m9g[1], loop_time, previous_pitch, pitch_gyro)
		
		## <boundary value change> Degree -180 ~ +180 		
		if (pitch_gyro > -180 and pitch_gyro < 180):
			pass
		elif (pitch_gyro <= -180):
			pitch_gyro = 360 + pitch_gyro	## x = 180 - ( abs(x) - 180 )	 	
		else: 	## (pitch_gyro >= 180)
			pitch_gyro = -360 + pitch_gyro 
		"""
		## <boundary value change> Degree 0 ~ 360
		if (pitch_gyro > 0 and pitch_gyro < 360):
			pass
		elif (pitch_gyro >= 360):	## Over Boundary : Clockwise Rotation
			pitch_gyro = -360 + pitch_gyro
		else:	## Over Boundary : Counterclockwise Rotation, (pitch_gyro <= 0)
			pitch_gyro = 360 + pitch_gyro		 		
		"""

		return pitch_gyro

	def gyro_pitchMore(self, loop_time, previous_pitch):


                m9a, m9g, m9m = acc.imu.getMotion9()
                #pitch_gyro = previous_pitch + (180 / math.pi) * m9g[1] * loop_time
                dt = m9g[1] * loop_time
		pitch_gyro = previous_pitch + dt
                #print "m9g[1] : %s, loop_time : %s, old : %s, new : %s" % (m9g[1], loop_time, previous_pitch, pitch_gyro)

                ## <boundary value change> Degree -180 ~ +180           
                if (pitch_gyro > -180 and pitch_gyro < 180):
                        pass
                elif (pitch_gyro <= -180):
                        pitch_gyro = 360 + pitch_gyro   ## x = 180 - ( abs(x) - 180 )           
                else:   ## (pitch_gyro >= 180)
                        pitch_gyro = -360 + pitch_gyro
                """
                ## <boundary value change> Degree 0 ~ 360
                if (pitch_gyro > 0 and pitch_gyro < 360):
                        pass
                elif (pitch_gyro >= 360):       ## Over Boundary : Clockwise Rotation
                        pitch_gyro = -360 + pitch_gyro
                else:   ## Over Boundary : Counterclockwise Rotation, (pitch_gyro <= 0)
                        pitch_gyro = 360 + pitch_gyro                           
                """

                return dt, pitch_gyro

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
