import urllib,urllib2,re,os
import xbmcplugin,xbmcgui,xbmcaddon
try:
    import json
except:
    import simplejson as json

__settings__ = xbmcaddon.Addon(id='plugin.video.flw.outdoors')
__language__ = __settings__.getLocalizedString
__home__ = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( __home__, 'icon.png' ) )


def CATEGORIES():
        addDir(__language__(30000),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=flwlatestvideos&method=getVideosInChannel',1,icon)
        addDir(__language__(30001),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=flwtv&method=getVideosInChannel',1,icon)
        addDir(__language__(30002),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=tipsfromthepros&method=getVideosInChannel',1,icon)
        addDir(__language__(30003),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=flwtour&method=getVideosInChannel',1,icon)
        addDir(__language__(30004),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=fantasyonflw&method=getVideosInChannel',1,icon)
        addDir(__language__(30005),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=collegeonflw&method=getVideosInChannel',1,icon)
        addDir(__language__(30006),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=flwpodcast&method=getVideosInChannel',1,icon)
        addDir(__language__(30007),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=ReelCast&method=getVideosInChannel',1,icon)
        addDir(__language__(30008),'http://www.flwoutdoors.com/flwMedia/ajax.cfm?callsign=flwmagpublic&method=getVideosInChannel',1,icon)


def INDEX(url):
        req = urllib2.Request(url)
        req.addheaders = [('Referer', 'http://www.flwoutdoors.com/flwondemand.cfm?cs=flwtour'),
                        ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
        response = urllib2.urlopen(req)
        link=response.read()
        data=json.loads(link)
        videos = data["CHANNEL"]["AFILE"]
        for video in videos:
            title = video["TITLE"]
            if not video["PATH"]=='':
                path = video["PATH"]
            else:
                path = 'http://www.jidocs.com'+str(video["STREAMING_PATH"])[4:]
            thumbnail = video["THUMBNAIL"]
            description = video["DESCRIPTION"]
            addLink (title,path,description,thumbnail)
        

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
                                
        return param


def addLink(name,url,description,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
    print ""
    CATEGORIES()
       
elif mode==1:
    print ""+url
    INDEX(url)

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
