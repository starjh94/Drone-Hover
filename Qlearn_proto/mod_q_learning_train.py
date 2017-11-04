import subprocess
#subprocess.Popen(["python","degree_process.py"])

import Servo
import numpy as np
import degree_gyro_q_l
import threading
import time

import sysv_ipc
import tensorflow as tf
import random
import dqn
from collections import deque

## Initialize - drone
count = 1
init_pwm_1 = 1.22
init_pwm_2 = 1.12
l_plus_pwm = 0.37
r_plus_pwm = 0.42
start_time = 0

memory_degree = sysv_ipc.SharedMemory(600)
memory_ang_vel = sysv_ipc.SharedMemory(1024)
memory_acc_degree = sysv_ipc.SharedMemory(256)
memory_semaphore = sysv_ipc.Semaphore(128)

## Initialize - neural network
input_size = 2    # (Degree, Angular Velocity)
output_size = 3    # (Motor Up, Keep, Motor Down)

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
	return mainDQN.update(x_stack, y_stack)

def get_copy_var_ops(dest_scope_name="target", src_scope_name="main"):
	# Copy variables src_scope to dest_scope
	op_holder = []
	
	src_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=src_scope_name)
	dest_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=dest_scope_name)

	for src_var, dest_var in zip(src_vars, dest_vars):
        	op_holder.append(dest_var.assign(src_var.value()))
    
    	return op_holder


"""
def step_aciton(action, pwm, l_or_r):	

	
	if l_or_r == "left":
		motor_max = 1.32
		motor_min = 1.22
	elif l_or_r == "right":
		motor_max = 1.21
		motor_min = 1.1

	if action == 0:
		if pwm > motor_min:
			return pwm - 0.01, False
		else:
			return pwm, True
	elif action == 1:
		return pwm, False
	else:
		if pwm < motor_max: 
			return pwm + 0.01, False
		else:
			return pwm, True
"""

def step_action(action, pwm):
	if action == 0:
                return pwm - 0.001
        elif action == 1:
                return pwm
        else:
        	return pwm + 0.001


def reward_done_check(pre_degree, degree):
	if degree > -20 and degree < 20:
        	return +1, False
	
	else:
		if abs(degree - pre_degree) < 0.5:
			return 0, False

		else:
			if abs(degree) >= abs(pre_degree):
				print "degree finish"
				return -100, True
			else: 
				return 0, False
		"""
		if abs(degree) >= abs(pre_degree):
                	if abs(degree - pre_degree) < 0.5:
                        	return 0, False
                	else:
				print "degree finish"
                		return -100, True
		else:
			return 0, False
		"""
	"""
	if abs(degree) >= abs(pre_degree):
		if abs(degree - pre_degree) < 0.5:
			return +10, False
		print "degree finish"
		return -100, True
	else:
		if degree > -1 and degree < 1:
			return +100, False
		else:
			return 0, False

	"""
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

	max_episodes = 2000
	## store the previous observations in replay memory
	left_replay_buffer = deque()
	right_replay_buffer = deque()		

	que = []
	acc_que = []
	timecheck_list = []    	
	
	#pitch_aver = acc_gyro_pitch = gyro_pitch_degree = b.pitch()	
	pwm_1 = init_pwm_1
	pwm_2 = init_pwm_2 
	
	## matplotlib data initialization ##
	#np_ML_data = np.array([[0, acc_gyro_pitch, b.pitch(), gyro_pitch_degree, init_pwm_1, init_pwm_2]])	

	#every5sec()
	#every1sec()
	
	with tf.Session() as sess:
		left_mainDQN = dqn.DQN(sess, input_size, output_size, name="left_main")
		left_targetDQN = dqn.DQN(sess, input_size, output_size, name="left_target")
		right_mainDQN = dqn.DQN(sess, input_size, output_size, name="right_main")
                right_targetDQN = dqn.DQN(sess, input_size, output_size, name="right_target")
		tf.global_variables_initializer().run()
		
		## initial copy q_net -> target_net
		copy_left_ops = get_copy_var_ops(dest_scope_name="left_target", src_scope_name="left_main")
		copy_right_ops = get_copy_var_ops(dest_scope_name="right_target", src_scope_name="right_main")
		sess.run([copy_left_ops, copy_right_ops])
	
		#start_time = time.time() 
		#timecheck_list.append(start_time)
		for episode in range(max_episodes):
			print "new episodes initializaion"
			e = 1. / ((episode / 10) + 1) 
			done = False
			step_count = 0
			pwm_left = init_pwm_1
			pwm_right = init_pwm_2			
			
			"""
			degree = memory_degree.read()
			acc_gyro_pitch = float(degree.rstrip('\x00'))
			ang_vel = memory_ang_vel.read()	
			p_ang_vel = float(ang_vel.rstrip('\x00'))
			"""
			"""
			timecheck_list.append(time.time())
                	loop_time = timecheck_list[1] - timecheck_list[0]
			timecheck_list.pop(0)
			
			acc_pitch_degree = b.pitch()			
			
			gyro_pitch_degree, _ = b.gyro_pitch(loop_time, gyro_pitch_degree)
			get_gyro_degree, p_ang_vel = b.gyro_pitch(loop_time, acc_gyro_pitch)
                	acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))	
			"""
			"""	
			state = np.array([acc_gyro_pitch, p_ang_vel, pwm_left, pwm_right])
			"""
			#state = np.array([acc_gyro_pitch, p_ang_vel])
			print "\n\n"	
			while not done:
				memory_semaphore.acquire(10)
#				print "get the degree from the other process"
				degree = memory_degree.read()
#				print "complementary : %s : %s" %(repr(degree), degree)
                        	acc_gyro_pitch = float(degree.rstrip('\x00'))
#	                       	print "complementary success!"
				ang_vel = memory_ang_vel.read()
#				print "ang_vel : %s : %s" %(repr(ang_vel), ang_vel)
                        	p_ang_vel = float(ang_vel.rstrip('\x00'))
#				print "ang_vel success!"
				acc_degree = memory_acc_degree.read()
#				print "acc_degree : %s : %s" %(repr(acc_degree), acc_degree)
				acc_pitch = float(acc_degree.rstrip('\x00'))
#				print "acc_degree success!"
				memory_semaphore.release()
				state = np.array([acc_gyro_pitch, p_ang_vel])

				print "\t\t\t<state> degree: %s vs A:%s, \tangular velocity: %s" %(state[0], acc_pitch, state[1])
				if np.random.rand(1) < e:
					action_left = np.random.randint(3)
					action_right = np.random.randint(3)
				else:
					action_left = np.argmax(left_mainDQN.predict(state))
					action_right = np.argmax(right_mainDQN.predict(state))
				"""
				pwm_left, l_m_done = step_action(action_left, pwm_left, "left")	
				pwm_right, r_m_done = step_action(action_right, pwm_right, "right")
				"""
				pwm_left = step_action(action_left, pwm_left) 
                                pwm_right = step_action(action_right, pwm_right)
				
				print "\t\t\t\t\t<action-motor> left: %s, right: %s" % (pwm_left, pwm_right)
			
				a.servo_1(pwm_left)
				a.servo_2(pwm_right)						
			
				time.sleep(0.01)
				
				## Get new state and reward from environment
				"""
				degree = memory_degree.read()
                        	acc_gyro_pitch = float(degree.rstrip('\x00'))
                        	ang_vel = memory_ang_vel.read()
                        	p_ang_vel = float(ang_vel.rstrip('\x00'))
				acc_degree = memory_acc_degree.read()
                                acc_pitch = float(acc_degree.rstrip('\x00'))
				"""
				memory_semaphore.acquire(10)
#				print "get the degree from the other process"
                                degree = memory_degree.read()
#                               print "complementary : %s : %s" %(repr(degree), degree)
                                acc_gyro_pitch = float(degree.rstrip('\x00'))
#                               print "complementary success!"
  	                        ang_vel = memory_ang_vel.read()
#				print "ang_vel : %s : %s" %(repr(ang_vel), ang_vel)
                                p_ang_vel = float(ang_vel.rstrip('\x00'))
#                               print "ang_vel success!"
                                acc_degree = memory_acc_degree.read()
#                               print "acc_degree : %s : %s" %(repr(acc_degree), acc_degree)
                                acc_pitch = float(acc_degree.rstrip('\x00'))
#                               print "acc_degree success!"
				memory_semaphore.release()
				"""
				timecheck_list.append(time.time())
                        	loop_time = timecheck_list[1] - timecheck_list[0]
				timecheck_list.pop(0)

                        	acc_pitch_degree = b.pitch()

                        	gyro_pitch_degree, _ = b.gyro_pitch(loop_time, gyro_pitch_degree)
                        	get_gyro_degree, p_ang_vel = b.gyro_pitch(loop_time, acc_gyro_pitch)
                        	acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))				
				"""
				next_state = np.array([acc_gyro_pitch, p_ang_vel])				
				
				"""
				next_state = np.array([acc_gyro_pitch, p_ang_vel, pwm_left, pwm_right])
				"""
				reward, done = reward_done_check(state[0], next_state[0])		
			
		
				## Save the experience to our buffer
				left_replay_buffer.append((state, action_left, reward, next_state, done))
				right_replay_buffer.append((state, action_right, reward, next_state, done))
				if len(left_replay_buffer) > REPLAY_MEMORY:
					left_replay_buffer.popleft()
				
				if len(right_replay_buffer) > REPLAY_MEMORY:
                                        right_replay_buffer.popleft()
					
				if done: 
                                    	
					"""
					if step_count < 10:
						print "\t\t\t<warm-up>"
						done = False
						pass
					"""	
				    	
                               		print "\t\t\t<finish state> degree: %s vs A: %s, \tangular velocity: %s" %(next_state[0], acc_pitch,next_state[1])
					time.sleep(3)
					
					"""	
					degree = memory_degree.read()
                        		acc_gyro_pitch = float(degree.rstrip('\x00'))
                       			ang_vel = memory_ang_vel.read()
                       			p_ang_vel = float(ang_vel.rstrip('\x00'))
					"""
					"""	
					timecheck_list.append(time.time())
                               		loop_time = timecheck_list[1] - timecheck_list[0]
                               		timecheck_list.pop(0)

                           	  	acc_pitch_degree = b.pitch()

                                	gyro_pitch_degree, _ = b.gyro_pitch(loop_time, gyro_pitch_degree)
                                	get_gyro_degree, p_ang_vel = b.gyro_pitch(loop_time, acc_gyro_pitch)
                                	acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))
					"""
					#next_state = np.array([acc_gyro_pitch, p_ang_vel])
				
				#state = next_state
				step_count += 1
				if step_count > 10000:
					break
			
			print "Episode: {}  steps: {}".format(episode, step_count)	
			if step_count > 10000:
				pass
	
			if len(left_replay_buffer) > 10 and episode % 10 == 1: # train every 10 episode
				# Get a random batch of experiences.
				for _ in range(50):
					left_minibatch = random.sample(left_replay_buffer, 10)
					right_minibatch = random.sample(right_replay_buffer, 10)
					
					left_loss, _ = replay_train(left_mainDQN, left_targetDQN, left_minibatch)
					right_loss, _ = replay_train(right_mainDQN, right_targetDQN, right_minibatch)
					
				print "Left Loss: %s, Right Loss: %s" % (left_loss, right_loss)

				# copy q_net -> target_net
				sess.run([copy_left_ops, copy_right_ops])
	

if __name__ == '__main__':
    	try :
		main()
	except :
		print("finish")
		
		#np.save('M_L_Data', np_ML_data)
		#print "time: %s, number of numpy data: %s" % (time.time() - start_time, len(np_ML_data))
