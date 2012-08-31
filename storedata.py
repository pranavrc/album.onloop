#!/usr/bin/env python

from album_metadata import *
import urllib2
from BeautifulSoup import BeautifulSoup as bs
import socket
import json
import os
import cPickle as pickle

def strip_tags(html):
	''' Strips tags out of the html. '''
	html = re.sub('<[^<]+?>', '', html)
	return html

def writeJson():
	user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1'
	headers = {'User-Agent':user_agent,}
	albumsList = []
	for count in range(1, 51):
		url = "http://rateyourmusic.com/charts/top/album/all-time/" + str(count)
		a = album_metadata()
		b = a.open_url(url, headers).read()
		content = bs(b)
		albums = content.findAll("span", {"style" :"font-size:x-large;"})
		albums = [strip_tags(str(eachAlbum)) for eachAlbum in albums]
		albumsList.extend(albums)

	albums = {'albums' :albumsList}

	f = open("static/list_of_albums.json", 'w')

	jsonEncode = json.dumps(albums)

	f.write(jsonEncode)
	f.close()

def readJson():
	f = open("static/list_of_albums.json").read()
	data = json.loads(f)
	return data

def storeVar(var):
	pickle.dump(var, open("userdata.p", "wb"))

def loadVar():
	var = pickle.load(open("userdata.p", "rb"))
	return var

def removePickle():
	if os.path.exists('userdata.p'):
		os.remove('userdata.p')

if __name__ == "__main__":
	writeJson()
	#username = "foo"
	#storeVar(username)
	#print loadVar(username)
