
def compute_ranks(graph):
	d = 0.8 #damping factor
	num_loops = 17

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1/npages
	#initialising the rank of all the pages present in the dictionary

	for i in range(0, num_loops):
		#iterating predefined number of times
		new_ranks = {}
		#will store the newly formed values at every iteration
		for page in graph:
			#computing page rank of each page in graph
			new_rank = (1-d)/npages
			#initialising with a fixed value
			#implies user stick to the page accessing
			for node in graph:
				#will be going over every node and checking 
				#the pages that outlinks to this page in hand
				if page in graph[node]:
					#if page is present in the outlink of any node
					#contribution of that node is added to its new rank calculation
					new_rank += d * (ranks[node]/len(graph[node]))
			new_ranks[page] = new_rank
		ranks = new_ranks
		#ranks is updated with the newly computed values
		#this value will be used again in future
	return ranks
