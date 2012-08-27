import gdata.youtube
import gdata.youtube.service
import urlparse

class ytMetadata:
	def PrintVideoFeed(self, feed):
		for entry in feed.entry:
			return self.video_urlparse(self.PrintEntryDetails(entry))

	def PrintEntryDetails(self, entry):
		#print 'Video title: %s' % entry.media.title.text
		#print 'Video published on: %s ' % entry.published.text
		#print 'Video description: %s' % entry.media.description.text
		#print 'Video category: %s' % entry.media.category[0].text
		#print 'Video tags: %s' % entry.media.keywords.text
		#print 'Video watch page: %s' % entry.media.player.url
		return entry.media.player.url
		#print 'Video flash player URL: %s' % entry.GetSwfUrl()
		#print 'Video duration: %s' % entry.media.duration.seconds

		# non entry.media attributes
		#print 'Video geo location: %s' % entry.geo.location()
		#print 'Video view count: %s' % entry.statistics.view_count
		#print 'Video rating: %s' % entry.rating.average

		# show alternate formats
		#for alternate_format in entry.media.content:
		      #if 'isDefault' not in alternate_format.extension_attributes:
			    #print 'Alternate format: %s | url: %s ' % (alternate_format.type, alternate_format.url)

		# show thumbnails
		#for thumbnail in entry.media.thumbnail:
		  #print 'Thumbnail url: %s' % thumbnail.url

	def SearchAndPrint(self, search_terms):
		yt_service = gdata.youtube.service.YouTubeService()
		query = gdata.youtube.service.YouTubeVideoQuery()
		query.vq = search_terms
		query.orderby = 'relevance'
		query.racy = 'include'
		query.max_results = 1
		feed = yt_service.YouTubeQuery(query)
		return self.PrintVideoFeed(feed)

	def video_urlparse(self, video_url):
		url = urlparse.urlparse(video_url)
		params = urlparse.parse_qs(url.query)
		return params['v'][0]



if __name__ == "__main__":
	yt = ytMetadata()
	a = yt.SearchAndPrint("rudie can't fail the clash")
	print a
