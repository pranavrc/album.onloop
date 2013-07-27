#!/usr/bin/env python

import lxml.html as lh
from lxml.html.clean import Cleaner
from lxml.etree import tostring

class SpotifyEmbed:
    def __init__(self, search_term):
        self.search_url = "http://ws.spotify.com/search/1/album?q=" + search_term

    def get_album_uri(self):
        document = lh.parse(self.search_url)
        album_id = document.xpath('.//album/@href')[0]
        return album_id

    def generate_embed_code(self, album_id):
        embed_code = '<iframe src="https://embed.spotify.com/?uri=%s" ' % album_id + \
                'width="300" height="380" frameborder="0" allowtransparency="true"></iframe>'
        return embed_code

if __name__ == "__main__":
    a = SpotifyEmbed(raw_input())
    print a.generate_embed_code(a.get_album_uri())
