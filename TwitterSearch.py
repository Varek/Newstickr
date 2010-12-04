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

	def __init__(self, keywords=None):
		self.query = keywordsToQuery(keywords)
		self.crawler = TagCrawler.TagCrawler(100000000,self.query,10)
		self.results = None
	
	def search(self):
		self.results = self.crawler.search()
		
class CombinedTwittersearch(object):
	
	def __init__(self, keywordArrays):
		self.searchResultsArray = []
		self.combinedSearchResults = []
		self.TwitterSearches = []
		for keywords in keywordArrays:
			self.TwitterSearches.append(Twittersearch(keywords))
		
	def search(self):
		for ts in self.TwitterSearches:
			ts.search()
			self.searchResultsArray.append(ts.results)
			#print ts.results
		
		
		
tag = CombinedTwittersearch(['rhok nyc', 'berlin'])
tag.search()
#print tag.TwitterSearches
#print tag.searchResultsArray


	
	
		
	
	
