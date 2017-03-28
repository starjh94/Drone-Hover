import sys
import time

import navio.pwm
import navio.util

#navio.util.check_apm()

PWM_OUTPUT_1 = 1
PWM_OUTPUT_2 = 2

SERVO_MIN = 1.3#ms
SERVO_MAX = 1 #ms
SERVO_MIN2 = 1.3#ms
SERVO_MAX2 = 1#ms
with navio.pwm.PWM(PWM_OUTPUT_1) as pwm_1, navio.pwm.PWM(PWM_OUTPUT_2) as pwm_2:

    pwm_1.set_period(50)
    pwm_2.set_period(50)

    while (True):
        pwm_1.set_duty_cycle(SERVO_MIN)
        pwm_2.set_duty_cycle(SERVO_MIN2)
        time.sleep(0.1)
       # pwm_1.set_duty_cycle(SERVO_MAX)
        #pwm_2.set_duty_cycle(SERVO_MAX)
       # time.sleep(0.1)
