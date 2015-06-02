# SearchEngine
This thesis will talk about the prototype of a search engine that takes specialization as input
and returns back the list of relevant faculty members as output in the order of priority. 
Crawling, indexing and ranking are basically the three things that this model will be performing in 
order to return the results. The crawler in totality will be covering a total of six IIT’s in its domain. 
The results that the search engine will return will be from these institutes only. 
The crawled pages will then be saved in the index where for each of the word we will have the location 
of its occurence i.e. URL of the document. In addition to the location, count of the word in the link 
will also be saved. This will be used by the ranker to compute the order the results will be displayed in. 
Finally it will be the user who will enter the query and based on the keywords used in the query relevant
links will be returned. The relevance of the links will be decided by the number of occurences of these
keywords in these links. A GUI for the engine will help the user to interact with the system and analyse 
the results more efficiently.

One can access the live working of the project at the URL mentioned below :
http://sahilmutneja.com/cgi-bin/search_engine.py
