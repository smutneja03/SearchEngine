
import urlparse
import urllib2
import indexing
import ranking
import httplib
from bs4 import BeautifulSoup
import re
import operator
import time

from HTMLParser import HTMLParser

def get_intersection(links, temp):
	solution = []
	if links == []:
		return temp#this is for the base case
		#for the first word this will run
	elif temp == []:
		return links
	else:
		for link in temp:
			if link in links and link not in solution:
				#nned to find the intersection with the 
				#already existing links we have 
				solution.append(link)
		return solution
	
def lookup(index, keyword, rank):

	links = []
	rank_links = {}
	words = re.split(r'[ ,:\r\n]+', keyword)
	for word in words:
		if word in index:
			temp = index[word]
		else:
			temp = []

		links = get_intersection(links, temp)

	if links==[]:
		return links #if there is nothing in the links

	
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
	if word not in index:
		index[word] = [url]


def add_page_to_index(index, url, content):

	content = ''.join(content.findAll(text=True))
	words = re.split(r'[ ,:.\r\n]+', content)#split on the basis of new line and space
	
	for word in words:
		word = word.lower()
		add_to_index(index, word, url)
		

