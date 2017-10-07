import threading
import degree_gyro_q_l
import numpy as np
import time

"""
class Degree(threading.Thread):
        def __init__(self):
                super(Degree, self).__init__()
		self.acc_gyro_pitch = 0
                self.p_ang_vel = 0              

        def run(self):
                b = degree_gyro_q_l.acc()
                
                timecheck_list = []
                self.acc_gyro_pitch = gyro_pitch_degree = b.pitch()
                
                start_time = time.time()
                timecheck_list.append(start_time)
                while(True):
                        acc_pitch_degree = b.pitch()
                        
                        timecheck_list.append(time.time())
                        loop_time = timecheck_list[1] - timecheck_list[0]
                        timecheck_list.pop(0)
                        
                        gyro_pitch_degree, _ = b.gyro_pitch(loop_time, gyro_pitch_degree)
                        get_gyro_degree, self.p_ang_vel = b.gyro_pitch(loop_time, self.acc_gyro_pitch)
                        self.acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))
			
			#print "Degree: %s, Ang_Vel: %s" % (self.acc_gyro_pitch, self.p_ang_vel)        
        def getDegree(self):
                return self.acc_gyro_pitch, self.p_ang_vel
"""


"""
acc_gyro_pitch = 0
p_ang_vel = 0

class Degree(threading.Thread):
        def run(self):
        	global acc_gyro_pitch
		global p_ang_vel        	
	
		b = degree_gyro_q_l.acc()
                
                timecheck_list = []
                acc_gyro_pitch = gyro_pitch_degree = b.pitch()
                
                start_time = time.time()
                timecheck_list.append(start_time)
                while(True):
                        acc_pitch_degree = b.pitch()
                        
                        timecheck_list.append(time.time())
                        loop_time = timecheck_list[1] - timecheck_list[0]
                        timecheck_list.pop(0)
                        
                        gyro_pitch_degree, _ = b.gyro_pitch(loop_time, gyro_pitch_degree)
                        get_gyro_degree, p_ang_vel = b.gyro_pitch(loop_time, acc_gyro_pitch)
                        acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))
                        
                        #print "Degree: %s, Ang_Vel: %s" % (self.acc_gyro_pitch, self.p_ang_vel)    
def main() :
	global acc_gyro_pitch
	global p_ang_vel

	degree = Degree()
	
	degree.daemon = True
	degree.start()
	while(True):	
		print "Degree: %s, Ang_Vel: %s" % (acc_gyro_pitch, p_ang_vel)
"""
class Degree(threading.Thread):
        def __init__(self):
                super(Degree, self).__init__()
                self.acc_gyro_pitch = 0
                self.p_ang_vel = 0
		self.threadlock = threading.Lock()              

        def run(self):
                b = degree_gyro_q_l.acc()
                
                timecheck_list = []
                acc_gyro_pitch = gyro_pitch_degree = b.pitch()
                
                start_time = time.time()
                timecheck_list.append(start_time)
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
        def getDegree(self):
		return self.acc_gyro_pitch, self.p_ang_vel

def main() : 
	lock = threading.Lock()
        degree = Degree()
        count = 0
	degree.daemon = True
        degree.start()
	star_time = time.time()
        while(True):
		#lock.acquire()
		#print "lock acquire!!"
		acc_gyro_pitch, p_ang_vel= degree.getDegree()
                #lock.release()
		#print "lock release!!"
		end_time = time.time()
		print count ,;print star_time - end_time ,;print "Degree: %s, Ang_Vel: %s" % (acc_gyro_pitch, p_ang_vel)
		count = count +1
if __name__ == '__main__':
	main()
		
