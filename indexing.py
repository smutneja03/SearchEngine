
import re

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

def lookup(index, keyword):

	links = []
	for string in index:
		if keyword in string:
			for link in index[string]:
				links.append(link)

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


