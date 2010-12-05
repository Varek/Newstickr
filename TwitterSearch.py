import TagCrawler
from oauth import oauth
from oauthtwitter import OAuthApi


def authorize():
	consumer_key = "KEKjQDvICVkstzgVsmiEHA"
	consumer_secret = "uBWsy1mwWpXN4f7TgDnWJpYWn43FFv0gdVRVb3WWMI"
	oauth_token = '222826358-YGWpuFgehEDb9pAuxWm7CGZKSLKdkEqi2Vnbj0fF'
	oauth_token_secret = 'BwbyKqDAc37FKO21IMJEAGBUJOuZNN2Qpv4jOrfes'
	return OAuthApi(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
	
def retweetCount(oAuth, status_id):
	print oAuth
	print status_id
	callurl = "statuses/retweets/" + status_id
	print callurl
	retweets = oAuth.ApiCall(callurl)
	print retweets
	return len(retweets)
	

# Retweet counting
#twitter = authorize()
#user_timeline = twitter.GetHomeTimeline()
#print retweetCount(twitter,"16208928355")


#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(user_timeline)

#tag = TagCrawler.TagCrawler(100000000,'rhok+nyc',10) 


def keywordsToQuery(keywords):
	return keywords.replace(' ','+')
	
class Twittersearch(object):

	def __init__(self, query=None):
		self.query = query
		self.crawler = TagCrawler.TagCrawler(100000000,self.query,10)
		self.results = None
	
	def search(self):
		self.results = self.crawler.search()

class GNewssearch(object):

	def __init__(self, query=None):
		self.query = query
		self.crawler = TagCrawler.TagCrawler(100000000,self.query,10)
		self.results = None
	
	def search(self):
		self.results = self.crawler.search()
		
class Blogsearch(object):

	def __init__(self, query=None):
		self.query = query
		self.crawler = TagCrawler.TagCrawler(100000000,self.query,10)
		self.results = None
	
	def search(self):
		self.results = self.crawler.search()
		
class CombinedSearch(object):
	
	def __init__(self, keywordArrays):
		self.searchResultsArray = []
		self.combinedSearchResults = []
		self.TwitterSearches = []
		self.NewsSearches = []
		self.BlogSearches = []
		self.searches = []
		for keywords in keywordArrays:
			query = keywordsToQuery(keywords)
			self.TwitterSearches.append(Twittersearch(keywords))
			#self.NewsSearches.append(GNewssearch(keywords))
			#self.BlogSearches.append(Blogsearch(keywords))
		self.searches.extend(self.TwitterSearches)
		#self.searches.extend(self.NewsSearches)
		#self.searches.extend(self.BlogSearches)
		
		
	def search(self):
		for s in self.searches:
			s.search()
			self.searchResultsArray.append(s.results)
			self.combinedSearchResults.extend(s.results)
			#print ts.results
		
		
		
		
if __name__ == '__main__':
	tag = CombinedSearch(['rhok nyc', 'berlin'])
	tag.search()
	#print tag.TwitterSearches
	#print tag.searchResultsArray

	
	
		
	
	
