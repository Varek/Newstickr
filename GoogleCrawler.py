import httplib
import json
import logging
import socket
import time
import urllib
import feedparser

BLOG_SEARCH_HOST="http://blogsearch.google.com/blogsearch_feeds?hl=de&"
BLOG_SEARCH_PATH_AFTER="&lr=&ie=utf-8&num=5&output=atom"
NEWS_SEARCH_HOST="news.google.com/news?"
NEWS_SEARCH_PATH_AFTER="&num=5&output=atom"
 
 
class GoogleCrawler(object):
    ''' Crawl twitter search API for matches to specified tag.  Use since_id to
    hopefully not submit the same message twice.  However, bug reports indicate
    since_id is not always reliable, and so we probably want to de-dup ourselves
    at some level '''
 
    def __init__(self, tag, t):
        self.tag = tag
        self.t = t
 
    def search(self):
    	if self.t == "NEWS":
    		path = NEWS_SEARCH_HOST + 'q=' + self.tag + NEWS_SEARCH_PATH_AFTER
    	else:
        	path = BLOG_SEARCH_HOST + 'q=' + self.tag + BLOG_SEARCH_PATH_AFTER
        rssentries = feedparser.parse(path).entries
        res = []
        for ens in rssentries:
        	entry = [ens.title, ens.link]
       	 	res.append(entry)
        return res
 
 
    def submit(self, data):
         res=[]
         for date in data:
            res.append(twitter.Status.NewFromJsonDict(date))
         #print res
         return res
         
#tag = GoogleCrawler(100000000,'rhok',10)
#print tag.search()
#print tag.TwitterSearches
#print tag.searchResultsArray
		 
