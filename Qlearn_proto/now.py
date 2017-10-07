import threading
import de_test2
import time
acc1 = 0.0
m9a = []
acc2 = 0.0
class Degree(threading.Thread):
	def __init__(self):
		self.abc =0.0
        def run(self):
		
		b = de_test.acc()
                start_time = time.time()
                timecheck_list.append(start_time)
                while(True):
			m9a, m9g, m9m = b.pitch()
			self.abc = m9a[0]
def main() : 
	lock = threading.Lock()
        degree = Degree()
        global m9a
	degree.daemon = True
        degree.start()
        while(True):
		#lock.dacquire()
		#print "lock acquire!!"
		#acc_gyro_pitch, p_ang_vel= degree.getDegree()
                #lock.release()
		#print "lock release!!"
		#print "Degree: %s, Ang_Vel: %s" % (acc_gyro_pitch, p_ang_vel)
		count = 0
if __name__ == '__main__':
	main()
		
