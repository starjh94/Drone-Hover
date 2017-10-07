import threading
import de_test
import time

class Degree:
        def __init__(self):
                self.acc_gyro_pitch = 0
                self.p_ang_vel = 0
		self.threadlock = threading.Lock()              
		self.pitch1=0.0
        def run(self):
                b = de_test.acc()
		b.pitch()
        	self.pitch1 = b.re_gyro()
		print self.pitch1
	def getDegree(self):
		return self.pitch1

def main() : 
	#lock = threading.Lock()
        #degree = Degree()
        
	#degree.daemon = True
        #degree.start()
	a = Degree()       
	while(True):
		a.run()
		#print "lock acquire!!"
		#print "lock release!!"
		#print "Degree: %s, Ang_Vel: " % (acc123)
		
if __name__ == '__main__':
	main()
