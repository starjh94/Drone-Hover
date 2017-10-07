import threading
import de_test2
import time

class Degree(threading.Thread):
        def __init__(self):
                super(Degree, self).__init__()
                self.acc_gyro_pitch = 0
                self.p_ang_vel = 0
		self.threadlock = threading.Lock()              

        def run(self):
                b = de_test2.acc()                
                timecheck_list = []
                m9a = b.pitch()
                start_time = time.time()
                timecheck_list.append(start_time)
		while(True):
			m9a = b.pitch()
			print m9a
                """
		while(True):
			self.threadlock.acquire()
                        #print "!!threadlock acquire"
			acc_pitch_degree = b.pitch()
                        
                        timecheck_list.append(time.time())
                        loop_time = timecheck_list[1] - timecheck_list[0]
                        timecheck_list.pop(0)
                        
                        gyro_pitch_degree, _ = b.gyro_pitch(loop_time, gyro_pitch_degree)
                        get_gyro_degree, p_ang_vel = b.gyro_pitch(loop_time, acc_gyro_pitch)
                        acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))
			self.acc_gyro_pitch = acc_gyro_pitch
			self.p_ang_vel = p_ang_vel
			self.threadlock.release()
                        
			#print "!!threadlock release"
			#print "----------====----------"
			#print "Degree: %s, Ang_Vel: %s" % (self.acc_gyro_pitch, self.p_ang_vel)        
        		"""
	def getDegree(self):
		return self.acc_gyro_pitch, self.p_ang_vel

def main() : 
	lock = threading.Lock()
        degree = Degree()
        
	degree.daemon = True
        degree.start()
        while(True):
		#lock.acquire()
		#print "lock acquire!!"
		#acc_gyro_pitch, p_ang_vel= degree.getDegree()
                #lock.release()
		#print "lock release!!"
		#print "Degree: %s, Ang_Vel: %s" % (acc_gyro_pitch, p_ang_vel)
		count = 0
if __name__ == '__main__':
	main()
		
