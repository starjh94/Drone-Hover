import Servo
import time
import degree
from threading import Thread

global print_check 

print_check = True
a = Servo.servo() 
b = degree.acc()

class startServo(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        time.sleep(5)
        print_check = False
        
        while(True):
            pitch_v = b.pitch()
            print pitch_v
            a.servo_2(1.22)
            a.servo_1(1.0)
            
class printAngle(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        while(print_check):
            print "Angle(before start) : ", b.pitch()
    


thread1 = startServo()
thread2 = printAngle()

thread1.start()
thread2.start()
