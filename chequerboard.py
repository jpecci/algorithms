import numpy as np
from decorators import time_func

DIR_N =(-3, 0)
DIR_NE=(-2,+2)
DIR_E =( 0,+3)
DIR_SE=(+2,+2)
DIR_S =(+3, 0)
DIR_SW=(+2,-2)
DIR_W =( 0,-3)
DIR_NW=(-2,-2)

dirs=[DIR_N, DIR_NE, DIR_E, DIR_SE, DIR_S, DIR_SW, DIR_W, DIR_NE]

def move(pos, dir):
	i_pos, j_pos=pos
	i_dir, j_dir=dir
	return (i_pos+i_dir, j_pos+j_dir)


@time_func
def fill_board(start_pos, size_i, size_j):
	board= -np.ones(shape=(size_i, size_j))
	counter=0
	
	def helper(curr_pos, counter):
		if counter == size_i*size_j:
			return True
		for dir in dirs:
			next_pos=move(curr_pos, dir)
			next_i, next_j =next_pos
			if  0 <= next_i and next_i < size_i and \
			    0 <= next_j and next_j < size_j:
				
				if board[next_i, next_j]<0:
					board[next_i, next_j]=counter
					if helper(next_pos, counter+1):
						return True #stop after the first solution is found
					
					board[next_i, next_j]=-1
	
	i,j=start_pos
	board[i,j]=counter
	helper(start_pos, counter+1)
	return board  

if __name__=="__main__":
	start_pos=(3,3)
	ans=fill_board(start_pos, 6,6)
	print ans