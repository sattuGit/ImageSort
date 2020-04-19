import logging
logger = logging.getLogger()
def getExt(fname,last=True):
    if fname.find('.') >-1:
        if last :   return fname[fname.rindex('.'):len(fname)]
        else:       return fname[fname.find('.'):len(fname)]
    return ""

def isKeyWordFound(source,key,case=False):
    if case:
        if source.find(key)>-1: return True
        else:
            return False
    else:
        #logger.debug(source.upper()+' '+key.upper())
        if source.upper().find(key.upper())>-1:return True
        else:
            return False

def isdateExist(fname):
    tmp=""
    ind=-1
    timeStamp=""
    if fname.find('.'):
        tmp=fname[0:fname.find('.')]
    ind = tmp.find('20')
    try:
        if int(tmp[ind:ind+4]) > 1999:
            return tmp[ind:ind+4]
    except:
        return ''

    ind = tmp.find('19')
    try:
        if int(tmp[ind:ind+4]) > 1990:
            return tmp[ind:ind+4]
    except:
        return ''
    return ''

    #if fname.find('19') or fname.find('20'):

def main():
    print('::'+getExt('fileScreenshot_2019-11-26-16-36-53-512_com.jeevansathi.android.jpg',False)+'::')
    print('::'+getExt('fileScreenshot_2019-11-26-16-36-53-512_com.jeevansathi.android.jpg',True)+'::')
    print('::'+getExt('fileScreenshot_2019-11-26-16-36-53-512_com',True)+'::')
    print('::'+getExt('fileScreenshot_2019-11-26-16-36-53-512_com')+'::')


if __name__ == "__main__":
    main()

