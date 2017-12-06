#Avery Tan(altan:1392212), Canopus Tong(canopus:1412275)

import sys
import numpy as np
import time
import copy


move_rng = None
world_rng = None



def check_valid(out,seed,n,size,colours,minballs,MC_runs):
	'''
	ensure that the command line arguements are within valid ranges
	'''
	if (out < -1):
		raise ValueError('invalid argv for out')
	if (n <= 0):
		raise ValueError('invalid argv for n')
	if (size < 6) or (size > 10):
		raise ValueError('invalid argv for size')
	if (colours < 2) or (colours > 6):
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



def init_game_state(size, colours):
	'''
	initialize starting board positions
	'''
	global move_rng, world_rng

	colour_list = np.arange(1, colours+1) #get a range in which each int in this range corresponds to one colour
	board = np.zeros((size*size))
	board = board.reshape(size,size)

	for i in range(size):
		for j in range(size):
			board[i][j] = float(world_rng.randint(1,colours+1))

	# print('init board',board)
	return board



def perform_action(action, board, size, colours):
	'''
	this is the state transition function which returns a list of all the tiles 
	that will be removed as a result of the action
	'''
	global move_rng, world_rng


	tiles_removed = [action] # stores list of tiles that will be removed
	neighbours_seen = set() #used to check if weve already been to a particular node
	colour = board[action]

	neighbours = get_neighbours(action[0], action[1], size) #gets initial neighbours
	neighbours_seen.add(action) #adds starting node to seen


	def perform_DFS(a, size, board, tiles_removed, neighbours_seen):
		neighbours = get_neighbours(a[0], a[1], size)
		for i in neighbours:
			if i not in neighbours_seen:
				x,y = i
				if board[x][y] == board[a[0]][a[1]]:
					tiles_removed.append(i)
					neighbours_seen.add(i)
					tiles_removed, neighbours_seen = perform_DFS(i, size, board, tiles_removed, neighbours_seen)
		return tiles_removed, neighbours_seen


	for i in neighbours:
		if i not in neighbours_seen:
			x,y = i
			if board[x][y] == colour:
				tiles_removed.append(i)
				neighbours_seen.add(i)
				tiles_removed, neighbours_seen = perform_DFS(i, size, board, tiles_removed, neighbours_seen)
			else:
				neighbours_seen.add(i)



	#perform removal
	board_copy = copy.deepcopy(board)
	x_dimens = set()
	for i in tiles_removed:
		board_copy[i[0]][i[1]] = 0.0
		x_dimens.add(i[1])

	# gravity acts on the tiles above the now-removed-tiles
	for j in x_dimens:
		for i in range(size): #start iterating from the top
			if board_copy[i][j]==0.0: #we hae empty tile, check tile above it
				if (i-1)>=0: #check that there is a tile above the empty tile
					if board_copy[i-1][j] != 0.0: #the tile above the empty tile is a NON-EMPTY tile
						for q in range(i,0,-1): #for everything above this non-empty tile
							board_copy[q][j] = board_copy[q-1][j] #move everything down by 1
						board_copy[0][j]= 0.0 # since everything has moved down by one, the top is now empty

	

	#check for empty columns and move stuff over by one if there is
	gen_new_col_flag = False #used to signal new col required
	for j in range(size-1, -1, -1): #iterate from the right towards the left
		if board_copy[size-1][j] == 0.0: #empty column found
			gen_new_col_flag = True 
			for q in range(j,0,-1): # for the newly found empty column, and everything to its left:
				for i in range(size): #for every row in this col
					# if (q-1) >=0: #ensure
					board_copy[i][q] = board_copy[i][q-1] #copy over cols
	if gen_new_col_flag == True:
		colour_list = np.arange(1, colours+1)
		for i in range(size):
			board_copy[i][0] = float(world_rng.randint(1,colours+1))

	score = len(tiles_removed) **2
	# print(tiles_removed)
	# print('\n' ,board_copy, '\n\n\n')
	return board_copy, score



def get_neighbours(i,j,size):
	neighbours  = list()
	if (i+1) < size:
		neighbours.append((i+1,j))
	if (i-1) >= 0:
		neighbours.append((i-1,j))
	if (j+1) < size:
		neighbours.append((i,j+1))
	if (j-1) >= 0:
		neighbours.append((i,j-1))

	return neighbours



def get_legal_moves(board, size):
	"""
	get list of legal moves
	"""
	been_there = set()
	legal_moves = list()

	for i in range(size): # these 2 for loops will iterate through every tile on the board
		for j in range(size):

			if (i,j) not in been_there: #check if each tile has already been 'seen'
				been_there.add((i,j))
				if board[i][j] == 0.0: #if empty
					continue
				neighbours = get_neighbours(i, j, size)
				for z in neighbours:
					x,y = z
					if board[i][j]==board[x][y]:
						legal_moves.append((i,j))
						if board[x][y] not in been_there:
							been_there.add((x,y))
							legal_moves.append((x,y))

	return legal_moves



def play_game(size, colours, minballs, MC_runs):
	'''
	function that plays the game
	'''
	global move_rng, world_rng

	history = list() #history of the game. Used for replay later
	score = [0]
	action = None
	action_list= list()
	board = init_game_state(size, colours) #init the starting board positions
	legal_moves = get_legal_moves(board, size) #list of legal moves


	board_copy = copy.deepcopy(board)
	history.append(board_copy) #add init state to history

	
	
	while legal_moves: #while there is still a move to play
		if MC_runs == 0:
			action = move_rng.randint(len(legal_moves)) #select move randomly
			action = legal_moves[action]
			action_list.append(action)
		else:
			for i in range(MC_runs):
				pass
		# print('init\n',board_copy)
		res_board, a_score = perform_action(action, board_copy, size, colours) #perform action
		score.append(a_score)
		board_copy = copy.deepcopy(res_board) #copy the new board and update board_copy
		history.append(board_copy) #add to history
		legal_moves = get_legal_moves(board_copy, size)


		# print(action,'\n' ,res_board, '\n\n\n')
		

	# print(len(history))
	# for i in history:
	# 	print(i, '\n')
	# print(legal_moves)
	action_list.append(None)

	return history, action_list, score



def output(board_sequence, action_sequence, score_sequence, output_options, size):
	'''
	replays games based on the desired output format
	'''
	global world_rng, move_rng
	master_moves = 0.0
	master_score = 0.0
	score_inper_game = list()
	moves_inper_game = list()


	if output_options == -1:
		colour_dict = { 0.0: '--', 1.0: '##', 2.0: 'oo', 3.0: '++', 4.0: '$$', 5.0: 'xx', 6.0: '&&' }
		x_label = '  '
		for i in range(size):
			x_label+= str(i)+' '


		#converting our representation into the one specified by the assg specs
		for i in range(len(board_sequence)): #for each game
			game_num = i+1 #game number starts at 0. is 0-index. so add 1
			tot_moves = len(action_sequence[i])-1 #play_game() added an extra 'None' to the action_sequence list to prevent going out of index range
			master_moves+=tot_moves #add to the TOTAL TOTAL moves over all games
			moves_inper_game.append(tot_moves) #add to this list which will be used to calc std_dev
			tot_score = 0 #tot score for only this game
			for uber in score_sequence[i]: #running out of variables
				tot_score+=uber #calculate total score for this game
			master_score+=tot_score #add to the TOTAL score over all games
			score_inper_game.append(tot_score) #add to this list which will be used to calc std_dev
			curr_score = 0 #curr score is the current score of a particular timestep

			for j in range(len(board_sequence[i])): #for each timestep in the ith game
				curr_score+=score_sequence[i][j] #update curr score of this timestep. score_sequence[i][0] = 0

				for k in range(len(board_sequence[i][j])): #for each row of our board in the curr timestep. Used to translate to assg specs

					res=str((size-1)-k)+'|' #(0,0) was the top left corner in our representation. It is not in the assg spec. Hence, convert
					for l in board_sequence[i][j][k]: #change colour repr from 1-6 to values in colour_dict. Change empty repr from 0.0 to '--'
						res+= colour_dict[l]
					res+='|'
					print(res)
				print(x_label) # bottom x axis labels

				move = action_sequence[i][j]
				if move != None: #don't print out action_sequence[i][-1]
					move_x = str(move[1])
					move_y = str((size-1) - int(move[0]))
					print('move:', move_x, move_y)


					print('m_ind:', j+1, 'of', tot_moves, 'move-score:', score_sequence[i][j+1], 'score:', curr_score, 'of', tot_score)
			
			avg_moves = master_moves/(i+1) # i starts at 0, hence i+1
			avg_score = master_score/(i+1)

			#calc std dev for moves
			move_err = 0.0
			for lud in moves_inper_game:
				move_err += (lud - avg_moves)**2
			std_dev_moves = (move_err/(float(len(moves_inper_game))))**(0.5)


			#calc std dev for score
			score_err = 0.0
			for lud in score_inper_game:
				score_err += (lud- avg_score)**2
			std_dev_scores = (score_err/(float(len(score_inper_game))))**(0.5)



			print('game', i+1, 'moves:', tot_moves, avg_moves, '(', std_dev_moves, ')', 'score:', tot_score, avg_score, '(', std_dev_scores,')')





				# print(game_num, j, '\n')
			# print(i,'\n')		
	

	elif output_options == 0:
		tot_moves = 0.0
		tot_score = 0.0
		num_games = len(score_sequence)
		

		std_score_list = list()
		std_moves_list = list()


		for i in range(num_games):
			moves = len(action_sequence[i])
			std_moves_list.append(moves)
			tot_moves+=moves


			score = 0.0
			for j in score_sequence[i]:
				score += j 
			std_score_list.append(score)
			tot_score += score


			avg_score = tot_score/(i+1)
			avg_moves = tot_moves/(i+1)


			std_err_moves = 0.0
			std_err_scores = 0.0
			for z in std_score_list:
				std_err_scores += (avg_score-z)**2
			for z in std_moves_list:
				std_err_moves += (avg_moves-z)**2

			std_dev_moves = (std_err_moves/(i+1.0))**(0.5)
			std_dev_scores = (std_err_scores/(i+1.0))**(0.5)

			print('game', i+1, 'moves:', moves, avg_moves, '(', std_dev_moves, ')', 'score:', score, avg_score, '(', std_dev_scores, ')')


	elif output_options > 0:
		#TODO color stuff
		pass

	return



if __name__ == '__main__':
	if len(sys.argv) != 8:
		raise ValueError('missing arguements. Expecting 7 cmd arguements')
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

		# print(out,seed,n,size,colours,minballs,MC_runs)
		check_valid(out,seed,n,size,colours,minballs,MC_runs) # check that cmd argv are within valid ranges


	move_rng, world_rng = init_random_num_gen(seed) # set up random num gen
	

	#play n games
	master_history = list()
	master_scores = list()
	master_actions = list()
	for i in range(n):
		history, action, score = play_game(size, colours, minballs, MC_runs)
		master_history.append(history)
		master_scores.append(score)
		master_actions.append(action)

	output(master_history, master_actions, master_scores, out, size)





