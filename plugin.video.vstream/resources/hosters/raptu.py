#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.config import cConfig 
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 
import re,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Raptu'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'raptu'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return False

    def getPattern(self):
        return ''
    
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        #Ne marche pas systematiquement
        #self.__sUrl = self.__sUrl.replace('www.rapidvideo.com','www.raptu.com')
        
    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        sUrl = self.__sUrl
        
        oParser = cParser()
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        #pour lien rapidvideo modif en raptu
        #sPattern = '<input type="hidden" value="(\d+)" name="block">'
        #aResult = oParser.parse(sHtmlContent,sPattern)
        #if (aResult[0] == True):
        #    cConfig().log('Modif rapidvideo > raptu')
        #    oRequest = cRequestHandler(sUrl)
        #    oRequest.setRequestType(1)
        #    oRequest.addParametersLine('confirm.x=74&confirm.y=35&block=1')
        #    sHtmlContent = oRequest.request()

        sPattern = '{"file":"([^"]+)","label":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))   
            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]

        if (api_call):
            return True, api_call
            
        return False, False
