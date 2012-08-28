#!/usr/bin/env python

import urlparse, urllib2
import string
from BeautifulSoup import NavigableString, BeautifulSoup as bs
import re
import socket

class album_metadata:
	content = bs()
	allmusicMetadata = {}
	rymMetadata = {}
	discogsMetadata = {}
	songList = []

	def search(self, searchString, contentSite):
		''' Google I'm Feeling Lucky Search for searchString in contentSite. '''

		## Url spoofing to get past Google's bot-blocking mechanism.
		searchString = searchString.replace(" ", "+")

		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1'
		headers = {'User-Agent':user_agent,}

		url = self.pick_url(searchString, contentSite, True)
		response = self.open_url(url, headers)
		isValidUrl = response.geturl()

		while True:
			if isValidUrl.find("release") != -1 or isValidUrl.find("album") != -1 or isValidUrl.find("master") != -1:
				break
			else:
				url = self.pick_url(searchString, contentSite, False)
				response = self.open_url(url, headers)
				firstMatchingUrl = self.fallback_search(bs(response.read()))
				response = self.open_url(firstMatchingUrl, headers)
				try:
					isValidUrl = response.geturl()
				except AttributeError:
					return ""

		data = response.read()

		# BeautifulSouping the webpage.
		self.content = bs(data)
		return self.content

	def fallback_search(self, searchResult):
		''' For cases where the I'm Feeling Lucky search fails. (like The Doors by The Doors) '''
		rs = re.compile("(.*)(release|album)(.*)");
		try:
			url = searchResult.findAll("a", {"href" :rs}, limit = 1)[0].get("href")
		except IndexError:
			url = ""
		return url
	
	def pick_url(self, searchString, contentSite, imFeelingLucky):
		''' Pick between advanced search and normal search. '''
		# Toggle the I'm Feeling Lucky search option.
		if imFeelingLucky:
			# Choosing between hyperlink search (site:foo.com) and general search.
			if (contentSite.find(".") != -1):
				url = "http://www.google.com/search?hl=en&safe=off&btnI&sourceid=navclient&q=" + searchString + "+site:" + contentSite
			else:
				url = "http://www.google.com/search?hl=en&safe=off&btnI&sourceid=navclient&q=" + searchString + "+" + contentSite
		else:
			if (contentSite.find(".") != -1):
				url = "http://www.google.com/search?hl=en&safe=off&sourceid=navclient&q=" + searchString + "+site:" + contentSite
			else:
				url = "http://www.google.com/search?hl=en&safe=off&sourceid=navclient&q=" + searchString + "+" + contentSite
		return url

	def open_url(self, url, headers):
		''' Return contents of url. '''
		# Properly encode special characters in url.
		url = urllib2.quote(url, safe = ":/?&+=")

		# Make request and fetch the webpage..
		request = urllib2.Request(url, None, headers)
		try:
			response = urllib2.urlopen(request)
		except urllib2.HTTPError, e:
			return 'Oops, HTTPError.'
		except urllib2.URLError, e:
			if isinstance(e.reason, socket.timeout):
				return 'Timed out.'
			return 'URL Error.'
		except ValueError:
			return 'Invalid URL.'

		return response

	def strip_tags(self, html):
		''' Strips tags out of the html. '''
		html = re.sub('<[^<]+?>', '', html)
		return html		

	def allmusic_parse(self, allmusicSoup):
		''' Parse the scraped Allmusic data. '''

		try:
			# Parse the rating out of its <span> tag.
			rating = self.content.findAll("span", {"itemprop" :"rating"})
			rating = rating[0].findAll(text = True) # Remove tags
			rating = rating[0] + "/5"

			if not rating:
				raise IndexError
		except IndexError:
			rating = ""

		try:
			# Parse the review out of its <span> tag.
			review = self.content.findAll("span", {"itemprop" :"description"})
			review = [self.strip_tags(str(eachReview)).strip() for eachReview in review] # Remove tags

			if not review:
				raise IndexError
		except IndexError:
			review = [""]

		try:
			# List of songs in the album
			self.songList = self.content.findAll("a", {"class" :"primary_link"})
			self.songList = [song.findAll(text = True)[0] for song in self.songList]
		except IndexError:
			self.songList = []
		
		# Populate the metadata dictionary.
		self.allmusicMetadata = {'rating': rating, 'review': review}

		return self.allmusicMetadata 
		
	def rym_parse(self, rymSoup):
		''' Parse the scraped RateYourMusic data. '''

		try:
			rating = self.content.findAll("span", {"style" :"font-size:1.3em;font-weight:bold;"})
			rating = rating[0].findAll(text = True)

			ratingCount = self.content.findAll("a", {"href" :"#ratings"})
			ratingCount = ratingCount[0].findAll(text = True)
			rating = rating[0] + "/5 from " + ratingCount[0] + " ratings."

			if not rating:
				raise IndexError
		except IndexError:
			rating = ""
			
		try:	
			review = self.content.findAll("td", {"style" :"padding:25px 50px 50px 50px;"}, limit = 2)
			review = [self.strip_tags(str(eachReview)).strip() for eachReview in review]

			if not review:
				raise IndexError
		except IndexError:
			review = ["", ""]
			
		self.rymMetadata = {'rating': rating, 'review': review}

		return self.rymMetadata

	def discogs_parse(self, discogSoup):
		''' Parse the scraped Discogs data. '''

		# Hacking around the varying span class attributes for every document with regex.
		try:
			rg = re.compile("(rating_value)(\\s+)(rating)(_)(value)(_)(r)(\\d+)", re.IGNORECASE|re.DOTALL)
			
			rating = self.content.findAll("span", {"class" :rg})
			rating = rating[0].findAll(text = True)

			rc = re.compile("(rating)(_)(count)(_)(r)(\\d+)", re.IGNORECASE|re.DOTALL)
			ratingCount = self.content.findAll("span", {"class" :rc})
			ratingCount = ratingCount[0].findAll(text = True)

			rating = rating[0] + "/5 from " + ratingCount[0] + " ratings."

			if not rating:
				raise IndexError
		except IndexError:
			rating = ""

		try:		
			review = self.content.findAll("div", {"class": "squish_lines_8 comment group"})
			review = [self.strip_tags(str(eachReview)).strip() for eachReview in review]

			if not review:
				raise IndexError
		except IndexError:
			review = [""]

		self.discogsMetadata = {'rating': rating, 'review': review}

		return self.discogsMetadata

if __name__ == "__main__":
	a = album_metadata()
	stringo = "village green preservation society the kinks"
	b = a.search(stringo, "discogs")
	#a.allmusic_parse(b)
	#b = a.search('abbey road the beatles', 'rateyourmusic')
	#print b
	#a.rym_parse(b)
	#b = a.search('abbey road the beatles', 'discogs')
	a.discogs_parse(b)
	#print a.allmusicMetadata
	#print
	#print a.rymMetadata
	#print
	print a.discogsMetadata
