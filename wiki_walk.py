# wiki_walk.py
#https://science.rpi.edu/sites/default/files/Aug07%20Part%20I%20and%20II.pdf
# Find the shortest path between two Wikipedia articles by following
# links. This program retrieves Wikipedia articles from the internet
# and performs a breadth-first traversal (retrieving at most 2000
# pages) to find the shortest path.
#
# Usage: python3 wiki_walk.py <first article name> <second article name>
# 
# Where each article name is the name of the article as it appears in a
# Wikipedia URL. For example, the Wikipedia page for the University of 
# Victoria has the URL
#   https://en.wikipedia.org/wiki/University_of_Victoria
# so the article name would be "University_of_Victoria".
#
# For example, try
#   python3 wiki_walk.py "University_of_Victoria" "Great_Pyramid_of_Giza"
# or
#   python3 wiki_walk.py "Raspberry" "Franz_Kafka"
#
#
# Note: This program downloads a large number of pages from a web server
# in quick succession. Wikipedia allows "friendly" web crawling activities,
# which do not require high bandwidth. The "max_visits" variable below limits
# the total number of retrieved pages to 2000, to keep the amount of bandwidth
# low. If you write your own web crawler, keep in mind that many web servers 
# will block repeated requests from the same source (since such requests will
# drain server resources and may be interpreted as a denial-of-service attack).
#
#
# B. Bird - 07/09/2016


import urllib.request
import sys
import re

start = sys.argv[1]
finish = sys.argv[2]

#Set the maximum number of pages to fetch to 2000
#Do not change this unless you want to risk having your IP blocked by the server.
max_visits = 2000
total_visits = 0

#Given an article name, return the URL of the corresponding article
def get_wikipedia_url(article_title):
	return 'https://en.wikipedia.org/wiki/%s'%article_title
	
	
#Given the complete HTML data for an article, find all HTML links
#to URLs of the form https://en.wikipedia.org/wiki/<article_name>
#and ignore any article names containing : or # characters.
#Article titles containing colons indicate that the page is not
#a regular article, and the # character is used for intra-article
#links (such as links to sections of the current article).
def find_matching_links(article_text):
	return re.findall('<a href="/wiki/([^#:"]*)"',article_text)
	
#Given an article title, retrieve the HTML data for the page.
#The urllib.request module allows a web page to be opened like a file.
def get_page_data(article_title):
	global total_visits
	total_visits += 1
	if total_visits > max_visits:
		return ''
	url = get_wikipedia_url(article_title)
	with urllib.request.urlopen(url) as f:
		data = f.read().decode('utf-8')
	print("Retrieved %d bytes (%s)"%(len(data),url),file=sys.stderr)
	return data
	
	
#Perform a breadth-first search (BFS) traversal starting at the
#first article until either the limit is reached or the second
#article is found. Graph traversal algorithms like BFS are covered in CSC 225.
links = {}
parents = {}
pages_found = set()
to_visit = []

to_visit.append(start)
pages_found.add(start)
parents[start] = None

i = 0
while i >= 0 and i < len(to_visit):
	article_title = to_visit[i]
	i += 1
	
	article_data = get_page_data(article_title)
	links = set(find_matching_links(article_data))
	print("Article %s: %d links"%(article_title,len(links)))
	for link in links:
		if link not in pages_found:
			pages_found.add(link)
			parents[link] = article_title
			to_visit.append(link)
			if link == finish:
				i = -1
				break
	
	
#If, when the traversal finished, the second article
#is among the articles found, then a path exists from
#article start to article finish. Trace backwards from
#the article finish through the BFS tree to generate the
#path.
if finish in parents:
	chain = []
	t = finish
	while t is not None:
		print('---'+t)
		chain.append(t)
		t = parents[t]
	chain = chain[::-1]
	print('%d steps:'%len(chain))
	for c in chain:
		print('\t'+c)
else:
	print('Couldn\'t find page %s'%finish)
	
	