

def lookup(index, keyword):

	links = []#will store the links where the keyword is found

	for entry in index:
		#dictionary key consists of string that could contain our keyword
		if( keyword.lower() in entry.lower()):
			for link in index[entry]:
				if link not in links:
					links.append(link)#will add the link in the links list

	#after traversing the entire indexer will return the links list
	return links

def add_to_index(index, line, url):
	#index now is a dictionary that maintains constant lookup time
	if line in index and url not in index[line]:
		index[line].append(url)
	else:
		#not present in the dictionary
		index[line] = [url]


def add_page_to_index(index, url, content):

	lines = content.split('\n')
	#content is divided based on new line

	for line in lines:
		#every line is checked and then added to indexer DS
		add_to_index(index, line, url)


