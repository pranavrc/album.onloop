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
		ratingMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>" + contentSite.title() + "</b>" + "</a>" + " - " + metadata['rating'].decode('utf-8') + linebreak
		reviewMarkup = ""
		for eachReview in metadata['review']:
			reviewMarkup = reviewMarkup + linebreak + "<i>" + '"' + eachReview.decode('utf-8') + '"' + "</i>" + linebreak
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
		html = markup(userRequest, albumInfo, 'allmusic', albumInfo.allmusic_parse)

	elif urlCount == 2:
		html = markup(userRequest, albumInfo, 'rateyourmusic', albumInfo.rym_parse)

	elif urlCount == 3:
		html = markup(userRequest, albumInfo, 'discogs', albumInfo.discogs_parse)

	elif urlCount == 4:
		html = markup(userRequest, albumInfo, 'itunes', albumInfo.itunes_parse)

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
