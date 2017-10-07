import threading
import degree_gyro_q_l
import numpy as np
import time
acc1 = 0.0
acc2 = 0.0
class Degree(threading.Thread):

        def run(self):
		global acc1
   		global acc2
		b = degree_gyro_q_l.acc()
   		count = 0             
                timecheck_list = []
                acc_gyro_pitch = gyro_pitch_degree = b.pitch()
                
                start_time = time.time()
                timecheck_list.append(start_time)
                while(True):
                        #print "!!threadlock acquire"
			acc_pitch_degree = b.pitch()
                        
                        timecheck_list.append(time.time())
                        loop_time = timecheck_list[1] - timecheck_list[0]
                        timecheck_list.pop(0)
                        
                        acc1 = gyro_pitch_degree, _ = b.gyro_pitch(loop_time, gyro_pitch_degree)
                        get_gyro_degree, p_ang_vel = b.gyro_pitch(loop_time, acc_gyro_pitch)
			end = time.time()
			#acc1 = np.sign(get_gyro_degree) * ((0.97 * get_gyro_degree) + (0.03 * acc_pitch_degree))
			#print start_time - end, ; print np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))

def main() : 
	lock = threading.Lock()
        degree = Degree()
        global acc1
	degree.daemon = True
        degree.start()
        while(True):
		#lock.acquire()
		#print "lock acquire!!"
		#acc_gyro_pitch, p_ang_vel= degree.getDegree()
                #lock.release()
		#print "lock release!!"
		#print "Degree: %s, Ang_Vel: %s" % (acc_gyro_pitch, p_ang_vel)
		print acc1
		count = 0
if __name__ == '__main__':
	main()
		
