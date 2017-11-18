import os
import sys
import glob

model_load = False

## Restore Model
if len(sys.argv) == 2 :

        #if os.path.exists("./TF_Data/"+sys.argv[1]) is False :
	if len(glob.glob("./TF_Data/"+sys.argv[1]+".*")) == 0:       
		print "'%s' is Not exist file\n" %(sys.argv[1])
                print "usage: sudo python *.py *.ckpt"
		exit()
	elif sys.argv[1][-5:] != ".ckpt":
                print "\nPlease write correctly!"
		print "usage: sudo python *.py *.ckpt"
        	exit()
	else:
		
                print "'%s' model will be restored!\n" %(sys.argv[1])
		model_load = True

## Enter Model name		
while True:
        learning_model_name= raw_input("Model name for save(<ex> *.ckpt) : ")

        if learning_model_name[-5:] != ".ckpt":
                print "\nPlease write correctly!"
        #elif os.path.exists("./TF_Data/"+learning_model_name) is True:
	elif len(glob.glob("./TF_Data/"+learning_model_name+".*")) > 0:

                while True:
                        same_name_answer = raw_input("\nThe file name already exists.\nDo you want to overwrite?(Y / N): ")

                        if same_name_answer.upper() == "Y":
                                print "\nIt will be overwrited as '%s'" % (learning_model_name)
                                break
                        elif same_name_answer.upper() == "N":
                                print "\nEnter the model name again"
                                break
                        else:
                                print "\nPleas write correctly!"

                if same_name_answer.upper() == "Y":
                        break
        else:
                print "\nIt will be saved as '%s'" % (learning_model_name)
                break

import subprocess
subprocess.Popen(["python","degree_process.py"])

import Servo
import numpy as np
import degree_gyro_q_l
import threading
import time

import copy
import sysv_ipc
import tensorflow as tf
import random
import REINFORCE

import matplotlib.pyplot
import pylab
import pdb
## Initialize - drone
count = 1
init_pwm_1 = 1.25
init_pwm_2 = 1.15
l_plus_pwm = 0.37
r_plus_pwm = 0.42


start_time = 0

done_episode = False

memory_degree = sysv_ipc.SharedMemory(600)
memory_ang_vel = sysv_ipc.SharedMemory(1024)
memory_acc_degree = sysv_ipc.SharedMemory(256)
memory_semaphore = sysv_ipc.Semaphore(128)

## Initialize - neural network
input_size = 2    # (Degree, Angular Velocity)
output_size = 9    # { (Motor Up, Keep, Motor Down) * (Motor Up, Keep, Motor Down) }

## for pylab
np_PG_data = np.array([[0, 0, 0]])

def step_action(action, pwm_left, pwm_right, var=0.0005):
	if action == 0:
                return pwm_left - var, pwm_right - var
        elif action == 1:
                return pwm_left - var, pwm_right
        elif action == 2: 
        	return pwm_left - var, pwm_right + var
	elif action == 3:
		return pwm_left, pwm_right - var
	elif action == 4:
		return pwm_left, pwm_right
	elif action == 5:
		return pwm_left, pwm_right + var
	elif action == 6:
		return pwm_left + var, pwm_right - var
	elif action == 7:
		return pwm_left + var, pwm_right
	else:
		return pwm_left + var, pwm_right + var

def safe_pwm(pwm_left, pwm_right):
	pwm_l = pwm_left
	pwm_r = pwm_right	

	if(pwm_left < 1.22):
		pwm_l = 1.22
	elif(pwm_left > 1.62):
		pwm_l = 1.62
	
	if(pwm_right < 1.12):
		pwm_r = 1.12
	elif(pwm_right > 1.57):
		pwm_r = 1.57

	return pwm_l, pwm_r

def action_print(action):
        if action == 0:
        	return "(Down, Down)"
	elif action == 1:
        	return "(Down, ...)"
	elif action == 2:
        	return "(Down, Up)"
	elif action == 3:
        	return "(..., Down)"
	elif action == 4:
        	return "(..., ...)"
	elif action == 5:
        	return "(..., Up)"
	elif action == 6:
        	return "(Up, Down)"
	elif action == 7:
        	return "(Up, ...)"
	else:
		return "(Up, Up)"
"""
def reward_done_check(pre_degree, degree):
        ## motor PWM check 
        if (degree[2] < 1.22 or degree[2] > 1.57) or (degree[3] < 1.12 or degree[3] > 1.52):
                return -200, True

        if abs(int(degree[0])) > abs(int(pre_degree[0])):               # <absolute> Degree ( now > past ) 
        	if abs(degree[1]) < abs(pre_degree[1]):         # <absolute> Angular velocity ( now < past )
                        return 1/(abs(degree[0])+0.01), False
                else:                                           # <absolute>  Angular velocity ( now > past )
                        if np.sign(degree[1]) * np.sign(degree[0]) == -1:       # Sign of the current angle and Sign of the angular velocity are different
                                return 1/(abs(degree[0])+0.01), False
                        else:                                                   # Same sign
                                print "degree finish"
                                return 1/(abs(degree[0])+0.01), True
        else:                                                           # <absolute> Degree ( now < past )
                return 1/(abs(degree[0])+0.01), False
"""
"""
def reward_check(degree):
        
	if degree[0] > -10 and degree[0] <+10:
		if degree[1] > - 160 and degree[1] < +160:
			return +100
		
		elif degree[1] > -160 and degree[1] < +160:
			return +10 
		
		else:
			return -10
                
	elif degree[0] < -170 or degree[0] > +170:
		return -100 
        else:
                return  -0.1
"""

## main ##
def reward_check(degree):
       	if degree[0] < -150 or degree[0] > +150:
		return +1
	
	else:
		return -(180 - abs(degree[0])) / 180
	""" 
        if degree[0] < -170 or degree[0] > +170:
               	return +1000
                
        elif degree[0] > -10 and degree[0] < +10:
                return -100 

        else:
                return  -0.1
	"""
"""
def reward_check(degree):
        if degree[0] > -10 and degree[0] <+10:
                return +10
        else:
                return -abs(degree[0]) 
"""
"""
def reward_check(degree):
        if degree[0] > -10 and degree[0] <+10:
                return +100 
        elif degree[0] < -170 and degree[0] > +170:
                return -100 
        else:
                return -0.1 
"""
"""
def reward_check(pre_degree, degree):
	if degree[0] > -1 and degree[0] <1:
		return +1        

	if abs(int(degree[0])) > abs(int(pre_degree[0])):               # <absolute> Degree ( now > past ) 
                if abs(degree[1]) < abs(pre_degree[1]):         # <absolute> Angular velocity ( now < past )
                        return 0
                else:                                           # <absolute>  Angular velocity ( now > past )
                        if np.sign(degree[1]) * np.sign(degree[0]) == -1:       # Sign of the current angle and Sign of the angular velocity are different
                                return 0
                        else:                                                   # Same sign
                                print "degree finish"
                                return -1
        else:                                                           # <absolute> Degree ( now < past )
                return 0
"""

def done_timer():
	global done_episode
	done_episode = True

## Using threading Timer
def every5sec() :
    	b = degree_gyro_q_l.acc()
    
    	global init_pwm_1
    	init_pwm_1 += 0.01
    
    	#print "pwm_v1 = %s pwm_v2 = %s degree = %s \n" % (pwm_1, pwm_2, b.pitch())
    	print "\n\n\n\n\n\n\n\n\n---------------------motor up---------------------\n"
	threading.Timer(5, every5sec).start()

def every1sec() :
	global count
	global f
	
	#data = "%s sensor data / sec \n" % count
	#f.write(data)
	count = 1
	#print "\n\n\n\n\n\n\n\n\n!!!!!!!!!!!!!!!!!!!!! 1sec over !!!!!!!!!!!!!!!!!!!!!\n"

	threading.Timer(1, every1sec).start()

"""
def drone_play(mainDQN) :
        global init_pwm_1
        global init_pwm_2

        a = Servo.servo()
        pwm_left = init_pwm_1
        pwm_right = init_pwm_2

        while True:
                memory_semaphore.acquire(10)
                degree = memory_degree.read()
                acc_gyro_pitch = float(degree.rstrip('\x00'))
                ang_vel = memory_ang_vel.read()
                p_ang_vel = float(ang_vel.rstrip('\x00'))
                acc_degree = memory_acc_degree.read()
                acc_pitch = float(acc_degree.rstrip('\x00'))

                memory_semaphore.release()
                state = np.array([acc_gyro_pitch, p_ang_vel, pwm_left, pwm_right])

                print "\t\t\t<state> degree: %s, \tangular velocity: %s" %(state[0],  state[1])
                action = np.argmax(mainDQN.predict(state))

                pwm_left, pwm_right = step_action(action, pwm_left, pwm_right)

                print "\t\t\t\t\t\t\t\t\t\t<action-motor> left: %s, right: %s <= %s" % (pwm_left, pwm_right, action_print(action))

                a.servo_1(pwm_left)
                a.servo_2(pwm_right)

                time.sleep(0.01)
"""

def main():
	a = Servo.servo()
    	b = degree_gyro_q_l.acc()
	global count
	global init_pwm_1
	global init_pwm_2
	global start_time
	global memory_degree
	global memory_ang_vel    	
	global memory_acc_degree	
	global memory_semaphore	
	global sess	
	global model_load
	global done_episode
	global np_PG_data


	max_episodes = 2000
		
	pwm_1 = init_pwm_1
	pwm_2 = init_pwm_2

	
	#init = tf.global_variables_initializer()	
	sess = tf.Session()
	if True:
		#pdb.set_trace()
		agent = REINFORCE.REINFORCEAgnet(sess, input_size, output_size, name="main")
		if not model_load:
			tf.global_variables_initializer().run(session=sess)
		else:
			saver = tf.train.Saver()
			saver.restore(sess, "./TF_Data/"+sys.argv[1]) 	
			print "'%s' model is loaded" % (sys.argv[1])	

		for episode in range(max_episodes):

			print "new episodes initializaion"
			done = False
            		done_episode = False
			score = 0

			pwm_left = init_pwm_1
			pwm_right = init_pwm_2
			
			timer = threading.Timer(10, done_timer).start()
			print "\n\n"	
			while not done:				
				memory_semaphore.acquire(10)
				degree = memory_degree.read()
                        	acc_gyro_pitch = float(degree.rstrip('\x00'))
				ang_vel = memory_ang_vel.read()
                        	p_ang_vel = float(ang_vel.rstrip('\x00'))
				acc_degree = memory_acc_degree.read()
				acc_pitch = float(acc_degree.rstrip('\x00'))
				
				memory_semaphore.release()
				state = np.array([acc_gyro_pitch, p_ang_vel])
				
				print "\t\t\t<state> degree: %s, \tangular velocity: %s" %(state[0],  state[1])
				#state = np.reshape(state, [1, 4])

				action = agent.predict(state)
				
				pwm_left, pwm_right = step_action(action, pwm_left, pwm_right)
				pwm_left, pwm_right = safe_pwm(pwm_left, pwm_right)
				
				print "\t\t\t\t\t\t\t\t<action-motor> left: %s, right: %s <= %s" % (pwm_left, pwm_right, action_print(action))
				a.servo_1(pwm_left)
				a.servo_2(pwm_right)
				
				time.sleep(0.01)
				
				## Get new state and reward from environment
				memory_semaphore.acquire(10)
				degree = memory_degree.read()
                                
                                acc_gyro_pitch = float(degree.rstrip('\x00'))
  	                        ang_vel = memory_ang_vel.read()
                                p_ang_vel = float(ang_vel.rstrip('\x00'))
                                acc_degree = memory_acc_degree.read()
                                acc_pitch = float(acc_degree.rstrip('\x00'))
				
				memory_semaphore.release()
				next_state = np.array([acc_gyro_pitch, p_ang_vel])
				print "\t\t\t<next-state> degree: %s, \tangular velocity: %s" %(next_state[0], next_state[1])	
				reward = reward_check(next_state)
				#reward = reward_check(state, next_state)
				if done_episode == True:
					done = done_episode
				
				agent.append_sample(state, action, reward)
				score += reward
				state = copy.deepcopy(next_state)

				if done:
					loss = agent.update(keep_prob=0.7)
					if episode == 0:
						np_PG_data = np.array([[episode, loss, score]])
					else:	
	 					np_PG_data = np.append(np_PG_data, [[episode, loss, score]], axis=0)
                    			score = round(score, 2)
                    			print "episode: %s  loss: %s  score: %s" %(episode, loss ,score)
					time.sleep(3)
			
if __name__ == '__main__':
    	try :
		main()
	except :
		print("finish")
		
		# Save Graph
		np.save('./Learning_Data/PG_L_Data', np_PG_data)
		print "\n<Learning Image Data is saved>"		

		# Save model 
		saver = tf.train.Saver()
		save_path = saver.save(sess, "./TF_Data/"+learning_model_name)
		print "\n<Model is saved>"
		
				
