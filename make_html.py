from album_metadata import *

def make_html(userRequest):
	albumInfo = album_metadata()
	
	htmlfoo = albumInfo.search(userRequest, 'allmusic')
	albumInfo.allmusic_parse(htmlfoo)

	htmlfoo = albumInfo.search(userRequest, 'rateyourmusic')
	albumInfo.rym_parse(htmlfoo)

	htmlfoo = albumInfo.search(userRequest, 'discogs')
	albumInfo.discogs_parse(htmlfoo)

	#print albumInfo.allmusicMetadata
	#print
	#print albumInfo.rymMetadata
	#print
	#print albumInfo.discogsMetadata

	linebreak = "<hr />"
	try:
		html = "<h3>Allmusic</h3>" + "<b>" + albumInfo.allmusicMetadata['rating'].decode('utf-8') + "</b>" + "<br />" + "<i>" + albumInfo.allmusicMetadata['review'][0].decode('utf-8') + "</i>"
	except KeyError:
		return 'Could not fetch content.'
	except UnicodeDecodeError:
		make_html(userRequest)

	return html

if __name__ == "__main__":
	print make_html('abbey road the beatles')
