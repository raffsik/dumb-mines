import numpy as np
from numpy.random import randint
from scipy.signal import convolve2d

class Board:
	def __init__(self,width=10,height=10,n_bombs=10):
		self.width = width
		self.height = height
		self.n_bombs = n_bombs
		self.shape = (width, height)

	def generate(self):
		self.bombs = np.zeros(shape = (self.width, self.height), dtype=np.int8)
		
		placed = 0
		while placed < self.n_bombs:
			x = randint(0, self.width)
			y = randint(0, self.height)

			if self.is_bomb(x,y):
				continue

			self.bombs[x,y] = 1
			placed += 1

		self.compute_counts()


	def compute_counts(self):
		ker = np.array([[1,1,1],[1,0,1],[1,1,1]])
		self.counts = convolve2d(self.bombs, ker, 'same')

	def is_bomb(self,x,y):
		return self.bombs[x,y] == 1

	def is_empty(self,x,y):
		return self.counts[x,y] == 0

	def load(self,file):
		pass

class Game:
	def __init__(self):
		pass

	def start(self):
		print('#'*20)
		print("## Mines of doom v0.1\n")
		
		width = int(input("Width: "))
		height = int(input("Height: "))
		n_bombs = int(input("Bombs: "))

		self.board = Board(width,height,n_bombs)
		self.board.generate()
		
		self.alive = True
		self.revealed = np.zeros(shape = self.board.shape)
	
	def print_board(self):

		for x in range(self.board.width):
			for y in range(self.board.height):
				if self.revealed[x,y]:
					if self.board.bombs[x,y]:
						print('B', end = ' ')
					else:
						print(self.board.counts[x,y], end = ' ')
				else:
					print('X', end=' ')
			print()
	
	def check(self,x,y):    

		c=False
		
		if 0<=x<self.board.width and 0<=y<self.board.height:
			c=True
		return c

	def run(self):
		
		print('#'*20)
		self.print_board()

		print("Your next move (format X Y): ",end='')
		x, y = [int(i) for i in input().split()]
		c=self.check(x,y)

		while c==False:
			print("Your next move (format X Y): ",end='')
			x, y = [int(i) for i in input().split()]
			c=self.check(x,y)
			
		if self.board.is_bomb(x,y):
			self.revealed = np.ones(shape=self.board.shape)
			self.alive = False
			self.game_over()
		else:
			self.revealed[x,y] = 1
			

		return self.alive

	def game_over(self):
		print('#'*20)
		self.print_board()

		print('Enjoy getting blown :3')
if __name__ == "__main__":
	
	game = Game()
	game.start()

	while True:
		if not game.run():
			break
