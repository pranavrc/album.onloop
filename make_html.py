from album_metadata import *
from random import choice
from yt_fetch import *
import string

def markup(userRequest, albumInfo, contentSite, parseFunc):
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

	try:
		ratingMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>" + contentSite.title() + "</b>" + "</a>" + "-" + metadata['rating'].decode('utf-8') + linebreak + "<i>"
		print ratingMarkup
		reviewMarkup = ""
		for eachReview in metadata['review']:
			reviewMarkup = reviewMarkup + linebreak + '"' + eachReview.decode('utf-8') + '"' + "</i>" + linebreak
		markup = ratingMarkup + reviewMarkup
	except:
		markup = "Oops, content not found."

	html = markup + hrline

	return html

def make_html(userRequest, urlCount):
	albumInfo = album_metadata()

	loadergif = "<img class=\"loader\" src=\"{{ url_for('static', filename='loader.gif') }}\" alt=\"Publishing...\" />"
	linebreak = "<br />"
	hrline = "<hr />"
	
	if urlCount == 1:
		#htmlfoo = albumInfo.search(userRequest, 'allmusic')
		#albumInfo.allmusic_parse(htmlfoo)

		#try:
		#	allmusicMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>Allmusic</b>" + "</a>" + " - " + albumInfo.allmusicMetadata['rating'].decode('utf-8') + linebreak + "<i>" + '"' + albumInfo.allmusicMetadata['review'][0].decode('utf-8') + '"' + "</i>"
		#except (KeyError, IndexError) as e:
		#	allmusicMarkup = 'Could not fetch content.'
	
		#html = allmusicMarkup + hrline
		html = markup(userRequest, albumInfo, 'allmusic', albumInfo.allmusic_parse)

	elif urlCount == 2:
		htmlfoo = albumInfo.search(userRequest, 'rateyourmusic')
		albumInfo.rym_parse(htmlfoo)
		
		try:
			rymMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>Rate Your Music</b>" + "</a>" + " - " + albumInfo.rymMetadata['rating'].decode('utf-8') + linebreak + "<i>" + '"' + albumInfo.rymMetadata['review'][0].decode('utf-8') + '"' + linebreak + linebreak + '"' + albumInfo.rymMetadata['review'][1].decode('utf-8') + '"' + "</i>"
		except (KeyError, IndexError) as e:
			rymMarkup = 'Could not fetch content.'

		html = rymMarkup + hrline

	elif urlCount == 3:
		htmlfoo = albumInfo.search(userRequest, 'discogs')
		albumInfo.discogs_parse(htmlfoo)
		
		try:
			discogsMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>Discogs</b>" + "</a>" + " - " + albumInfo.discogsMetadata['rating'].decode('utf-8') + linebreak + "<i>" + '"' + albumInfo.discogsMetadata['review'][0].decode('utf-8') + '"' + "</i>"
		except (KeyError, IndexError) as e:
			discogsMarkup = 'Could not fetch content.'

		html = discogsMarkup + hrline

	elif urlCount == 4:
		htmlfoo = albumInfo.search(userRequest, 'itunes')
		albumInfo.itunes_parse(htmlfoo)

		try:
			itunesMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>iTunes Store</b>" + "</a>" + " - " + albumInfo.itunesMetadata['rating'].decode('utf-8') + linebreak + "<i>" + '"' + albumInfo.itunesMetadata['review'][0].decode('utf-8') + '"' + "</i>"
		except (KeyError, IndexError) as e:
			itunesMarkup = 'Could not fetch content.'

		html = itunesMarkup + hrline

	elif urlCount == 5:
		htmlfoo = albumInfo.search(userRequest, 'allmusic')
		albumInfo.allmusic_parse(htmlfoo)

		try:
			randomSongChosen = ytMetadata().SearchAndPrint(choice(albumInfo.songList) + " " + userRequest)
		except:
			randomSongChosen = ""

		if not randomSongChosen:
			return "Video not found."

		youtubeEmbed = '<iframe width="420" height="345" src="http://www.youtube.com/embed/' + randomSongChosen + '"></iframe>'
		
		html = youtubeEmbed

	#print albumInfo.allmusicMetadata
	#print
	#print albumInfo.rymMetadata
	#print
	#print albumInfo.discogsMetadata

	#html = allmusicMarkup + hrline + rymMarkup + hrline + discogsMarkup + hrline + youtubeEmbed

	return html

if __name__ == "__main__":
	print make_html('london calling', 4)
