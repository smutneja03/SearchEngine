
import urlparse
import urllib2
import indexing
import ranking
import httplib
from bs4 import BeautifulSoup

def is_valid_link(link):
	#checks if the link is valid by first checking the format of the url
	#if format is valid sends a request to the server for a positive response

	if ("http://" not in link and "https://" not in link) or " " in link:
		return False
	if "doc" in link or "pdf" in link:
		return False
		
	try:
		check = urllib2.urlopen(link)
	except urllib2.URLError as e:
		check = e

	if check.code in (200, 401):
		return True
	else:
		return False



def crawl_web(seed):

	tocrawl = [seed]
	crawled = []
	index = {}
	graph = {}

	while tocrawl:
		try:
			html_text = urllib2.urlopen(tocrawl[0]).read()
			#stores the html content of the document in unstructured format
		except urllib2.HTTPError, e:
			html_text = e.read()
		except urllib2.URLError, e:
			html_text = e.read()

		soup = BeautifulSoup(html_text)
		#converts the html into object, which represents document as nested data structure

		url = tocrawl.pop(0)
		
		indexing.add_page_to_index(index, url, soup) #each of the page popped out of the queue is added to the indexer
		crawled.append(url) #once the url is added to the indexer, its added in the crawled list
		
		outlinks = []
		for tag in soup.findAll('a', href=True): #finds all the anchor tags and processes them one by one
			
			tag['href'] = urlparse.urljoin(url, tag['href']) #decomposes the relative path into the absolute one
			
			if tag['href'] not in outlinks:
				outlinks.append(tag['href']) #building the list of outlinks from a given link
			
			if tag['href'] not in crawled and is_valid_link(tag['href']):
				if "faculty" in tag['href']:
					#IIT MANDI faculty	
					tocrawl.append(tag['href'])
		
		#adding a mapping of the url to all of its outlink to the graph
		graph[url] = outlinks
				
	return index, graph

seed = "http://www.iitmandi.ac.in/institute/faculty.html"

index, graph = crawl_web(seed)
ranks = ranking.compute_ranks(graph)#function call to get the ranks dictioanary

while 1:

	string = raw_input("Enter your specialization query\n")
	string = string.lower()
	links_query = indexing.lookup(index, string, ranks)
	print '\n'
	print "Links with the keyword " + string
	
	if links_query==[]:
		print "There are no results to be displayed"
	else:
		for i in links_query:
			print i

	print '\n'
