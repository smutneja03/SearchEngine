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
input_value = searched_query
if searched_query is not None:
	searched_query = searched_query.lower()
else:
	searched_query = "Check123..."
	input_value = "" 
pkl_file = open('index.pkl', 'rb')
title_file = open('title.pkl', 'rb')
index = pickle.load(pkl_file)
pkl_file.close()

links_query = indexing.lookup(index, searched_query)
links_faculty = []
links_departments = []

faculty_requirements = ["People+Faculty+", "faculty.iitmandi.ac.in", "profile.php", "faculty/", "iitj.ac.in/neww/people/nfacultyprofile", ".iitgn.ac.in/faculty/"]

for link in links_query:
	for i in faculty_requirements:
		if i in link and link not in links_faculty:
			links_faculty.append(link)

for i in links_query:
	if i not in links_faculty:
		links_departments.append(i)

print "<html>"
print "<head>"
print "<title>Search Engine</title>"
print "<link href='http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css' rel='stylesheet'>"   
print "<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js'></script>"
print "<link rel='stylesheet' href='http://cdn.datatables.net/1.10.2/css/jquery.dataTables.min.css'></style>"
print "<script type='text/javascript' src='http://cdn.datatables.net/1.10.2/js/jquery.dataTables.min.js'></script>"
print "<script type='text/javascript' src='http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'></script>"

print "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css'>"


print "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css'>"

print "<script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js'></script>"

print "<script>"
print "$(document).ready(function(){"
print "    $('#myTable2').dataTable();"
print "});"
print "</script>"

print "<script>"
print "$(document).ready(function(){"
print "    $('#myTable1').dataTable();"
print "});"
print "</script>"

print "<style>"
print "table {"
print "    table-layout: fixed;"
print "    word-wrap: break-word;"
print "}"
print "</style>"
print "</head>"
print "<body style='margin-left:10px'>"
print "</br>"
print "<form action='search_engine.py' method='get'>"
print "<div class='row'>"
print "<div class='form-group col-md-6'>"
print "  <label for='inputQuery'>Enter the Query you want to search :</label>"
print "  <input type='text' class='form-control' id='inputQuery' placeholder='Enter query' name='query' value='" + input_value + "'>"
print "</div>"
print "</div>"
print "<div class='row' style='margin-left:1px'>"
print "<button type='submit' class='btn btn-primary'>Submit</button>"
print "</div>"
print "</form>"
print "</br>"
if links_query=={}:
	print "<h3>There are no results to be displayed</h3>"
else:
	#printing the webpages for faculty
	print "<div style='width:1300px'>"

	print "<div style='float:left;width:957px'>"
	serial_number = 1
	print "<table id='myTable1' class='table table-striped table-condensed' width='957px'>"
	print "<thead>"
	print "<tr>"
	print "<th class='col-md-1'>S.No.</th>"
	print "<th class='col-md-8'>Faculty Web Pages</th>"
	print "</tr>"
	print "</thead>"
	print "<tbody>"
	for i in links_faculty:
		print "<tr>"
		print "<td class='col-md-1'>%d</td>" % (serial_number)
		print "<td class='col-md-8'><a href=%s target='_blank'>%s</a></td>" % (i, i)
		print "</tr>"
		serial_number+=1
	print "</tbody>"
	print "</table>"
	print "</div>"
	
	print "<div style='float:left;margin-left:50px;width:200px;height:425px;'>"
	#for showing related search items
	related_search_terms = {"learning":["Machine Learning", "Pattern Recognition", "Computer Vision", "Speech Technology"], "Machine Learning":["Machine Learning", "Pattern Recognition", "Computer Vision", "Speech Technology"], "Pattern Recognition" : ["Machine Learning", "Pattern Recognition", "Computer Vision", "Speech Technology"]}
	print "<h2>Related search terms</h2>"
	if searched_query in related_search_terms:
		array  = related_search_terms[searched_query]
	else:
		array = ["Machine Learning", "Pattern Recognition", "Computer Vision", "Speech Technology", "Kernel Methods", "Speech Technology", "Image Processing"]
	print "<ul>"
	
	for i in array:
		url = "http://localhost:8888/cgi-bin/search_engine.py?query="
		word_array = i.split()
		for a in word_array:
			url = url + a.lower()
			url = url + '+'
		url = url[:-1]
		print "<li><a href=%s>%s</a></li>" % (url, i)
	print "</ul>"
	print "</div>"

	print "<div style='float:left;width:957px;margin-top:20px;margin-bottom:30px'>"
	serial_number = 1
	print "<table id='myTable2' class='table table-striped table-condensed' width='957px'>"
	print "<thead>"
	print "<tr>"
	print "<th class='col-md-1'>S.No.</th>"
	print "<th class='col-md-8'>Other Relevant Web Pages</th>"
	print "</tr>"
	print "</thead>"
	print "<tbody>"
	for i in links_departments:
		print "<tr>"
		print "<td class='col-md-1'>%d</td>" % (serial_number)
		print "<td class='col-md-8'><a href=%s target='_blank'>%s</a></td>" % (i, i)
		print "</tr>"
		serial_number+=1
	print "</tbody>"
	print "</table>"
	print "</div>"
	
	print "</div>"
	print "<br />"
	

print "</body>"
print "</html>"

