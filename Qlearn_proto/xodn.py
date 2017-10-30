import numpy as np

def reward_done_check(pre_degree, degree):
        if abs(int(degree[0])) > abs(int(pre_degree[0])):
                if abs(degree[1]) < abs(pre_degree[1]) :
                        print "1"
			return -abs(int(degree[0])), False
                else:
                        if np.sign(degree[1]) * np.sign(degree[0]) == -1:
                                print "2"
                                return -abs(int(degree[0])), False
                        else:
				print "3"
                                print "degree finish"
                                return -abs(int(degree[0])), True
        else:
		print "4"
                return -abs(int(degree[0])), False

pre_degree = [0.04, 208.6]
degree = [1.98, 211.71]

print reward_done_check(pre_degree, degree)
