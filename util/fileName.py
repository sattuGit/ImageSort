
def getExt(fname):
    if fname.find('.') :
        return fname[fname.find('.'):len(fname)].upper()
    return ""

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
    print(getExt('fileScreenshot_2019-11-26-16-36-53-512_com.jeevansathi.android.jpg'))


if __name__ == "__main__":
    main()

