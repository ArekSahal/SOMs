import numpy as np 
import csv

class SOMap:

	def __init__(self, n_input,n_nodes, learning_rate=0.2, method="2D", generosity=0.5):
		self.n_nodes = n_nodes
		self.n_input = n_input
		self.learning_rate = learning_rate
		self.generosity = generosity # Multiply with neighbour update
		self.labels=[]
		self.method = method
		self.w_hist = []
		self.depth_hist = []
		self.change_hist = []

		# Init the weight matrix
		self.w = np.random.rand(self.n_nodes, self.n_input)

		# Create a neighbour map where element i in nei_map contains a list A 
		# of for weight i where... I think an example would be better
		# nei_map[3[2] = a list of indicies for all nodes 2 lenghts from node 3
		self.nei_map = []
		for w1 in range(n_nodes):
			w1_neighs = [[] for i in range(n_nodes)]
			for w2 in range(n_nodes):
				if w1 != w2:
		  			dist = self.weight_distance(w1,w2, method=method)
		  			dist = int(dist)
		  			w1_neighs[dist].append(w2)
			self.nei_map.append(w1_neighs)

	def set_data(self, data, labels=[]):
	# rows = data point
	# cols = attributes

		self.data = data
		self.labels=labels
		"""
		random_data_points_index = np.random.choice(data.shape[0],self.n_nodes, replace=False)
		self.w = data[random_data_points_index,:]
		"""

	def weight_distance(self, node_index1, node_index2, method="1D"):
		if method == "2D":
	  		s = np.sqrt(self.n_nodes)
	  		rem1 = node_index1 % s
	  		rem2 = node_index2 % s
	  		return np.max([ np.abs(rem1 - rem2), np.abs(((node_index1 - rem1)/s) - ((node_index2 - rem2)/s))])


	def train(self, epochs, tune=False, max_depth=False, adapt=False):
		# Force certain neighbourhood size 
		if tune:
	  # train the network without a neighbourhood
	  		nei_sizes = [0]*epochs
		elif max_depth:
	  		nei_sizes = np.linspace(max_depth, 0, epochs)
		else:
	  		nei_sizes = np.linspace(np.floor(self.n_nodes/2), 0, epochs)


		# Adaptive Neighbourhood
		if max_depth:
	  		current_depth = max_depth
		else:
	  		current_depth = np.floor(self.n_nodes/2)

		if adapt:
	  		self.depth_hist.append(current_depth)
		self.w_hist.append(np.copy(self.w))

		# Main loop
		print("Estimated time: No idea.. but let me know when you are done!")
		for i in range(epochs):
	  		# Go through every data point
			shuffled_indx = np.arange(self.data.shape[0])
			np.random.shuffle(shuffled_indx)
			self.data = self.data[shuffled_indx,:]
			if i % (epochs*0.1)==0:
				print("Epoch: ", i)
			for p in range(self.data.shape[0]):
				point = self.data[p,:]
				winner = self.find_winner(point)
		
				if adapt:
		  			self.update(winner, point, depth=current_depth)
				else:
		  			self.update(winner, point, depth=np.round(nei_sizes[i]))

			change_percentage = np.linalg.norm(self.w - self.w_hist[-1]) / np.linalg.norm(self.w_hist[-1])
			change_percentage = np.max(change_percentage)
			self.change_hist.append(change_percentage)
			if adapt:
				self.depth_hist.append(current_depth)
				# How much have the weights changed? if small then make neighbourhood smaller
				if change_percentage < 0.01:
					if current_depth > 0:
						current_depth -= 1
					else:
						print("Done after: ", i, " epochs")
						return 0
			else:
				self.depth_hist.append(np.round(nei_sizes[i]))
			self.w_hist.append(np.copy(self.w))		

		return 0

	def find_winner(self, point):
		diffs = self.w - point
		diffs_norm = np.linalg.norm(diffs, axis=1)
		winner = np.argmin(diffs_norm)
		return winner

	def update(self, winner, p, depth=1):
		self.w[winner] = self.w[winner] + self.learning_rate*(p - self.w[winner])
		for d in range(1,int(depth) + 1):
			for nei in self.nei_map[winner][d]:
				self.w[nei] = self.w[nei] + self.learning_rate*self.generosity*(p - self.w[nei])
		return 0

	def reset(self):
		self.w = np.random.rand(self.n_nodes, self.n_input)
		self.w_hist = []
		self.depth_hist = []

	def save(self, fname="out_w.dat"):
		with open(fname, "w",newline='', ) as csvfile:
		    wr = csv.writer(csvfile, delimiter=' ', quotechar='|')
		    for row in self.w:
		         wr.writerow(row)

	def load(self, fname="out_w.dat"):
		self.w = []
		with open(fname, "r",newline='', ) as csvfile:
		    r = csv.reader(csvfile, delimiter=' ', quotechar='|')
		    for row in r:
		         self.w.append([float(i) for i in row])




