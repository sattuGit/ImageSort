import sys
import logging

import processFile as fProcess

logging.basicConfig(filename="ImageSorting.log", format='[%(levelname)s] %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

def main():
    moveInParent    =   True    #By Default move file opertaion move all file inside root
    OPeration       =   "NONE"
    baseDir = {
                'rootDir' : '/home/satendra/Desktop/workYard/',
                'copyDir' : '/home/satendra/Desktop/dumpYard/'
               }
    opList = []
    patternList=[]

    if len(sys.argv) == 2 and sys.argv[1] == "-help":
        '''
        FOR HELP ImageSort.py -help
        '''
        print('ImageSort.py {fileType} <Operation> <pattern> <moveToParent=True/False>')
        print('     FileType  "filetype=.example1,.example2,..."  ALL is Default ** NO SPACE IN LIST ')
        print('     Operation "-mv/-cp/-RmEmpDir"')
        print('     pattern   "<freeStyleString should contain by file name CAN BE MULTIPLE separated by comma >"')
        print(' Example ::  python ImageSort.py fileType=.jpg,.jpeg,.png -mv pattern=whatsapp,shaadi,jeevan,facebook,PicsArt,FB_,Screenshot')
        print('             process only .jpg,.jpeg,.png Files only, rest file type will be ignored ')
        print('             check pattern with file name from left to right , if match move to pattern dir "-mv for move"  ')
        print('             breakStructure  is True by default .. i.e will create new structure for file movement ')
        print('             duplicateRemove is True by default .. i.e will seperate all duplicate files  ')
        return True
    baseArg = int(1)
    if len(sys.argv) > baseArg and (sys.argv[1])[0:9]=='fileType=':
        ftypecsv=sys.argv[1][9:len(sys.argv[1])]
        opList = ftypecsv.replace(' ','').split(',')
        baseArg+=1

    if len(sys.argv) > baseArg and  sys.argv[baseArg].upper()=="-MV":
        OPeration = "MOVE_FILE"
        baseArg+=1
    elif len(sys.argv) > baseArg and sys.argv[baseArg].upper()=="-CP":
        OPeration = "COPY_FILE"
        baseArg+=1
    elif len(sys.argv) > baseArg:
        logger.warning('Invalid/Unknown Arguments .. call -help ')
        return False

    if len(sys.argv) > baseArg and OPeration!="NONE" and (OPeration in ['MOVE_FILE','COPY_FILE']):
        if sys.argv[baseArg][0:8]=='pattern=':
            patternList=sys.argv[baseArg][8:len(sys.argv[baseArg])].split(',')
            baseArg+=1

    if len(sys.argv) > baseArg and sys.argv[baseArg].upper()=="MOVETOPARENT=TRUE":
        moveInParent = True
    elif len(sys.argv) > baseArg and sys.argv[baseArg].upper()=="MOVETOPARENT=FALSE":
        moveInParent = False
    elif len(sys.argv) > baseArg:
        logger.warning('Invalid/Unknown Arguments .. call -help ')
        return False

    if not fProcess.processFullTree(baseDir,opList,OPeration,patternList,moveInParent):
        print('ERRORR................')

if __name__ == "__main__":
    main()
