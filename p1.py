

#Avery Tan(altan:1392212), Canopus Tong(canopus:1412275)

import numpy as np 



k_num_runs = [1,2,3,4,5,6,7,8] #the number of runs
s_num_samples = 10 # value of s




if __name__ == '__main__':
	for i in k_num_runs:
		tot_instances = 0
		instances_inside_unit_circle = 0

		for j in range(s_num_samples**i): #perform this 10**k times
			tot_instances+=1
			x = np.random.uniform() #random real number between [0,1]
			y = np.random.uniform()
			if (x**2 + y**2 < 1):
				instances_inside_unit_circle+=1

		pi = (4* instances_inside_unit_circle)/tot_instances
		print('Approximate value: ', pi, 'error: ', abs(pi-np.pi))



