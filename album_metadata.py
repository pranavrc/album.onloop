import urlparse, urllib2
import string
from BeautifulSoup import NavigableString, BeautifulSoup as bs
import re

class album_metadata:
	content = bs()
	allmusicMetadata = {}
	rymMetadata = {}
	discogsMetadata = {}

	def imFeelingLucky(self, searchString, contentSite):
		''' Google I'm Feeling Lucky Search for searchString in contentSite. '''

		## Url spoofing to get past Google's bot-blocking mechanism.
		searchString = searchString.replace(" ", "+")

		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1'
		headers = {'User-Agent':user_agent,}

		# Choosing between hyperlink search (site:foo.com) and general search.
		if (searchString.find(".") != -1):
			url = "http://www.google.com/search?hl=en&safe=off&btnI&sourceid=navclient&q=" + searchString + "+site:" + contentSite
		else:
			url = "http://www.google.com/search?hl=en&safe=off&btnI&sourceid=navclient&q=" + searchString + "+" + contentSite
		
		# Properly encode special characters in url.
		url = urllib2.quote(url, safe = ":/?&+=")

		# Make request and fetch the webpage.
		request = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(request)
		data = response.read()

		# BeautifulSouping the webpage.
		self.content = bs(data)
		return self.content

	def strip_tags(self, html):
		''' Strips tags out of the html. '''
		html = re.sub('<[^<]+?>', '', html)
		return html		

	def allmusic_parse(self, allmusicSoup):
		''' Parse the scraped Allmusic data. '''

		# Parse the rating out of its <span> tag.
		rating = self.content.findAll("span", {"itemprop" :"rating"})
		rating = rating[0].findAll(text = True) # Remove tags
		rating = rating[0] + "/5"

		# Parse the review out of its <span> tag.
		review = self.content.findAll("span", {"itemprop" :"description"})
		review = [self.strip_tags(str(eachReview)).strip('\n') for eachReview in review] # Remove tags

		# List of songs in the album
		songList = self.content.findAll("a", {"class" :"primary_link"})
		songList = [song.findAll(text = True)[0] for song in songList]
		
		# Populate the metadata dictionary.
		self.allmusicMetadata = {'rating': rating, 'review': review}
		return self.allmusicMetadata 
		
	def rym_parse(self, rymSoup):
		''' Parse the scraped RateYourMusic data. '''

		rating = self.content.findAll("span", {"style" :"font-size:1.3em;font-weight:bold;"})
		rating = rating[0].findAll(text = True)
		
		ratingCount = self.content.findAll("a", {"href" :"#ratings"})
		ratingCount = ratingCount[0].findAll(text = True)

		rating = rating[0] + "/5 from " + ratingCount[0] + " ratings."

		review = self.content.findAll("td", {"style" :"padding:25px 50px 50px 50px;"}, limit = 2)
		review = [self.strip_tags(str(eachReview)).strip('\n') for eachReview in review]
		
		self.rymMetadata = {'rating': rating, 'review': review}

		return self.rymMetadata

	def discogs_parse(self, discogSoup):
		''' Parse the scraped Discogs data. '''

		# Hacking around the varying span class attributes for every document with regex.
		rg = re.compile("(rating_value)(\\s+)(rating)(_)(value)(_)(r)(\\d+)", re.IGNORECASE|re.DOTALL)
		rating = self.content.findAll("span", {"class" :rg})
		rating = rating[0].findAll(text = True)

		rc = re.compile("(rating)(_)(count)(_)(r)(\\d+)", re.IGNORECASE|re.DOTALL)
		ratingCount = self.content.findAll("span", {"class" :rc})
		ratingCount = ratingCount[0].findAll(text = True)

		rating = rating[0] + "/5 from " + ratingCount[0] + " ratings."
		
		review = self.content.findAll("div", {"class": "squish_lines_8 comment group"})
		review = [self.strip_tags(str(eachReview)).strip('\n') for eachReview in review]

		self.discogsMetadata = {'rating': rating, 'review': review}

		return self.discogsMetadata

if __name__ == "__main__":
	a = album_metadata()
	b = a.imFeelingLucky('abbey road the beatles', 'allmusic')
	a.allmusic_parse(b)
	b = a.imFeelingLucky('abbey road the beatles', 'rateyourmusic')
	#print b
	a.rym_parse(b)
	b = a.imFeelingLucky('abbey road the beatles', 'discogs')
	a.discogs_parse(b)
	print a.allmusicMetadata
	print
	print a.rymMetadata
	print
	print a.discogsMetadata
