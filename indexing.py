
import re
import operator

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def lookup(index, keyword, rank):

	links = []
	rank_links = {}
	words = keyword.split()
	for string in index:
		#going through all the keys in the dict
		for word in words:
			#splitting the query into words
			if word in string:
				#checking whether the query exists in the key
				#if exists its added to the links if not present
				for link in index[string]:
					if link not in links:
						links.append(link)

	#here we have the links sorted in an random order
	#need to sort the links on the basis of the ranks we have
	for link in links:
		#traversing the links of the solution
		if link in rank:#rank is dict with link to score mapping
			rank_links[link] = rank[link]
		else:
			rank_links[link] = 0

	#need to sort the dictionary on the basis of values
	sorted_ranks = sorted(rank_links.items(), key=operator.itemgetter(1))
	#list of tupples will be formed from which links needs to be extracted
	sorted_ranks = sorted_ranks[::-1]

	links = [x[0] for x in sorted_ranks]
	return links

def add_to_index(index, word, url):
	
	if word in index and url not in index[word]:
		index[word].append(url)
	else:
		index[word] = [url]


def add_page_to_index(index, url, content):

	content = strip_tags(content)
	words = content.split(' ')
	for word in words:
		word = word.lower()
		add_to_index(index, word, url)


