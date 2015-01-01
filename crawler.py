
import urlparse
import urllib2
import indexing
import httplib
from bs4 import BeautifulSoup

def is_valid_link(link):
	#checks if the link is valid by first checking the format of the url
	#if format is valid sends a request to the server for a positive response

	if ("http://" not in link and "https://" not in link) or " " in link:
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

		indexing.add_page_to_index(index, url, html_text)
		#each of the page popped out of the queue is added to the indexer
		crawled.append(url)
		#once the url is added to the indexer, its added in the crawled list

		for tag in soup.findAll('a', href=True):
			#finds all the anchor tags and processes them one by one
			tag['href'] = urlparse.urljoin(url, tag['href'])
			if "faculty" in tag['href'] and tag['href'] not in crawled and is_valid_link(tag['href']):
				tocrawl.append(tag['href'])
				
	return index

seed = "http://www.iitmandi.ac.in/institute/faculty.html"

index = crawl_web(seed)

print str(len(index)) + " is the length of the index formed"

while 1:

	string = raw_input("Enter your query\n")
	string = string.lower()
	links_query = indexing.lookup(index, string)
	print '\n'
	print "Links with the keyword " + string
	
	for i in links_query:
		print i

	print '\n'
