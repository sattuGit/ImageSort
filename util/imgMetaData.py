#https://pillow.readthedocs.io/en/stable/
#https://pypi.org/project/PIL/
import os
import datetime
import logging
from PIL import Image

logger = logging.getLogger()

class imgObj:
    _invalid = False
    _isExifFound = False
    _width  =0
    _hight  =0
    __metaData = None
    _metaCreateDate=""
    maker = ""
    model =""
    selfi =False
    gioTag = ""
    def __init__(self,url):
        #print('INSIDDE INIT '+url)
        if os.path.isfile(url):
            try:
                #print('inside class constructor url'+url)
                fp = Image.open(url,'r')
                self.__metaData = fp._getexif()
                if self.__metaData: self._isExifFound = True
                self._sysModifyDate = datetime.datetime.fromtimestamp(os.path.getmtime(url)).strftime('%Y%m%d')
            except IOError:
                self._invalid=True
                #print('Excepion Occurs '+str(IOError))
                logger.critical('FILE IO ERROR '+str(IOError))
            except:
                self._invalid=True
                #print('Unknown exception')
                logger.critical('Unknown exception')
            finally:
                #print('final')
                if not self._invalid:
                    fp.close()
                # process Data
                if self.__metaData:
                    self._width = self.__metaData.get(256)
                    self._hight = self.__metaData.get(257)
                    if self.__metaData.get(306):
                        tmpTime =datetime.datetime.strptime(self.__metaData.get(306),'%Y:%m:%d %H:%M:%S')
                        self._metaCreateDate = tmpTime.strftime('%Y%m%d')
                    self.gioTag = self.__metaData.get(34853)
                    if self.gioTag:
                        tmp = str(self.gioTag.get(29))
                        #print(tmp)
                        self._gioCreateDate = tmp.replace(':','')
                        #print(tmp.replace(":",""))
                    self.maker  = self.__metaData.get(271)
                    if self.maker:  self.maker = self.maker.strip()
                    self.model  = self.__metaData.get(272)
                    if self.model:  self.model = self.model.strip()
                    self.selfi  =   self.__metaData.get(39321)

                #print(self.model)
        else:
            #print('else part')
            self._invalid = True

    def __del__(self):
        i=0
    def isValid(self)   : return not self._invalid
    def isMetaFound(self)   : return self._isExifFound
    def isGio(self)     : return self.gioTag
    def getMaker(self)  : return str(self.maker)
    def getModel(self)  : return str(self.model)
    def getGPS(self): return self.gioTag
    def getMetaCreateDate(self): return self._metaCreateDate
    def getGioCreateDate(self): return self._gioCreateDate
    def getSysModifyDate(self): return self._sysModifyDate

def main():
    x =imgObj(os.getcwd()+'/../sample/test.jpg')
    print(x.isValid())
    print(x.isMetaFound())
    #print(x.isGio())
    #print(x.getGPS())
    print(x.getSysModifyDate())
    print(x.getGioCreateDate())
    print(x.getMetaCreateDate())
if __name__ == "__main__":
    main()
