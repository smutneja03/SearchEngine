

def lookup(index, keyword):

	links = []#will store the links where the keyword is found

	for entry in index:#will check the first half of evey value in index
		if( keyword.lower() in entry[0].lower() and entry[1] not in links):
			links.append(entry[1])#will add the link in the links list

	#after traversing the entire indexer will return the links list
	return links

def add_to_index(index, line, url):

	for entry in index:
		if(line in entry[0] and url not in entry[1]):
			#will append the url if the line already exists
			entry[1].append(url)
			return 
	#will add a new item in the list along with the URL
	index.append([line, [url]])


def add_page_to_index(index, url, content):

	lines = content.split('\n')
	#content is divided based on new line

	for line in lines:
		#every line is checked and then added to indexer DS
		add_to_index(index, line, url)


