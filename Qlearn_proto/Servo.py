import sys
import time

import navio.pwm
import navio.util

#navio.util.check_apm()
class servo:
    PWM_OUTPUT_1 = 1
    PWM_OUTPUT_2 = 2

    SERVO_MIN = 1#ms
    SERVO_MAX = 1 #ms
    SERVO_MIN2 = 1#ms
    SERVO_MAX2 = 1#ms
  
    def servo_1(self,pwm_v):
	with navio.pwm.PWM(1) as pwm_1:
		pwm_1.set_period(50)
		pwm_1.set_duty_cycle(pwm_v)
    def servo_2(self):
        with navio.pwm.PWM(2) as pwm_2:
                pwm_2.set_period(50)
                pwm_2.set_duty_cycle(pwm_v)
