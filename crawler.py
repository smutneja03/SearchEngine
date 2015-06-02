
import urlparse
import urllib2
import indexing
import ranking
import httplib
from bs4 import BeautifulSoup
import pickle

def is_valid_link(link):
	#checks if the link is valid by first checking the format of the url
	#if format is valid sends a request to the server for a positive response
	extras = ["doc", "pdf", " ", "https", "JPG", "#", "family", "Participation", "PDF", "gif", "mailto:", "javascript:", "[", "]"]
	for i in extras:
		if i in link:
			return False
	if "http://" not in link and "iitmandi" not in link and "www.iitr" not in link and "www.iitbbs" not in link and "www.iitp.ac" not in link and "www.iitj.ac" not in link:
		return False
	if "faculty" not in link and "Faculty" not in link and "profile.php" not in link:
		return False
	try:
		check = urllib2.urlopen(link)
	except urllib2.URLError as e:
		check = e
	
	if check.code in (200, 401):
		return True
	else:
		return False


index = {}
graph = {}

def crawl_web(seed):

	tocrawl = [seed]
	crawled = []

	while tocrawl:
		try:
			html_text = urllib2.urlopen(tocrawl[0]).read()
			#stores the html content of the document in unstructured format
		except urllib2.HTTPError, e:
			html_text = "e.read()"
		except urllib2.URLError, e:
			html_text = "e.read()"

		soup = BeautifulSoup(html_text)
		#converts the html into object, which represents document as nested data structure
		url = tocrawl.pop(0)
		
		if soup.title is not None:
			title_url = soup.title.string
		else:
			title_url = url

		indexing.add_page_to_index(index, url, soup, title_url) #each of the page popped out of the queue is added to the indexer
		outlinks = []
		anchor_tags = soup.findAll('a', href=True)#finds all the anchor tags and processes them one by one
		for tag in anchor_tags:
			print tag['href'] + " caused error"
			tag['href'] = tag['href'].replace("]", "") 
			tag['href'] = urlparse.urljoin(url, tag['href']) #decomposes the relative path into the absolute one
			print tag['href'] + " caused error"
			if tag['href'] not in outlinks:
				outlinks.append(tag['href']) #building the list of outlinks from a given link
			if tag['href'] not in crawled and tag['href'] not in tocrawl and is_valid_link(tag['href']):
				#print tag['href']
				crawled.append(tag['href'])
				if "faculty" in tag['href'] and "iitmandi" in tag['href']:
					#IIT MANDI faculty	
					tocrawl.append(tag['href'])
					print tag['href']
				elif "departments" in tag['href'] and "iitr" in tag['href'] and "Faculty" in tag['href']:
					#IIT ROORKEE faculty	
					tocrawl.append(tag['href'])
					print tag['href']
				elif "profile.php" in tag['href'] and "iitbbs" in tag['href']:
					tocrawl.append(tag['href'])
					print tag['href']
				elif "faculty" in tag['href'] and "iitgn" in tag['href']:
					tocrawl.append(tag['href'])
					print tag['href']
				elif "nfacultyprofile" in tag['href']:
					tocrawl.append(tag['href'])
					print tag['href']
				elif "iitp.ac.in" in tag['href'] and "faculty" in tag['href']:
					tocrawl.append(tag['href'])
					print tag['href']
					
		#adding a mapping of the url to all of its outlink to the graph
		graph[url] = outlinks
				
	return index, graph

iit_roorkee = ["http://www.iitr.ac.in/departments/ASE/pages/Index.html",
			"http://www.iitr.ac.in/departments/BT/pages/index.html",
			"http://www.iitr.ac.in/departments/CH/pages/index.html",
			"http://www.iitr.ac.in/departments/CY/pages/index.html",
			"http://www.iitr.ac.in/departments/CE/pages/index.html",
			"http://www.iitr.ac.in/departments/CSE/pages/index.html",
			"http://www.iitr.ac.in/departments/EE/pages/index.html",
			"http://www.iitr.ac.in/departments/ECE/pages/Home.html",
			"http://www.iitr.ac.in/departments/HS/pages/About_the_Department___.html",
			"http://www.iitr.ac.in/departments/MA/pages/index.html",
			"http://www.iitr.ac.in/departments/ME/pages/index.html",
			"http://www.iitr.ac.in/departments/MT/pages/index.html",
			"http://www.iitr.ac.in/departments/PH/pages/index.html"]

iit_mandi = ["http://www.iitmandi.ac.in/institute/faculty.html"]

iit_bhubaneswar = ["http://www.iitbbs.ac.in/faculty-members.php"]

iit_bombay = ["http://www.cse.iitb.ac.in/page14"]

iit_gandhinagar = ["http://www.iitgn.ac.in/faculty.htm"]

iit_jodhpur = ["http://www.iitj.ac.in/neww/people/?id=Faculty"]

iit_patna = ["http://www.iitp.ac.in/index.php/schools-and-centers/engineering/computer-science-a-engineering/people/faculty.html",
"http://www.iitp.ac.in/index.php/schools-and-centers/engineering/electrical-engineering/people/faculty.html",
"http://www.iitp.ac.in/index.php/schools-and-centers/engineering/mechanical-engineering/people/faculty.html",
"http://www.iitp.ac.in/index.php/schools-and-centers/engineering/civil-engineering/people/faculty.html",
"http://www.iitp.ac.in/index.php/schools-and-centers/engineering/chemical-and-biochemical-engineering/people-chemical-and-biochemical-engg/faculty-cbe.html",
"http://www.iitp.ac.in/index.php/schools-and-centers/engineering/material-science-and-engineering/people-mse/faculty-mse.html"]


seed = iit_patna + iit_jodhpur + iit_mandi + iit_roorkee + iit_gandhinagar + iit_bhubaneswar

for i in seed:
	index, graph = crawl_web(i)

output = open('index.pkl', 'wb')
pickle.dump(index, output)
output.close()
