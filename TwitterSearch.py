import TagCrawler
import GoogleCrawler
from oauth import oauth
from oauthtwitter import OAuthApi
from Config import Config
import oauth_keys
	
def authorize():
	return OAuthApi(oauth_keys.consumer_key, oauth_keys.consumer_secret, oauth_keys.oauth_token, oauth_keys.oauth_token_secret)
	
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
		self.crawler = GoogleCrawler.GoogleCrawler(self.query,"NEWS")
		self.results = None
	
	def search(self):
		self.results = self.crawler.search()
		
class Blogsearch(object):

	def __init__(self, query=None):
		self.query = query
		self.crawler = GoogleCrawler.GoogleCrawler(self.query,"BLOG")
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
		self.TwitterSearchResults = []
		self.NewsSearchResults = []
		self.BlogSearchResults = []
		self.SearchesByTopic = []
		ts = bs = ns = None
		for keywords in keywordArrays:
			query = keywordsToQuery(keywords)
			if Config.useTwitter:
				print "twitwitwit"
				ts = Twittersearch(query)
				self.TwitterSearches.append(ts)
			if Config.useBlogSearch:
				bs = Blogsearch(query)
				self.BlogSearches.append(bs)
			if Config.useNewsSearch:
				ns = GNewssearch(query)
				self.NewsSearches.append(ns)
			for s in [ts,bs,ns]:
				self.SearchesByTopic.append(s)
		self.searches.append(self.TwitterSearches)
		self.searches.append(self.BlogSearches)
		self.searches.append(self.NewsSearches)
		
		
	def search(self):
		for st in self.searches:
			for s in st:
				s.search()
				self.searchResultsArray.append(s.results)
				self.combinedSearchResults.extend(s.results)
				#print ts.results
		
		
		
		
if __name__ == '__main__':
	tag = CombinedSearch(['rhok nyc', 'berlin'])
	tag.search()
	#print tag.TwitterSearches
	#print tag.searchResultsArray

	
	
		
	
	
