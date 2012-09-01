#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse, urllib2, urllib
import string
from BeautifulSoup import NavigableString, BeautifulSoup as bs
import re
import socket
from werkzeug import url_fix
import json

socket.setdefaulttimeout(3)

class album_metadata:
	content = bs()
	allmusicMetadata = {}
	rymMetadata = {}
	discogsMetadata = {}
	itunesMetadata = {}
	pitchforkMetadata = {}
	sputnikmusicMetadata = {}
	songList = []
	pageUrl = ""
	albumart = ""
	searchUrl = ""
	rymUrlValid = False

	def search(self, searchString, contentSite):
		''' Google I'm Feeling Lucky Search for searchString in contentSite. '''

		## Url spoofing to get past Google's bot-blocking mechanism.
		searchString = searchString.replace(" ", "+")

		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1'
		headers = {'User-Agent':user_agent,}

		url = self.pick_url(searchString, contentSite, True)
		response = self.open_url(url, headers)
		try:
			isValidUrl = response.geturl()
		except:
			return ""

		while True:
			if (isValidUrl.find(contentSite.lower()) != -1) and (isValidUrl.find("release") != -1 or isValidUrl.find("album") != -1 or isValidUrl.find("master") != -1 or isValidUrl.find("review") != -1):
				if contentSite.lower() == 'rateyourmusic':
					if isValidUrl.find("buy") == -1 or self.rymUrlValid:
						break
					else:
						response = self.urlhelper(searchString, contentSite, headers)
						try:
							isValidUrl = response.geturl()
						except AttributeError:
							return ""
				break
			else:
				response = self.urlhelper(searchString, contentSite, headers)
				try:
					isValidUrl = response.geturl()
				except AttributeError:
					return ""

		self.pageUrl = isValidUrl
		data = response.read()

		# BeautifulSouping the webpage.
		self.content = bs(data)
		return self.content

	def urlhelper(self, searchString, contentSite, headers):
		''' Do a fallback search on invalid URL. '''
		url = self.pick_url(searchString, contentSite, False)
		response = self.open_url(url, headers)
		firstMatchingUrl = self.fallback_search(bs(response.read()), contentSite)
		response = self.open_url(firstMatchingUrl, headers)
		return response

	def fallback_search(self, searchResult, contentSite):
		''' For cases where the I'm Feeling Lucky search fails. (like The Doors by The Doors) '''
		rs = re.compile("(.*)(" + contentSite.lower() + ")(.*)(release|album|master|review)(.*)");
		i = 0
		while True:
			try:
				url = searchResult.findAll("a", {"href" :rs})[i].get("href")
				if contentSite.lower() == 'rateyourmusic':
					if url.find('buy') != -1:
						i += 1
						continue
					else:
						break
				break
			except:
				if contentSite.lower() == 'rateyourmusic':
					if i > 0:
						url = searchResult.findAll("a", {"href" :rs}, limit = 1)[0].get("href")
						self.rymUrlValid = True
					else:
						self.rymUrlValid = True
				else:
					url = ""
				break
		return url

	def pick_url(self, searchString, contentSite, imFeelingLucky):
		''' Pick between advanced search and normal search. '''
		# Toggle the I'm Feeling Lucky search option.
		if imFeelingLucky:
			# Choosing between hyperlink search (site:foo.com) and general search.
			if (contentSite.find(".") != -1):
				url = "http://www.google.com/search?hl=en&safe=off&btnI&sourceid=navclient&q=" + urllib.quote_plus(searchString.encode('utf-8')) + "+site:" + urllib.quote_plus(contentSite.encode('utf-8'))
			else:
				url = "http://www.google.com/search?hl=en&safe=off&btnI&sourceid=navclient&q=" + urllib.quote_plus(searchString.encode('utf-8')) + "+" + urllib.quote_plus(contentSite.encode('utf-8'))
		else:
			if (contentSite.find(".") != -1):
				url = "http://www.google.com/search?hl=en&safe=off&sourceid=navclient&q=" + urllib.quote_plus(searchString.encode('utf-8')) + "+site:" + urllib.quote_plus(contentSite.encode('utf-8'))
			else:
				url = "http://www.google.com/search?hl=en&safe=off&sourceid=navclient&q=" + urllib.quote_plus(searchString.encode('utf-8')) + "+" + urllib.quote_plus(contentSite.encode('utf-8'))

		self.searchUrl = url
		return url

	def open_url(self, urlS, headers):
		''' Return contents of url. '''
		# Properly encode special characters in url.
		url = url_fix(urlS)

		# Make request and fetch the webpage..
		request = urllib2.Request(url, None, headers)
		try:
			response = urllib2.urlopen(request, timeout = 3)
		except:
			return 'Oops, something went wrong.'

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
			rating = "<b>" + rating[0] + "/5" + "</b>"

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
			self.songList = [song.findAll(text = True)[0].encode('utf-8') for song in self.songList]
		except IndexError:
			self.songList = []

		if self.songList:
			try:
				self.albumart = self.content.findAll("div", {"class" :"image-container"}, limit = 1)[0].get("data-large")
				self.albumart = json.loads(self.albumart)["url"]
				urllib.urlretrieve(str(self.albumart), "./static/albumart.jpg")
			except:
				self.albumart = []

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
			rating = "<b>" + rating[0] + "/5" + "</b>" + " from " + "<b>" + ratingCount[0] + " ratings" + "</b>" + "."

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

			rating = "<b>" + rating[0] + "/5" + "</b>" + " from " + "<b>" + ratingCount[0] + " ratings" + "</b>" + "."

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

	def itunes_parse(self, itunesSoup):
		''' Parse the scraped iTunes Store data. '''

		try:
			rg = re.compile("(.+)(\\s+)(stars)(,)(\\s+)(.+)(\\s+)(Ratings)")

			rating = self.content.findAll("div", {"aria-label" :rg})[0].get("aria-label")

			rating = "<b>" + rating + "</b>"

			if not rating:
				raise IndexError
		except IndexError:
			rating = ""

		try:
			review = self.content.findAll("div", {"class" :"product-review"})

			if not review:
				review = self.content.findAll("div", {"class" :"customer-review"}, limit = 1)

			review = [self.strip_tags(str(eachReview)).strip() for eachReview in review]

			review[0] = review[0][13:]

			if not review:
				raise IndexError
		except IndexError:
			review = [""]

		self.itunesMetadata = {'rating': rating, 'review': review}

		return self.itunesMetadata

	def pitchfork_parse(self, pitchforkSoup):
		''' Parse the scraped Pitchfork data. '''

		try:
			rg = re.compile("(score)(\\s+)(score)(-)(\\d+)(-)(\\d+)")
			rating = self.content.findAll("span", {"class" :rg}, limit = 1)
			rating = rating[0].findAll(text = True)

			rating = "<b>" + rating[0].strip() + "/10" + "</b>"

			if not rating:
				raise IndexError
		except IndexError:
			rating = ""

		try:
			review = self.content.findAll("div", {"class" :"editorial"}, limit = 1)
			review = [self.strip_tags(str(eachReview)).strip() for eachReview in review]

			if not review:
				raise IndexError
		except IndexError:
			review = [""]

		self.pitchforkMetadata = {'rating': rating, 'review': review}

		return self.pitchforkMetadata

	def sputnikmusic_parse(self, sputnikmusicSoup):
		''' Parse the scraped Sputnikmusic data. '''
		try:
			rating = self.content.findAll("font", {"size" :"5", "color" :"#FF0000"})
			rating = rating[0].findAll(text = True)

			rating = "<b>" + rating[0].strip() + "/5" + "</b>"

			if not rating:
				raise IndexError
		except IndexError:
			rating = ""

		try:
			review = self.content.findAll("font", {"size" :"2", "class" :"defaulttext"}, limit = 1)
			review = [self.strip_tags(str(eachReview)).strip() for eachReview in review]

			rg = re.compile("(\\d+)( of )(\\d+)( thought this review was well written)");
			rc = re.compile("(Share:)(.*)");

			review[0] = re.sub(rg, '<br />', review[0])
			review[0] = review[0].replace("\n", "")
			review[0] = re.sub(rc, '', review[0])#.decode('ISO-8859-1').encode('utf-8')

			# Bad Hack to get around ISO-8859-1 to UTF-8 conversion issues.
			rc = re.compile('(&)((?:[a-z][a-z]+))(;)(&)((?:[a-z][a-z]+))(;)')
			review[0] = re.sub(rc, '', review[0])
			rc = re.compile('(â|€)')
			review[0] = re.sub(rc, '', review[0])
			#review[0] = review[0].replace('€', '')
			#review[0] = review[0].replace('â', '\'')

			if not review:
				raise IndexError
		except IndexError:
			review = [""]

		self.sputnikmusicMetadata = {'rating': rating, 'review': review}

		return self.sputnikmusicMetadata

if __name__ == "__main__":
	a = album_metadata()
	stringo = "abbey road"
	b = a.search(stringo, "rateyourmusic")
	#a.sputnikmusic_parse(b)
	#print a.sputnikmusicMetadata
	#a.pitchfork_parse(b)
	#print a.pitchforkMetadata
	#a.allmusic_parse(b)
	#b = a.search('abbey road the beatles', 'rateyourmusic')
	print b
	#a.rym_parse(b)
	#b = a.search('abbey road the beatles', 'discogs')
	#a.discogs_parse(b)
	#print a.allmusicMetadata
	#print
	#print a.rymMetadata
	#print
	#print a.discogsMetadata
	#a.itunes_parse(b)
	#print a.itunesMetadata
