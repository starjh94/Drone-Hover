import tensorflow as tf
import numpy as np

class DQN:
    
	def __init__(self, session, input_size, output_size, name="main"):
        	self.session = session
        	self.input_size = input_size
        	self.output_size = output_size
        	self.net_name = name
		self.keep_prob = tf.placeholder(tf.float32)  	
      
        	self._build_network()
	
	def leaky_relu(self, x, alpha):
		return tf.nn.relu(x) - tf.multiply(alpha, tf.nn.relu(-x))    	

	def huber_loss(self, labels, predictions, delta=1.0):
		residual = tf.abs(predictions - labels)
		condition = tf.less(residual, delta)
		small_res = 0.5 * tf.square(residual)
		large_res = delta * residual - 0.5 * tf.square(delta)
		return tf.where(condition, small_res, large_res)		

    	def _build_network(self, h_size=64, l_rate=1e-4):
    		with tf.variable_scope(self.net_name):
           		self._X = tf.placeholder(tf.float32, [None, self.input_size], name="input_x")
            
            		# First layer of weights
            		W1 = tf.get_variable("W1", shape=[self.input_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
		
	                #layer1 = tf.nn.relu(tf.matmul(self._X, W1))
            		layer1 = self.leaky_relu(tf.matmul(self._X, W1), 0.1)
			layer1 = tf.nn.dropout(layer1, keep_prob= self.keep_prob)
            
           		# Second layer of weights
            		W2 = tf.get_variable("W2", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
            		
			#layer2 = tf.nn.relu(tf.matmul(layer1, W2))
			layer2 = self.leaky_relu(tf.matmul(layer1, W2), 0.1)
			layer2 = tf.nn.dropout(layer2, keep_prob= self.keep_prob)			

			# Third layer of weights
            		W3 = tf.get_variable("W3", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
            
            		#layer3 = tf.nn.relu(tf.matmul(layer2, W3))
            		layer3 = self.leaky_relu(tf.matmul(layer2, W3), 0.1)
			layer3 = tf.nn.dropout(layer3, keep_prob= self.keep_prob)
            
            		# Fourth layer of weights
            		W4 = tf.get_variable("W4", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
            
            		#layer4 = tf.nn.relu(tf.matmul(layer3, W4))
            		layer4 = self.leaky_relu(tf.matmul(layer3, W4), 0.1)
			layer4 = tf.nn.dropout(layer4, keep_prob= self.keep_prob)

            		# Fifth layer of weights
            		W5 = tf.get_variable("W5", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())
            	
			#layer5 = tf.nn.relu(tf.matmul(layer4, W5))
			layer5 = self.leaky_relu(tf.matmul(layer4, W5), 0.1)
			layer5 = tf.nn.dropout(layer5, keep_prob= self.keep_prob)

			# Sixth layer of weights
			W6 = tf.get_variable("W6", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())

                        #layer6 = tf.nn.relu(tf.matmul(layer5, W6))
                        layer6 = self.leaky_relu(tf.matmul(layer5, W6), 0.1)
			layer6 = tf.nn.dropout(layer6, keep_prob= self.keep_prob)
			
			# Seventh layer of weights
 			W7 = tf.get_variable("W7", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())

                        #layer7 = tf.nn.relu(tf.matmul(layer6, W7))
                        layer7 = self.leaky_relu(tf.matmul(layer6, W7), 0.1)
			layer7 = tf.nn.dropout(layer7, keep_prob= self.keep_prob)
	
			# Eighth layer of weights
			W8 = tf.get_variable("W8", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())

                        #layer8 = tf.nn.relu(tf.matmul(layer7, W8))
                        layer8 = self.leaky_relu(tf.matmul(layer7, W8), 0.1)
			layer8 = tf.nn.dropout(layer8, keep_prob= self.keep_prob)

			# Nineth layer of weights
			W9 = tf.get_variable("W9", shape=[h_size, h_size], initializer=tf.contrib.layers.xavier_initializer())

                        #layer9 = tf.nn.relu(tf.matmul(layer8, W9))
                        layer9 = self.leaky_relu(tf.matmul(layer8, W9), 0.1)
			layer9 = tf.nn.dropout(layer9, keep_prob= self.keep_prob)

			# Tenth 
			W10 = tf.get_variable("W10", shape=[h_size, self.output_size], initializer=tf.contrib.layers.xavier_initializer())
	
			# Q prediction
            		self._Qpred = tf.matmul(layer9, W10)
            
        	# We need to define the parts of the network needed for learning a policy
        	self._Y = tf.placeholder(shape=[None, self.output_size], dtype=tf.float32)
        
        	# Loss function
		self.h_loss = self.huber_loss(self._Qpred, self._Y)
		self._loss = tf.reduce_mean(self.h_loss)
        	# Learning
        	self._train = tf.train.AdamOptimizer(learning_rate=l_rate).minimize(self._loss)
        
    	def predict(self, state, keep_prob=1):
        	x = np.reshape(state, [1, self.input_size])
        	return self.session.run(self._Qpred, feed_dict={self._X: x, self.keep_prob: keep_prob})
    
    	def update(self, x_stack, y_stack, keep_prob):
        	return self.session.run([self._loss, self._train], feed_dict={self._X: x_stack, self._Y: y_stack, self.keep_prob: keep_prob})
