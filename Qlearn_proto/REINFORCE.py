import tensorflow as tf
import numpy as np

class REINFORCEAgnet:
	def __init__(self, session, input_size, output_size, name="main"):
		self.session = session
		self.state_size = input_size
		self.action_size = output_size
		
		self.discount_factor = 0.99
		self.keep_prob = tf.placeholder(tf.float32)
        	self.name = name
        	self._build_network()
        	self.states, self.actions, self.rewards = [], [], []
	
    	def leaky_relu(self, x, alpha):
                return tf.nn.relu(x) - alpha * tf.nn.relu(-x)
            
    	def _build_network(self, h_size=24, l_rate=1e-3):
		with tf.variable_scope(self.name):
            		self._X = tf.placeholder(tf.float32, [None, self.state_size], name="input_x")
			
			# First layer of weights
            		W1 = tf.get_variable("W1", shape=[self.state_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
			
           		layer1 = tf.nn.relu(tf.matmul(self._X, W1))
			layer1 = tf.nn.dropout(layer1, keep_prob= self.keep_prob) 
			
			# Second layer of weights
            		W2 = tf.get_variable("W2", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
            		
			layer2 = tf.nn.relu(tf.matmul(layer1, W2))
            		layer2 = tf.nn.dropout(layer2, keep_prob= self.keep_prob)
			
			# Third layer of weights
            		W3 = tf.get_variable("W3", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
           	 	
			layer3 = tf.nn.relu(tf.matmul(layer2, W3))
			layer3 = tf.nn.dropout(layer3, keep_prob= self.keep_prob)
			
			# Fourth layer of weights
            		W4 = tf.get_variable("W4", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
            
            		layer4 = tf.nn.relu(tf.matmul(layer3, W4))
			layer4 = tf.nn.dropout(layer4, keep_prob= self.keep_prob)
			
			# Fifth layer of weights
            		W5 = tf.get_variable("W5", shape=[h_size, self.action_size], initializer=tf.contrib.layers.xavier_initializer())
            		
			self._Pgradient = tf.nn.softmax(tf.matmul(layer4, W5))
        	
		self._action = tf.placeholder(tf.float32, shape=[None, self.action_size])
        	self._discounted_rewards = tf.placeholder(tf.float32, shape=[None,])
		
		self._action_prob = tf.reduce_sum(self._action * self._Pgradient, 1)
		self._cross_entropy = tf.log(self._action_prob) * self._discounted_rewards
		self._loss = -np.sum(self._cross_entropy)

        	self._train = tf.train.AdamOptimizer(learning_rate=l_rate).minimize(self._loss)

    	
	def predict(self, state):
		state = np.reshape(state, [1, self.state_size])
		print "111"
		policy = self.session.run(self._Pgradient, feed_dict={self._X: state})[0]
		print "222"
		return np.random.choice(self.action_size, 1, p=policy)[0]
    
    	def discount_rewards(self, rewards):
        	discounted_rewards = np.zeros_like(rewards)
        	running_add = 0
        	for t in reversed(range(0, len(rewards))):
            		running_add = running_add * self.discount_factor + rewards[t]
            		discounted_rewards[t] = running_add
        	return discounted_rewards
    
    	def append_sample(self, state, action, reward):
        	self.states.append(state[0])
        	self.rewards.append(reward)
        	act = np.zeros(self.action_size)
        	act[action] = 1
        	self.actions.append(act)
        
    	def update(self, keep_prob):
        	discounted_rewards = np.float32(self.discount_rewards(self.rewards))
        	discounted_rewards -= np.mean(discounted_rewards)
        	discounted_rewards /= np.std(discounted_rewards)
        
        	loss, _ = self.session.run([self._loss, self._train], feed_dict = {self._X: self.states, self._action: self.actions, self._discounted_rewards: discounted_rewards, self.keep_prob: keep_prob})
        	self.states, self.actions, self.rewards = [], [], []
        	return loss
