import urllib
import urllib2
import urlparse
import json
import time
import pprint
import xbmcplugin
import xbmcaddon
import xbmcgui
import xbmc
import sys
import hmac
import hashlib
import binascii
import os

xbmc_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')

site='www.viki.com'
applicationID='100366a'
#applicationID='65535a'
secret='1329baa34fcc958a65132726952111712751276c90a89e9c0f9739c010fb5ee23b8e32eff5'
#secret='-$iJ}@p7!G@SyU/je1bEyWg}upLu-6V6-Lg9VD(]siH,r.,m-r|ulZ,U4LC/SeR)'
apiurl='http://api.viki.io/'
apiVersion='v4'
baseurl=apiurl + apiVersion
userAgent='Mozilla/5.0'


def getSignature(url,secret):
    hashSignature = hmac.new(secret, url, hashlib.sha1)    
    return binascii.hexlify(hashSignature.digest())

def build_url(query):
    return xbmc_url + '?' + urllib.urlencode(query)

def viki_api_search(searchString,filterType='container',pageNumber=1,pageSize=25,sortValue='views',sortDirection='dsc'):
    currentEpochTime = int(time.time())

    params = urllib.urlencode({'t': currentEpochTime,'app': applicationID, 'term': searchString, 'with_paging':True, 'per_page': pageSize, 'page': pageNumber, 'sort':sortValue, 'direction':sortDirection, 'type':filterType})
    url = baseurl + '/search.json?' + params
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

def homeScreen():
    url = build_url({'mode' : 'SearchVideos'})
    li = xbmcgui.ListItem('Search videos')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
    
def searchVideo():
    kb = xbmc.Keyboard(heading='Search',hidden=False)
    kb.doModal()
    searchText = ''
    if(kb.isConfirmed()):
        searchText = kb.getText()
    else:
        return
    
    page =1 
    jsondata = viki_api_search(searchString=searchText, pageNumber=page)
    
    while (len(jsondata['response']) > 0):
        for item in jsondata['response']:
            url = build_url({'mode':'videoResultSelected','type':item['type'].encode('utf-8'),'id':item['id'].encode('utf-8')})
                
            if item['images'] is not None and 'poster' in item['images']:
                li = xbmcgui.ListItem(item['titles']['en'].encode('utf-8'),iconImage=item['images']['poster']['url'].encode('utf-8'))
            else:
                li = xbmcgui.ListItem(item['titles']['en'].encode('utf-8'))

            xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=li,isFolder=True)
                
        page = page + 1
        jsondata = viki_api_search(searchString=searchText, pageNumber=page)
   
def displayContainerContent():
    containerType = args['type'][0]
    containerID = args['id'][0]
    
    if containerType == 'series':
        displayEpisodesContent(containerID)
    else:
        displayMoviesContent(containerID)
        
def displayEpisodesContent(seriesID):
    page = 1
    
    jsondata = viki_api_getEpisodes(seriesID=seriesID, pageNumber=page)
    while(len(jsondata['response']) > 0):
        for item in jsondata['response']:
            url = build_url({'mode':'episodeSelected','id':item['id'].encode('utf-8')})
            
            if item['images'] is not None and 'poster' in item['images']:
                li = xbmcgui.ListItem(item['container']['titles']['en'].encode('utf-8') + ' episode ' + str(item['number']),iconImage=item['images']['poster']['url'].encode('utf-8'))
            else:
                li = xbmcgui.ListItem(item['container']['titles']['en'].encode('utf-8') + ' episode ' + str(item['number']))
            
            xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=li,isFolder=True)
        
        page = page + 1
        jsondata = viki_api_getEpisodes(seriesID=seriesID, pageNumber=page)
            
def displayMoviesContent(movieID):
    page = 1
    
    jsondata = viki_api_getMovies(moviesID=movieID, pageNumber=page)
    while(len(jsondata['response']) > 0):
        for item in jsondata['response']:
            url = build_url({'mode':'moviesSelected','id':item['id'].encode('utf-8')})
            
            if item['images'] is not None and 'poster' in item['images']:
                li = xbmcgui.ListItem(item['titles']['en'].encode('utf-8'),iconImage=item['images']['poster']['url'].encode('utf-8'))
            else:
                li = xbmcgui.ListItem(item['titles']['en'].encode('utf-8'))
            
            xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=li,isFolder=True)
        
        page = page + 1
        jsondata = viki_api_getMovies(moviesID=movieID, pageNumber=page)
 
def displayStreams():
    videoID = args['id'][0]
    page = 1
      
    jsondata = viki_api_getVideoStreams(videoID, pageNumber=page)
    if(len(jsondata) > 0):
        for item in jsondata:
            url = build_url({'mode':'streamSelected','id':videoID,'url':jsondata[item]['http']['url']})
            li = xbmcgui.ListItem(str(item))
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=li,isFolder=False)

def playStream():
    videoID = args['id'][0]
    url = args['url'][0]
    language = 'en'
    
    win = xbmcgui.Window(10000)
    player = xbmc.Player()
    player.play(url)
    
    # check if subtitle is available, if it does, download it
    jsondata = viki_api_getVideo(videoID)
    if language in jsondata['response'][0]['subtitle_completions']:
        srtSubtitle = viki_api_getVideoSubtitle(videoID, language)
        location = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources')
        filename = 'subtitle.srt'
        
        with open(os.path.join(location,filename),'wb') as fileDescriptor:
            fileDescriptor.write(srtSubtitle)
            fileDescriptor.close()
            
        player.setSubtitles(os.path.join(location,filename))
        
     
mode = args.get('mode', None)

if mode is None:
    homeScreen()
elif mode[0] == 'SearchVideos':
    searchVideo()
elif mode[0] == 'videoResultSelected':
    displayContainerContent()
elif mode[0] == 'moviesSelected':
    displayStreams()
elif mode[0] == 'episodeSelected':
    displayStreams()
elif mode[0] == 'streamSelected':
    playStream()
    
xbmcplugin.endOfDirectory(addon_handle)

print addon_handle
#if __name__ == '__main__':
    #searchString = 'jang bo ri'
    #containerID = '22824c'

    #videoData = viki_api_search(searchString=searchString,filterType='container',pageNumber=1,pageSize=5)
    
    
    #pprint.pprint(videoData)

    #data =  viki_api_getEpisodes(containerID,7)
    #pprint.pprint(data)
