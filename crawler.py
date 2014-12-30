
import urlparse
import urllib2
import indexing
import httplib
from bs4 import BeautifulSoup

def is_valid_link(link):

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
		except urllib2.HTTPError, e:
			html_text = e.read()
		except urllib2.URLError, e:
			html_text = e.read()

		soup = BeautifulSoup(html_text)

		url = tocrawl.pop(0)

		for tag in soup.findAll('a', href=True):
			tag['href'] = urlparse.urljoin(url, tag['href'])
			if "faculty" in tag['href'] and tag['href'] not in crawled and is_valid_link(tag['href']):
				tocrawl.append(tag['href'])
				crawled.append(tag['href'])
				indexing.add_page_to_index(index, tag['href'], html_text)

	return index

seed = "http://www.iitmandi.ac.in/institute/faculty.html"

index = crawl_web(seed)

print str(len(index)) + " is the length of the index formed"

while 1:

	string = raw_input("Enter your query")
	links_query = indexing.lookup(index, string)
	print '\n'
	print "Links with the keyword " + string
	
	for i in links_query:
		print i

	print '\n'





