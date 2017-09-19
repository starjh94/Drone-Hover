import Servo
import numpy as np
import degree_gyro
import threading
import time

import tensorflow as tf
import random
import dqn
from collections import deque

## Initialize - drone
count = 1
init_pwm_1 = 1.22
init_pwm_2 = 1.1
l_plus_pwm = 0.37
r_plus_pwm = 0.42
start_time = 0

## Initialize - neural network
input_size = 2    # (Degree, Angular Velocity)
output_size = 3    # (Motor Up, Keep, Motor Down)

dis = 0.9
REPLAY_MEMORY = 50000

## Initialize - save data
np_ML_data = np.array([[0, 0, 0, 0, 0, 0]])
#f = open("data.txt", 'w')
"""
np_gyro_degree = np.array([[0, 0]])
np_acc_degree = np.array([[0, 0]])
np_acc_gyro = np.array([[0, 0]])

np_left_motor = np.array([[0, 0]])
np_right_motor = np.array([[0, 0]])
"""

def replay_tarin(mainDQN, targetDQN, train_batch):
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

## Using threading Timer
def every5sec() :
    	b = degree_gyro.acc()
    
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
    	b = degree_gyro.acc()
	global count
	global init_pwm_1
	global init_pwm_2
        global np_gyro_degree
        global np_acc_degree
        global np_acc_gyro
        global np_left_motor
        global np_right_motor    	
	global np_ML_data
	global start_time
    	
	max_episodes = 2000
	## store the previous observations in replay memory
	replay_buffer = deque()

	que = []
	acc_que = []
	timecheck_list = []    	
	
	pitch_aver = acc_gyro_pitch = gyro_pitch_degree = b.pitch()	
	pwm_1 = init_pwm_1
	pwm_2 = init_pwm_2 
	
	## matplotlib data initialization ##
	np_ML_data = np.array([[0, acc_gyro_pitch, b.pitch(), gyro_pitch_degree, init_pwm_1, init_pwm_2]])	

	#every5sec()
	every1sec()
	
	with tf.Session() as sess:
		mainDQN = dqn.DQN(sess, input_size, output_size, name="main")
		targetDQN = dqn.DQN(sess, input_size, output_size, name="target")
		tf.global_variables_initializer().run()

		## initial copy q_net -> target_net
		copy_ops = get_copy_var_ops(dest_scope_name="target", src_scope_name="main")
		sess.run(copy_cps)

		
		start_time = time.time() 
		timecheck_list.append(start_time)
		for episode in range(max_episodes):
			e = 1. / ((episode / 10) + 1) 
			done = False
			step_count = 0
			
			timecheck_list.append(time.time())
                	timecheck_list.pop(0)
			
			acc_pitch_degree = b.pitch()

                	gyro_pitch_degree = b.gyro_pitch(loop_time, gyro_pitch_degree)
                	get_gyro_degree = b.gyro_pitch(loop_time, acc_gyro_pitch)
                	acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree)))	
				
			state = 

			while not done:
				if np.random.rand(1) < e:
					pwm_1 = "-------------------------------------------------------"
					pwm_2 = "-------------------------------------------------------"
				else:
					pwm_1 = np.argmax(mainDQN.predict(state))
					pwm_2 = np.argmax(mainDQN.predict(state))
			
				## Get new state and reward from environment
				next_state, reward, done, _ = "-------------------------------------------------------"
				
				if done: # Penalty
					reward = -100
				else:
					if state[0] > -1 and state[0] < 1:
						reward = +10
				
					## Save the experience to our buffer
					replay_buffer.append((state, action, reward, next_state, done))
					if len(replay_buffer) > REPLAY_MEMORY:
					replay_buffer.popleft()

				state = next_state
				step_count += 1
				if step_count > 10000:
					break
		
			print "Episode: {}  steps: {}".format(episode, step_count)	
			if step_count > 10000:
				pass
	
			if episode % 10 == 1: # train every 10 episode
				# Get a random batch of experiences.
				for _ in range(50):
					minibatch = random.sample(replay_buffer, 10)
					loss, _ = replay_train(mainDQN, targetDQN, minibatch)
				
				print("Loss: ", loss)
				# copy q_net -> target_net
				sess.run(copy_ops)



    	while(True):
	
		timecheck_list.append(time.time())
		timecheck_list.pop(0)
					
		acc_pitch_degree = b.pitch()
		
		gyro_pitch_degree = b.gyro_pitch(loop_time, gyro_pitch_degree)
		get_gyro_degree = b.gyro_pitch(loop_time, acc_gyro_pitch)
                acc_gyro_pitch = np.sign(get_gyro_degree) * ((0.97 * abs(get_gyro_degree)) + (0.03 * abs(acc_pitch_degree))) 
		
		time_count = time.time()
		
		## for matplotlib ##
                data_time = time.time() - start_time
		np_ML_data = np.append(np_ML_data, [[data_time, acc_gyro_pitch, acc_pitch_degree, gyro_pitch_degree, pwm_1, pwm_2]], axis=0)

		
		count += 1
		time.sleep(0.01)

if __name__ == '__main__':
    	try :
		main()
	except :
		print("finish")
		
		np.save('M_L_Data', np_ML_data)
		print "time: %s, number of numpy data: %s" % (time.time() - start_time, len(np_ML_data))
