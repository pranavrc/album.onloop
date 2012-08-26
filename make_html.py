from album_metadata import *

def make_html(userRequest):
	albumInfo = album_metadata()
	
	htmlfoo = albumInfo.imFeelingLucky(userRequest, 'allmusic')
	albumInfo.allmusic_parse(htmlfoo)

	htmlfoo = albumInfo.imFeelingLucky(userRequest, 'rateyourmusic')
	albumInfo.rym_parse(htmlfoo)

	htmlfoo = albumInfo.imFeelingLucky(userRequest, 'discogs')
	albumInfo.discogs_parse(htmlfoo)

	#print albumInfo.allmusicMetadata
	#print
	#print albumInfo.rymMetadata
	#print
	#print albumInfo.discogsMetadata

	linebreak = "<hr />"
	html = "<h3>Allmusic</h3>" + "<b>" + albumInfo.allmusicMetadata['rating'] + "</b>" + "<br />" + "<i>" + albumInfo.allmusicMetadata['review'][0] + "</i>"

	return html

if __name__ == "__main__":
	print make_html('abbey road the beatles')
