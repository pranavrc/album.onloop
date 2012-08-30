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
	elif contentSitename == 'pitchfork'.lower():
		metadata = albumInfo.pitchforkMetadata

	try:
		if metadata['rating']:
			ratingMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>" + contentSite.title() + "</b>" + "</a>" + " - " + metadata['rating'].decode('utf-8') + linebreak
			ratingMarkedup = True
		else:
			ratingMarkup = "<a href=\"" + albumInfo.pageUrl + '" target="_blank">' + "<b>" + contentSite.title() + "</b>" + "</a>" + linebreak
			ratingMarkedup = False

		if not metadata['review'][0]:
			reviewMarkup = ""
			reviewMarkedup = False
		else:
			reviewMarkup = ""
			for eachReview in metadata['review']:
				reviewMarkup = reviewMarkup + linebreak + "<i>" + '"' + eachReview.decode('utf-8') + '"' + "</i>" + linebreak
			reviewMarkedup = True

		if not ratingMarkedup and not reviewMarkedup:
			markup = ratingMarkup
		else:
			markup = ratingMarkup + reviewMarkup
	except:
		markup = "Oops, content not found."
	
	if not albumInfo.pageUrl:
		html = markup + "<br/><i>Album not found.</i>" + hrline
	else:
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
		html = markup(userRequest, albumInfo, 'pitchfork', albumInfo.pitchfork_parse)

	elif urlCount == 6:
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
