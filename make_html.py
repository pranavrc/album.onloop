#!/usr/bin/env python
# -*- coding: utf-8 -*-

from album_metadata import *
from random import choice
from yt_fetch import *
import string

def markup(userRequest, albumInfo, contentSite, parseFunc, encoding):
	loadergif = "<img class=\"loader\" src=\"{{ url_for('static', filename='loader.gif') }}\" alt=\"Publishing...\" />"
	linebreak = "<br />"
	hrline = "<hr />"
	
	htmlfoo = albumInfo.search(userRequest, contentSite)
	parseFunc(htmlfoo)
	contentSitename = contentSite.lower()
	if contentSitename == 'allmusic'.lower():
		metadata = albumInfo.allmusicMetadata
	elif contentSitename == 'rateyourmusic'.lower():
		metadata = albumInfo.rymMetadata
	elif contentSitename == 'discogs'.lower():
		metadata = albumInfo.discogsMetadata
	elif contentSitename == 'itunes'.lower():
		metadata = albumInfo.itunesMetadata
	elif contentSitename == 'pitchfork'.lower():
		metadata = albumInfo.pitchforkMetadata
	elif contentSitename == 'sputnikmusic'.lower():
		metadata = albumInfo.sputnikmusicMetadata

	try:
		if metadata['rating']:
			ratingMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>" + contentSite.title() + "</b>" + "</a>" + " - " + metadata['rating'].decode(encoding) + linebreak
			ratingMarkedup = True
		else:
			if not albumInfo.pageUrl:
				ratingMarkup = "<a href=\"" + albumInfo.searchUrl.strip("&btnI") + '" target="_blank">' + "<b>" + contentSite.title() + "</b>" + "</a>" + linebreak
				ratingMarkedup = False
			else:
				ratingMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>" + contentSite.title() + "</b>" + "</a>" + linebreak
				ratingMarkedup = True 

		if not metadata['review'][0]:
			reviewMarkup = ""
			reviewMarkedup = False
		else:
			reviewMarkup = ""
			for eachReview in metadata['review']:
				reviewMarkup = reviewMarkup + linebreak + "<i>" + '"' + eachReview.decode(encoding) + '"' + "</i>" + linebreak

			reviewMarkedup = True

		if not ratingMarkedup and not reviewMarkedup:
			markup = ratingMarkup
		else:
			markup = ratingMarkup + reviewMarkup
	except:
		markup = "<i>Oops, content not found.</i>"
	
	if not albumInfo.pageUrl:
		html = markup + "<br/><i>Album not found.</i>" + hrline
	else:
		html = markup + hrline

	if contentSitename == 'allmusic'.lower():
		if albumInfo.songList and albumInfo.albumart:
			try:
				info = make_tracklist(albumInfo.songList).decode('utf-8') + hrline
			except:
				info = ""
			html = info + html

	return html

def make_tracklist(songList):
	tracklisting = "<b><i>Track Listing:</b></i><br/>"
	
	for eachSong in songList:
		if eachSong != songList[-1]:
			tracklisting = tracklisting + "<i>" + eachSong + "</i>" + " - "
		else:
			tracklisting = tracklisting + "<i>" + eachSong + "</i>"

	albumpic = "<img class=\"albumart\" width=\"200\" height=\"200\" src=\"./static/albumart.jpg\" alt=\"Album Art\" /><br />"
	
	html = albumpic + tracklisting
	return html

def make_html(userRequest, urlCount):
	albumInfo = album_metadata()

	loadergif = "<img class=\"loader\" src=\"{{ url_for('static', filename='loader.gif') }}\" alt=\"Publishing...\" />"
	linebreak = "<br />"
	hrline = "<hr />"
	
	if urlCount == 1:
		html = markup(userRequest, albumInfo, 'allmusic', albumInfo.allmusic_parse, 'utf-8')

	elif urlCount == 2:
		html = markup(userRequest, albumInfo, 'rateyourmusic', albumInfo.rym_parse, 'utf-8')

	elif urlCount == 3:
		html = markup(userRequest, albumInfo, 'discogs', albumInfo.discogs_parse, 'utf-8')

	elif urlCount == 4:
		html = markup(userRequest, albumInfo, 'itunes', albumInfo.itunes_parse, 'utf-8')
	
	elif urlCount == 5:
		html = markup(userRequest, albumInfo, 'pitchfork', albumInfo.pitchfork_parse, 'utf-8')

	elif urlCount == 6:
		html = markup(userRequest, albumInfo, 'sputnikmusic', albumInfo.sputnikmusic_parse, 'utf-8')

	elif urlCount == 7:
		htmlfoo = albumInfo.search(userRequest, 'allmusic')
		albumInfo.allmusic_parse(htmlfoo)
		
		if not albumInfo.songList:
			return "<i>Youtube Video not found.</i>"

		for i in range(0, 3):
			try:
				randomSongChosen = ytMetadata().SearchAndPrint(choice(albumInfo.songList) + " " + userRequest)
				break
			except:
				randomSongChosen = ""
				continue

		if not randomSongChosen:
			return "<i>Youtube Video not found.</i>"

		youtubeEmbed = '<iframe title="Youtube video player" width="420" height="315" src="http://www.youtube.com/embed/' + randomSongChosen + '" frameborder="0" allowfullscreen></iframe>'
		
		html = youtubeEmbed

	#print albumInfo.allmusicMetadata
	#print
	#print albumInfo.rymMetadata
	#print
	#print albumInfo.discogsMetadata

	#html = allmusicMarkup + hrline + rymMarkup + hrline + discogsMarkup + hrline + youtubeEmbed

	return html

if __name__ == "__main__":
	print make_html('the doors the doors', 4)
