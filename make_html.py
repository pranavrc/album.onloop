#!/usr/bin/env python
# -*- coding: utf-8 -*-

from album_metadata import *
from random import choice
from yt_fetch import *
import string
from spotify_playlist import SpotifyEmbed

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
    elif contentSitename == 'rollingstone'.lower():
        metadata = albumInfo.rsMetadata
    elif contentSitename == 'metacritic'.lower():
        metadata = albumInfo.metacriticMetadata

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
        html = markup + "<br/><i>Album not found.</i>"
    else:
        html = markup

    if contentSitename == 'allmusic'.lower():
        try:
            info = make_tracklist(albumInfo.songList, albumInfo.albumart, albumInfo.genre, albumInfo.styles).decode('utf-8')
        except:
            info = ""

        if info:
            html = "<div class=\"info\">" + info + "</div>" + hrline + html
        else:
            html = info + html

    return html

def make_tracklist(songList, imageFile, genre, styles):
    tracklisting = "<b><i>Track Listing:</b></i><br/>"

    if genre:
        if styles:
            albumGenre = "<b><i>Genre:</b></i> " + "<i>" + genre + " (" + styles + ")</i><br /><br />"
        else:
            albumGenre = "<b><i>Genre:</b></i> " + "<i>" + genre + "</i><br /><br />"
    else:
        albumGenre = ""

    if songList:
        for eachSong in songList:
            if eachSong != songList[-1]:
                tracklisting = tracklisting + "<i>" + eachSong + "</i>" + " - "
            else:
                tracklisting = tracklisting + "<i>" + eachSong + "</i>"
    else:
        tracklisting = ""

    if imageFile:
        albumpic = "<img class=\"albumart\" width=\"200\" height=\"200\" src=\"" + imageFile + \
                "\" alt=\"Album Art\" /><br /><br />"
    else:
        albumpic = ""

    html = str(albumpic) + str(albumGenre) + str(tracklisting)
    return html

def make_html(userRequest, urlCount):
    albumInfo = album_metadata()

    loadergif = "<img class=\"loader\" src=\"{{ url_for('static', filename='loader.gif') }}\" alt=\"Publishing...\" />"
    linebreak = "<br />"
    hrline = "<hr />"
    segmented = False

    if urlCount == 1:
        html = "<p>" + markup(userRequest, albumInfo, 'allmusic', albumInfo.allmusic_parse, 'utf-8') + "</p>"

    elif urlCount == 2:
        htmlfoo = albumInfo.search(userRequest, 'allmusic')
        albumInfo.allmusic_parse(htmlfoo, getAlbumArt = False, getGenre = False, getStyles = False)

        if not albumInfo.songList:
            try:
                randomSongChosen = ytMetadata().SearchAndPrint(userRequest.encode('utf-8'))
            except:
                randomSongChosen = ""
        else:
            for i in range(0, 3):
                try:
                    randomSongChosen = ytMetadata().SearchAndPrint(choice(albumInfo.songList) + " " + userRequest.encode('utf-8'))
                    break
                except:
                    randomSongChosen = ""
                    continue

        if not randomSongChosen:
            return "<i>Youtube Video not found.</i>"

        youtubeEmbed = '<iframe title="Youtube video player" width="50%" height="380" ' + \
                'src="http://www.youtube.com/embed/' + randomSongChosen + \
                '" frameborder="0" allowfullscreen></iframe>'

        html = youtubeEmbed
        segmented = True

    elif urlCount == 3:
        album = SpotifyEmbed(userRequest)
        segmented = True
        try:
            album_uri = album.get_album_uri()
            html = album.generate_embed_code(album_uri) + hrline
        except:
            html = hrline + "<i>Album not found on Spotify.</i>" + hrline

    elif urlCount == 4:
        html = "<p>" + markup(userRequest, albumInfo, 'rateyourmusic', albumInfo.rym_parse, 'utf-8') + "</p>"

    elif urlCount == 5:
        html = "<p>" + markup(userRequest, albumInfo, 'discogs', albumInfo.discogs_parse, 'utf-8') + "</p>"

    elif urlCount == 6:
        html = "<p>" + markup(userRequest, albumInfo, 'itunes', albumInfo.itunes_parse, 'utf-8') + "</p>"

    elif urlCount == 7:
        html = "<p>" + markup(userRequest, albumInfo, 'pitchfork', albumInfo.pitchfork_parse, 'utf-8') + "</p>"

    elif urlCount == 8:
        html = "<p>" + markup(userRequest, albumInfo, 'sputnikmusic', albumInfo.sputnikmusic_parse, 'utf-8') + "</p>"

    elif urlCount == 9:
        html = "<p>" + markup(userRequest, albumInfo, 'rollingstone', albumInfo.rs_parse, 'utf-8') + "</p>"

    elif urlCount == 10:
        html = "<p>" + markup(userRequest, albumInfo, 'metacritic', albumInfo.metacritic_parse, 'utf-8') + "</p>"
        segmented = True

    #print albumInfo.allmusicMetadata
    #print
    #print albumInfo.rymMetadata
    #print
    #print albumInfo.discogsMetadata

    #html = allmusicMarkup + hrline + rymMarkup + hrline + discogsMarkup + hrline + youtubeEmbed

    if segmented:
        return html
    else:
        return html + hrline

if __name__ == "__main__":
    make_html('live', 4)
