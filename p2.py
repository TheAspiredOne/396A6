

#Avery Tan(altan:1392212), Canopus Tong(canopus:1412275)

import numpy as np 



k_num_runs = [1,2,3,4,5,6,7,8] #the number of runs
s_num_samples = 10 # value of s
true_val = 4/3.0 - np.cos(1)




if __name__ == '__main__':
	for i in k_num_runs:
		tot_instances = 0
		area = 0

		for j in range(s_num_samples**i): #perform this 10**k times
			tot_instances+=1
			x = np.random.uniform() #random real number between [0,1]
			area += np.sin(x)+x**2

		approx_area = 1/float(tot_instances)*area
		print('Approximate area: ', approx_area, 'error: ', abs(approx_area- true_val))



