import urllib
import urllib2
import urlparse
import json
import time
import pprint
import sys
import hmac
import hashlib
import binascii
import os

site='www.viki.com'
applicationID='100366a'
#applicationID='65535a'
secret='1329baa34fcc958a65132726952111712751276c90a89e9c0f9739c010fb5ee23b8e32eff5'
#secret='-$iJ}@p7!G@SyU/je1bEyWg}upLu-6V6-Lg9VD(]siH,r.,m-r|ulZ,U4LC/SeR)'
apiurl='http://api.viki.io/'
apiVersion='v4'
baseurl=apiurl + apiVersion
userAgent='Mozilla/5.0'
proxyUrl='https://losangeles-s02-i01.cg-dialup.net/go/browse.php?u=*url*&b=7'


def getSignature(url,secret):
    hashSignature = hmac.new(secret, url, hashlib.sha1)    
    return binascii.hexlify(hashSignature.digest())

def build_url(query):
    return xbmc_url + '?' + urllib.urlencode(query)

def viki_api_search(searchString,filterType='container',pageNumber=1,pageSize=25,sortValue='views',sortDirection='dsc'):
    currentEpochTime = int(time.time())

    params = urllib.urlencode({'t': currentEpochTime,'app': applicationID, 'term': searchString, 'with_paging':True, 'per_page': pageSize, 'page': pageNumber, 'sort':sortValue, 'direction':sortDirection, 'type':filterType})
    url = proxyUrl.replace('*url*',baseurl + '/search.json?' + params)
    #url = baseurl + '/search.json?' + params
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', userAgent)

    print url
    try:
        data = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        print 'HTTP error: %d' % e.code
    except urllib2.URLError, e:
        print 'Network error: %s' % e.reason.args[1]

    jsonData = json.loads(data)

    videos = jsonData
    return videos    

def viki_api_getEpisodes(seriesID,pageNumber=1,pageSize=10,sortValue='number',sortDirection='asc'):
    currentEpochTime = int(time.time())

    params = urllib.urlencode({'t': currentEpochTime,'app': applicationID, 'with_paging':True, 'per_page': pageSize, 'page': pageNumber, 'sort':sortValue, 'direction':sortDirection})
    url = baseurl + '/series/' + seriesID + '/episodes.json?' + params   
    
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', userAgent)

    print url
    try:
        data = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        print 'HTTP error: %d' % e.code
    except urllib2.URLError, e:
        print 'Network error: %s' % e.reason.args[1]

    return json.loads(data)

def viki_api_getMovies(moviesID,pageNumber=1,pageSize=10,sortValue='number',sortDirection='asc'):
    currentEpochTime = int(time.time())

    params = urllib.urlencode({'t': currentEpochTime,'app': applicationID, 'with_paging':True, 'per_page': pageSize, 'page': pageNumber, 'sort':sortValue, 'direction':sortDirection})
    url = baseurl + '/films/' + moviesID + '/movies.json?' + params   
    
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', userAgent)

    print url
    try:
        data = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        print 'HTTP error: %d' % e.code
    except urllib2.URLError, e:
        print 'Network error: %s' % e.reason.args[1]

    return json.loads(data)

def viki_api_getVideoStreams(videoID,pageNumber=1,pageSize=10,sortValue='number',sortDirection='asc'):
    currentEpochTime = int(time.time())
    
    params = urllib.urlencode({'t': currentEpochTime,'app': applicationID, 'with_paging':True, 'per_page': pageSize, 'page': pageNumber, 'sort':sortValue, 'direction':sortDirection,'site':site})
    
    signatureURL = '/' + apiVersion + '/videos/' + videoID + '/streams.json?' + params 
    signature = getSignature(signatureURL, secret)
    signedParams = urllib.urlencode({'t': currentEpochTime,'app': applicationID, 'with_paging':True, 'per_page': pageSize, 'page': pageNumber, 'sort':sortValue, 'direction':sortDirection,'site':site,'sig':signature})
    
    url = baseurl + '/videos/' + videoID + '/streams.json?' + signedParams   
    
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', userAgent)

    print url
    try:
        data = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        print 'HTTP error: %d' % e.code
    except urllib2.URLError, e:
        print 'Network error: %s' % e.reason.args[1]

    return json.loads(data)

def viki_api_getVideoSubtitle(videoID,language):
    currentEpochTime = int(time.time())

    params = urllib.urlencode({'t': currentEpochTime,'app': applicationID, 'site':site})

    signatureURL = '/' + apiVersion + '/videos/' + videoID + '/subtitles/' + language + '.srt?' + params
    signature = getSignature(signatureURL, secret)
    signedParams = urllib.urlencode({'t': currentEpochTime,'app': applicationID,'site':site,'sig':signature})

    url = baseurl + '/videos/' + videoID + '/subtitles/' + language + '.srt?' + signedParams

    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', userAgent)

    print url
    try:
        data = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        print 'HTTP error: %d' % e.code
    except urllib2.URLError, e:
        print 'Network error: %s' % e.reason.args[1]

    return data

def viki_api_getVideo(videoID):
    currentEpochTime = int(time.time())

    params = urllib.urlencode({'t': currentEpochTime,'app': applicationID,'ids':videoID})
    url = baseurl + '/videos.json?' + params   
    
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', userAgent)

    print url
    try:
        data = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        print 'HTTP error: %d' % e.code
    except urllib2.URLError, e:
        print 'Network error: %s' % e.reason.args[1]

    return json.loads(data)

def viki_api_getLanguages():
    currentEpochTime = int(time.time())

    params = urllib.urlencode({'t': currentEpochTime,'app': applicationID})
    url = baseurl + '/languages.json?' + params   
    
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', userAgent)

    print url
    try:
        data = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        print 'HTTP error: %d' % e.code
    except urllib2.URLError, e:
        print 'Network error: %s' % e.reason.args[1]

    return json.loads(data)

if __name__ == '__main__':
    searchString = 'decendants'
    containerID = '22824c'

    videoData = viki_api_search(searchString=searchString,filterType='container',pageNumber=1,pageSize=5)
    
    
    pprint.pprint(videoData)

    #data =  viki_api_getEpisodes(containerID,7)
    #pprint.pprint(data)
