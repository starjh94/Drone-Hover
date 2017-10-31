import os
import sys
import glob

model_load = False
deque_load = False

## Restore Model
if len(sys.argv) == 2 :

        #if os.path.exists("./TF_Data/"+sys.argv[1]) is False :
	if len(glob.glob("./TF_Data/"+sys.argv[1]+".*")) == 0:       
		print "'%s' is Not exist file\n" %(sys.argv[1])
                print "usage: sudo python *.py *.ckpt"
		exit()
        else:
                print "'%s' model will be restored!\n" %(sys.argv[1])
		model_load = True

## Restore Model & Deque
elif len(sys.argv) == 3:
	
	if len(glob.glob("./TF_Data/"+sys.argv[1]+".*")) == 0:
                print "'%s' is Not exist file\n" %(sys.argv[1])
	else :
        	model_load = True
	
	if os.path.exists("./Deque_Data/"+sys.argv[2]) is False:
		print "'%s' is Not exist file\n" %(sys.argv[2]) 
	else:
		deque_load = True
	
	if not (model_load and deque_load):
                print "usage: sudo python *.py  *.ckpt  *.txt"
		exit()
	else:  
		print "'%s' model & '%s' deque will be restored!\n" %(sys.argv[1], sys.argv[2])


## Enter Model name		
while True:
        learning_model_name= raw_input("Model name for save(<ex> *.ckpt) : ")

        if learning_model_name[-5:] != ".ckpt":
                print "\nPlease write correctly!"
        elif os.path.exists("./TF_Data/"+learning_model_name) is True:

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

## Enter Deque name
while True:
        learning_deque_name= raw_input("Deque name for save(<ex> *.txt) : ")

        if learning_deque_name[-4:] != ".txt":
                print "\nPlease write correctly!"
        elif os.path.exists("./Deque_Data/"+learning_deque_name) is True:

                while True:
                        same_deq_name_answer = raw_input("\nThe file name already exists.\nDo you want to overwrite?(Y / N): ")

                        if same_deq_name_answer.upper() == "Y":
                                print "\nIt will be overwrited as '%s'" % (learning_deque_name)
                                break
                        elif same_deq_name_answer.upper() == "N":
                                print "\nEnter the deque name again"
                                break
                        else:
                                print "\nPleas write correctly!"

                if same_deq_name_answer.upper() == "Y":
                        break
        else:
                print "\nIt will be saved as '%s'" % (learning_deque_name)
                break



import subprocess
subprocess.Popen(["python","degree_process.py"])

import Servo
import numpy as np
import degree_gyro_q_l
import threading
import time

import sysv_ipc
import tensorflow as tf
import random
import dqn_test as dqn
from collections import deque
import pickle

## Initialize - drone
count = 1
init_pwm_1 = 1.25
init_pwm_2 = 1.15
l_plus_pwm = 0.37
r_plus_pwm = 0.42
start_time = 0

memory_degree = sysv_ipc.SharedMemory(600)
memory_ang_vel = sysv_ipc.SharedMemory(1024)
memory_acc_degree = sysv_ipc.SharedMemory(256)
memory_semaphore = sysv_ipc.Semaphore(128)

## Initialize - neural network
input_size = 4    # (Degree, Angular Velocity, PWM_Left, PWM_Right)
output_size = 9    # { (Motor Up, Keep, Motor Down) * (Motor Up, Keep, Motor Down) }

dis = 0.9
REPLAY_MEMORY = 50000

## Initialize - save data
np_ML_data = np.array([[0, 0, 0, 0, 0, 0]])

def replay_train(mainDQN, targetDQN, train_batch):
	x_stack = np.empty(0).reshape(0, input_size)
	y_stack = np.empty(0).reshape(0, output_size)

	# Get stored information from the buffer
	for state, action, reward, next_state, done in train_batch:
		Q = mainDQN.predict(state)

		# terminal?
		if done:
			Q[0, action] = reward
		else:
			Q[0, action] = reward + dis * np.max(targetDQN.predict(next_state))
		
		y_stack = np.vstack([y_stack, Q])
		x_stack = np.vstack([x_stack, state])
	
	# Train our network using target and predicted Q values on each episode
	return mainDQN.update(x_stack, y_stack, 0.7)

def get_copy_var_ops(dest_scope_name="target", src_scope_name="main"):
	# Copy variables src_scope to dest_scope
	op_holder = []
	
	src_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=src_scope_name)
	dest_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=dest_scope_name)

	for src_var, dest_var in zip(src_vars, dest_vars):
        	op_holder.append(dest_var.assign(src_var.value()))
    
    	return op_holder



def step_action(action, pwm_left, pwm_right, var=0.001):
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
        if degree[0] > -5 and degree[0] < 5:
                return +1, False

        else:
                if abs(degree[0] - pre_degree[0]) < 0.5:
                        return 0, False

                else:
                        if abs(degree[0]) >= abs(pre_degree[0]):
                                if abs(degree[1]) < abs(pre_degree[1]) :
                                        return 0, False
                                else:
                                        print "degree finish"
                                        return -100, True
                        else:
                                return 0, False
"""
"""
def reward_done_check(pre_degree, degree):
	if degree[0] > -5 and degree[0] < 5:
        	return -abs(degree[0]), False
	
	else:
		if abs(degree[0] - pre_degree[0]) < 0.5:
			return -abs(degree[0]), False

		else:
			if abs(degree[0]) >= abs(pre_degree[0]):
				if abs(degree[1]) < abs(pre_degree[1]) :
					return -abs(degree[0]), False
				else:
					if np.sign(degree[1]) * np.sign(degree[0]) == -1:
                                		print "!!"
                                		return -abs(degree[0]), False
					else:
						print "degree finish"
						return -abs(degree[0]), True
			else: 
				return -abs(degree[0]), False

"""
"""
def reward_done_check(pre_degree, degree):
        if degree[0] > -5 and degree[0] < 5:
                return -abs(degree[0]), False
        
        else:
              	if abs(degree[0]) >= abs(pre_degree[0]):
                	if abs(degree[1]) < abs(pre_degree[1]) :
                                return -abs(degree[0]), False
                        else:
                                print "degree finish"
                                return -abs(degree[0]), True
                else: 
                        return -abs(degree[0]), False
"""
"""
def reward_done_check(pre_degree, degree):
        if int(degree[0]) > -5 and int(degree[0]) < 5:
                return -abs(int(degree[0])), False
        
        else:
                if abs(int(degree[0])) > abs(int(pre_degree[0])):
                        if abs(degree[1]) < abs(pre_degree[1]) :
                                return -abs(int(degree[0])), False
                        else:
				if np.sign(degree[1]) * np.sign(degree[0]) == -1: 
                                	print "!!"
					return -abs(int(degree[0])), False
				else:
					print "degree finish"
                                	return -abs(int(degree[0])), True
                else: 
                        return -abs(int(degree[0])), False
"""
"""
def reward_done_check(pre_degree, degree):
	## motor PWM check 
	if (degree[2] < 1.22 or degree[2] > 1.57) or (degree[3] < 1.12 or degree[3] > 1.52):
		return -10000, True

	## Degree & Angular velocity check
	if abs(int(degree[0])) > abs(int(pre_degree[0])):
        	if abs(degree[1]) < abs(pre_degree[1]) :
                        return -abs(degree[0]), False
                else:	
                        if np.sign(degree[1]) * np.sign(degree[0]) == -1: 
                                return -abs(degree[0]), False
                        else:
                                print "degree finish"
                                return -abs(degree[0]), True
        else: 
                return -abs(degree[0]), False
"""
def reward_done_check(pre_degree, degree):
        ## motor PWM check 
        if (degree[2] < 1.22 or degree[2] > 1.57) or (degree[3] < 1.12 or degree[3] > 1.52):
                return -100, True

        ## Degree & Angular velocity check
	if degree[0] > -15 and degree[0] < 15:		# objective( 0 degree ) +,- 15 degree
                return +1, False
        
        else:
        	if abs(int(degree[0])) > abs(int(pre_degree[0])):		# <absolute> Degree ( now > past ) 
			if abs(degree[1]) < abs(pre_degree[1]):		# <absolute> Angular velocity ( now < past )
                        	return 0, False
                	else:						# <absolute>  Angular velocity ( now > past )
                        	if np.sign(degree[1]) * np.sign(degree[0]) == -1: 	# Sign of the current angle and Sign of the angular velocity are different
                                	return 0, False
                        	else:							# Same sign
                                	print "degree finish"
                                	return -100, True
        	else: 								# <absolute> Degree ( now < past )
                	return 0, False



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

def main() :
	a = Servo.servo()
    	b = degree_gyro_q_l.acc()
	global count
	global init_pwm_1
	global init_pwm_2
	global np_ML_data
	global start_time
	global memory_degree
	global memory_ang_vel    	
	global memory_acc_degree	
	global memory_semaphore	
	global sess	
	global model_load	
	global deque_load
	global replay_buffer	

	max_episodes = 2000
	## store the previous observations in replay memory
	if not deque_load:
		replay_buffer = deque()
	else:
		f = open("./Deque_Data/"+sys.argv[2], 'r')
		replay_buffer = pickle.load(f)
		f.close()
		print "'%s' deque is loaded" % (sys.argv[2])		

	que = []
	acc_que = []
	timecheck_list = []    	
	
	pwm_1 = init_pwm_1
	pwm_2 = init_pwm_2 
	
	## matplotlib data initialization ##
	#np_ML_data = np.array([[0, acc_gyro_pitch, b.pitch(), gyro_pitch_degree, init_pwm_1, init_pwm_2]])	
	

	init = tf.global_variables_initializer()	
	sess = tf.Session()
	
	if True:
	#with tf.Session() as sess:
		mainDQN = dqn.DQN(sess, input_size, output_size, name="main")
		targetDQN = dqn.DQN(sess, input_size, output_size, name="target")
		if not model_load:
			tf.global_variables_initializer().run(session=sess)
		else:
			saver = tf.train.Saver()
			saver.restore(sess, "./TF_Data/"+sys.argv[1]) 	
			print "'%s' model is loaded" % (sys.argv[1])			

		## initial copy q_net -> target_net
		copy_ops = get_copy_var_ops(dest_scope_name="target", src_scope_name="main")
		sess.run(copy_ops)

		for episode in range(max_episodes):
			print "new episodes initializaion"
			e = 1. / ((episode / 10) + 1) 
			done = False
			step_count = 0
			pwm_left = init_pwm_1
			pwm_right = init_pwm_2			
			
			#state = np.array([acc_gyro_pitch, p_ang_vel])
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
				state = np.array([acc_gyro_pitch, p_ang_vel, pwm_left, pwm_right])

				print "\t\t\t<state> degree: %s, \tangular velocity: %s" %(state[0],  state[1])
				if np.random.rand(1) < e:
					action = np.random.randint(9)
				else:
					action = np.argmax(mainDQN.predict(state))
				
				print "Q: %s" % (mainDQN.predict(state))	
				pwm_left, pwm_right = step_action(action, pwm_left, pwm_right) 
				
				print "\t\t\t\t\t\t\t\t\t\t<action-motor> left: %s, right: %s <= %s" % (pwm_left, pwm_right, action_print(action))
			
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
				
				next_state = np.array([acc_gyro_pitch, p_ang_vel, pwm_left, pwm_right])				
				
				reward, done = reward_done_check(state, next_state)		
			
		
				## Save the experience to our buffer
				replay_buffer.append((state, action, reward, next_state, done))
				if len(replay_buffer) > REPLAY_MEMORY:
					replay_buffer.popleft()
				
				if done: 
                                    	
					"""
					if step_count < 10:
						print "\t\t\t<warm-up>"
						done = False
						pass
					"""	
				    	
                               		print "\t\t\t<finish state> degree: %s, \tangular velocity: %s" %(next_state[0], next_state[1])
					time.sleep(3)
					
					#next_state = np.array([acc_gyro_pitch, p_ang_vel])
				
				#state = next_state
				step_count += 1
				if step_count > 10000:
					break
			
			print "Episode: {}  steps: {}".format(episode, step_count)	
			if step_count > 10000:
				pass
	
			if len(replay_buffer) > 100 and episode % 10 == 1: # train every 10 episode
				# Get a random batch of experiences.
				for _ in range(50):
					minibatch = random.sample(replay_buffer, 10)
					
					loss, _ = replay_train(mainDQN, targetDQN, minibatch)
					
				print "Loss: %s" % (loss)

				# copy q_net -> target_net
				sess.run(copy_ops)
	

if __name__ == '__main__':
    	try :
		main()
	except :
		print("finish")
		# Save model 
		saver = tf.train.Saver()
		save_path = saver.save(sess, "./TF_Data/"+learning_model_name)
		print "\n<Model is saved>"
				
		# Save deque
		f = open("./Deque_Data/"+learning_deque_name, 'w')
		pickle.dump(replay_buffer, f)
		f.close()			
		print "<Deque is saved>"		

		#np.save('M_L_Data', np_ML_data)
		#print "time: %s, number of numpy data: %s" % (time.time() - start_time, len(np_ML_data))
