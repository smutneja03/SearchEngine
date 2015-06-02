#!/usr/bin/python
print "Content-type:text/html\r\n\r\n"
# Import modules for CGI handling 
import cgi, cgitb, pickle 
import urlparse
import urllib2
import indexing
import ranking
import httplib
from bs4 import BeautifulSoup

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
searched_query = form.getvalue('query')
if searched_query is not None:
	searched_query = searched_query.lower()
else:
	searched_query = "Check123..." 

pkl_file = open('index.pkl', 'rb')
index = pickle.load(pkl_file)
pkl_file.close()

links_query = indexing.lookup(index, searched_query)
links_faculty = []
links_departments = []

for link in links_query:
	if "People+Faculty+" in link or "faculty.iitmandi.ac.in" in link:
		links_faculty.append(link)
	else:
		links_departments.append(link)

print "<html>"
print "<head>"
print "<title>Search Engine</title>"
print "</head>"
print "<body>"
print "<form action='test.py' method='get'>"
print "Enter the query you want to search :<br/> <input type='text' name='query'> <br />"
print "<input type='submit' value='Submit' />"
print "</form>"

if links_query=={}:
	print "<h3>There are no results to be displayed</p>"
else:
	#printing the webpages for faculty
	print "<h2>Faculty Web Pages</h2>"
	print "<ul>"
	count = 0
	for i in links_faculty:
		print "<li>"
		print "<h4><a href=%s target='_blank'>%s</a></h4>" % (i, i)
		print "</li>"
		count+=1
	print "</ul"
	print "<h3>A total of %d results displayed</h3>" % count
	
	#printing the webpages for departments
	print "<h2>Department Web Pages</h2>"
	print "<ul>"
	count = 0
	for i in links_departments:
		print "<li>"
		print "<h4><a href=%s target='_blank'>%s</a></h4>" % (i, i)
		print "</li>"
		count+=1
	print "</ul"
	print "<h3>A total of %d results displayed</h3>" % count

print "</body>"
print "</html>"

