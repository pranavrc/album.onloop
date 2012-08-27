from album_metadata import *
from random import choice
from yt_fetch import *

def make_html(userRequest):
	albumInfo = album_metadata()
	
	htmlfoo = albumInfo.search(userRequest, 'allmusic')
	albumInfo.allmusic_parse(htmlfoo)

	htmlfoo = albumInfo.search(userRequest, 'rateyourmusic')
	albumInfo.rym_parse(htmlfoo)

	htmlfoo = albumInfo.search(userRequest, 'discogs')
	albumInfo.discogs_parse(htmlfoo)
	
	try:
		randomSongChosen = ytMetadata().SearchAndPrint(choice(albumInfo.songList) + " " + userRequest)
	except:
		randomSongChosen = ""

	#print albumInfo.allmusicMetadata
	#print
	#print albumInfo.rymMetadata
	#print
	#print albumInfo.discogsMetadata

	linebreak = "<br />"
	hrline = "<hr />"
	
	try:
		allmusicMarkup = "<b>Allmusic" + " - " + albumInfo.allmusicMetadata['rating'].decode('utf-8') + "</b>" + linebreak + "<i>" + '"' + albumInfo.allmusicMetadata['review'][0].decode('utf-8') + '"' + "</i>"
	except (KeyError, IndexError) as e:
		allmusicMarkup = 'Could not fetch content.'

	try:
		rymMarkup = "<b>Rate Your Music" + " - " + albumInfo.rymMetadata['rating'].decode('utf-8') + "</b>" + linebreak + "<i>" + '"' + albumInfo.rymMetadata['review'][0].decode('utf-8') + '"' + linebreak + linebreak + '"' + albumInfo.rymMetadata['review'][1].decode('utf-8') + '"' + "</i>"
	except (KeyError, IndexError) as e:
		rymMarkup = 'Could not fetch content.'

	try:
		discogsMarkup = "<b>Discogs" + " - " + albumInfo.discogsMetadata['rating'].decode('utf-8') + "</b>" + linebreak + "<i>" + '"' + albumInfo.discogsMetadata['review'][0].decode('utf-8') + '"' + "</i>"
	except (KeyError, IndexError) as e:
		discogsMarkup = 'Could not fetch content.'

	youtubeEmbed = '<iframe width="420" height="345" src="http://www.youtube.com/embed/' + randomSongChosen + '"></iframe>'

	html = allmusicMarkup + hrline + rymMarkup + hrline + discogsMarkup + hrline + youtubeEmbed

	return html

if __name__ == "__main__":
	print make_html('village green preservation society the kinks')
