#Avery Tan(altan:1392212), Canopus Tong(canopus:1412275)

import sys
import numpy as np
import time


def check_valid(out,seed,n,size,colours,minballs,MC_runs):
	'''
	ensure that the command line arguements are within valid ranges
	'''
	if (out != -1) or (out != 0) or (out > 0):
		raise ValueError('invalid argv for out')
	if (n <= 0):
		raise ValueError('invalid argv for n')
	if (size < 6) or (size > 10):
		raise ValueError('invalid argv for size')
	if (colours < 2) OR (colours > 6):
		raise ValueError('invalid argv for colours')
	if (minballs < 1) or (minballs > size):
		raise ValueError('invalid argv for minballs')
	if (MC_runs < 0):
		raise ValueError('invalid argv for MC_runs') 



def init_random_num_gen(seed):
	a = np.random.RandomState()
	b = np.random.RandomState()		
	if (seed != 0):
		a.seed(seed)
		b.seed(seed)
		return (a,b)
	elif (seed == 0):
		seed = int(time.time())
		a.seed(seed)
		seed = int(time.time())
		b.seed(seed)
		return (a,b)



def check_legal_moves():




def play_game():
	check_legal_moves()


def output(game_state, output_options):









if __name__ == '__main__':
	if len(sys.argv) != 8:
		print('must be 8!!')
	else:
		''': (output mode) 0: no replay output when a game is finished, 
		-1: plain text state/move replay output, 
		k > 0: coloured state/move replay output, 
		waiting k milliseconds after each listed
		move and additional k milliseconds after a game ends
		'''
		out = int(sys.argv[1])


		'''(random number seed) 0: initialize random number 
		generators with a time based seed,
		k != 0: initialize them with k'''
		seed = int(sys.argv[2])


		n = int(sys.argv[3]) # num of games/runs
		size = int(sys.argv[4]) #board width/height [6,10]
		colours = int(sys.argv[5]) #num of ball colours [2,6]
		minballs = int(sys.argv[6]) #min num of balls in new columns [1,size]
		MC_runs = int(sys.argv[7]) #num MC runs per move [0,inf]


		check_valid(out,seed,n,size,colours,minballs,MC_runs) # check that cmd argv are within valid ranges


	move_rng, world_rng = init_random_num_gen(seed)
	

	for i in range(n):
		game_details = play_game()
		output(game_details,out)






