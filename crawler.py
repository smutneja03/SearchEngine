
#Code for Crawler
#given program starts from a page and crawls 

import urllib2#will be used for opening the url
import indexing#contians fuctions of the indexing module

def get_page(url):

	req = urllib2.Request(url)
	#get the response by opening the url
	#getting the response from the request issued
	
	try:
		response = urllib2.urlopen(req)
		#get the html content of the url in html variable
		html = response.read()
		#return the html variable
		return html
	
	except urllib2.HTTPError, e:
		return e.read()


def get_next_target(page):

	start_link = page.find('<a href=')

	if(start_link==-1):
		return None, 0
 
	start_quote = page.find('"', start_link)
	#stores the first location of start quote 
	end_quote = page.find('"', start_quote+1)
	#stores the last location of end quote
	url = page[start_quote+1 : end_quote]
	#url stores the firt link present in the string page

	return url, end_quote

def get_all_links(page, link):

	links = []
	#used to store all the links while crawler will run
	while True:
		#loop will run till we find all the links on the given page
		url, endpos = get_next_target(page)

		if url is not None:#url will store None when there are no more links on the page
			url_base = link.rsplit("/", 2)#will split the string into three parts

		if url and "../" in url:
			url = url.replace("..", url_base[0])#will replace the string
		
		elif url and "../" not in url and "http://" not in url and "https://" not in url:
			url = url_base[0] + "/" + url_base[1] + "/" + url
		#if the page is in the same directory as that of the current page

		if url and ( "http://" in url or "https://" in url):
			if "faculty" in url and "iitmandi" in url:
				links.append(url)
				#link is appended when we are talking only about the faculty
			page = page[endpos:]
			#page will start from the end point of the url and will have the rest page
		else:
			break

	#links contains all the links present on the entered page		
	return links


def union(p, q):
	#given two lists, combines them to contain distinct elements present in the two list
	#and returns the final list after modifying p
	for element in q:
		#checks each element of second list
		if element not in p:
			#if not present in the first list appends it to it
			p.append(element)

def crawl_web(seed):
	#procedure to crawl the whole of web
	tocrawl = [seed]#starts with the page entered by the user
	crawled = []#will list all the pages that are crawled
	index = {}#will contain the word to url mapping
	while tocrawl:
		link = tocrawl.pop()
		#page stores the link of the last popped out item from the tocrawl list
		if link not in crawled:
			#to avoid repetition checking if the page is already explored
			#it avoids cycles
			content = get_page(link)#stores the content of the page
			indexing.add_page_to_index(index, link, content)#add it to indexer
			union(tocrawl, get_all_links(content, link))
			crawled.append(link)
	#will list all the pages that will be crawled starting from the seed page
	return index


seed = "http://www.iitmandi.ac.in/institute/faculty.html"
index = crawl_web(seed)
print len(index)

while 1:
	string = raw_input("Indexer is ready, Enter your string :: ")
	links_query = indexing.lookup(index, string)
	print '\n'
	print "Links with the keyword " + string
	
	for i in links_query:
		print i

	print '\n'

