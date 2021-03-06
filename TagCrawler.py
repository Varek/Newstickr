import httplib
import json
import logging
import socket
import time
import urllib
import twitter
from Config import Config

SEARCH_HOST="search.twitter.com"
SEARCH_PATH="/search.json"
 
 
class TagCrawler(object):
    ''' Crawl twitter search API for matches to specified tag.  Use since_id to
    hopefully not submit the same message twice.  However, bug reports indicate
    since_id is not always reliable, and so we probably want to de-dup ourselves
    at some level '''
 
    def __init__(self, max_id, tag, interval):
        self.max_id = max_id
        self.tag = tag
        self.interval = interval
 
    def search(self):
        c = httplib.HTTPConnection(SEARCH_HOST)
        params = {'q' : self.tag}
        if self.max_id is not None:
            params['since_id'] = self.max_id
            #params['geocode'] = "37.781157,-122.398720,1mi"
            params['rpp'] = Config.rpp
        path = "%s?%s" %(SEARCH_PATH, urllib.urlencode(params))
        print path
        try:
            c.request('GET', path)
            r = c.getresponse()
            data = r.read()
            c.close()
            try:
                result = json.loads(data)
            except ValueError:
                return None
            if 'results' not in result:
                return None
            self.max_id = result['max_id']
            return self.submit(result['results'])
        except (httplib.HTTPException, socket.error, socket.timeout), e:
            logging.error("search() error: %s" %(e))
            return None
 
    def loop(self):
        while True:
            logging.info("Starting search")
            data = self.search()
            if data:
                logging.info("%d new result(s)" %(len(data)))
                self.submit(data)
            else:
                logging.info("No new results")
            logging.info("Search complete sleeping for %d seconds"
                    %(self.interval))
            time.sleep(float(self.interval))
 
    def submit(self, data):
         res=[]
         for date in data:
            stat =  twitter.Status.NewFromJsonDict(date)
            res.append([stat.text,stat.GetStatusURL()])
         #print res
         return res
		 
