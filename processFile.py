import os
import logging
from symbol import nonlocal_stmt
from urllib.request import FancyURLopener

import util.fileName        as fName
#import util.imgMetaData     as imgObj
from util.imgMetaData import imgObj
import util.fileDirOSOps    as fOps
import util.fileUnique      as booti
logger = logging.getLogger()
pelter = {}
filterBase = 'ImageSort_move'
duplicateRoot = 'DUPLICATE'
copyDir = '/home/satendra/Desktop/DUMP_YARD/'
metaDir = "FILE_WITH_INFO"
nonMetaDir = "FILE_WITH_NO_INFO"
def processFullTree(rootDir,opList,op="NONE",pattern=[],breakStructure=True,duplicatFilter=True):
    logger.info('ROOT IS           ['+rootDir+']')
    logger.info('File Type         ['+str(opList)+']')
    logger.info('Operation         ['+op+']')
    logger.info('Pattern           ['+str(pattern)+']')
    logger.info('Move to parent    ['+str(breakStructure)+']')
    #quit()
    logger.info('--------------------------------------------------')
    logger.info('            PROCESSING DIRs                       ')
    logger.info('            ' + rootDir)
    logger.info('Current valid file type are :' + str(opList))
    logger.info('--------------------------------------------------')

    moveDirBase=os.path.join(copyDir,filterBase)
    if not fOps.createDir(copyDir,filterBase):
        logger.critical('Directory ['+moveDirBase+'] creation failed')

    metaFileDir=os.path.join(moveDirBase,'META_FILE')
    if not fOps.createDir(moveDirBase,'META_FILE'):
        logger.critical('Directory ['+metaFileDir+'] creation failed')
        return False

    nonMetaFileDir=os.path.join(moveDirBase,'NON_META_FILE')
    if not fOps.createDir(moveDirBase,'NON_META_FILE'):
        logger.critical('Directory ['+nonMetaFileDir+'] creation failed')
        return False

    duplicateBase = os.path.join(moveDirBase,duplicateRoot)
    if fOps.createDir(rootDir,filterBase): # ./filterBase
        for sub in pattern:
            if not fOps.createDir(moveDirBase,sub): #./filterBase/pattern
                logger.critical('Sub directory '+sub+' creation failed')
                return False
            else:
                tmpPath = os.path.join(moveDirBase,sub)
                if not fOps.createDir(moveDirBase,metaDir):
                    logger.critical('Directory ['+metaDir+'] creation failed')
                    return False

                if not fOps.createDir(moveDirBase,nonMetaDir):
                    logger.critical('Directory ['+nonMetaDir+'] creation failed')
                    return False


        if not fOps.createDir(moveDirBase,duplicateRoot): #./filterBase/duplicateRoot
            logger.critical('Pattern Directory creation Failed ')
            return False
    else:
        logger.critical('Directory creation Failed ')
        return False

    for subdir, dirs, files in os.walk(rootDir):
        logger.info('--------------------------------------------------')
        logger.info('Current DIR ' + subdir)
        validCnt    = 0
        moveCnt     = 0

        # if subdir == moveDirBase :
        #     logger.debug('IGNORE WORKING DIR '+subdir+'#'+moveDirBase)
        #     continue


        for file in files:
            fileAbsPath = os.path.join(subdir,file)
            print('Processing...['+fileAbsPath+']')
            #logger.info('=====START')
            if fName.getExt(file) in opList :
                validCnt += 1

                # filter duplicate files
                if duplicatFilter:
                    if duplicateFilter(fileAbsPath,duplicateBase):
                        continue

                if op == "MOVE_FILE":
                    logger.debug('INSIDE MOVE BLOCK')
                    for sub in pattern:
                        if fName.isKeyWordFound(file,sub):
                            pickUp  =   fileAbsPath
                            drop    =   os.path.join(os.path.join(moveDirBase,sub) , file)
                            logger.debug('ARG ['+pickUp+']['+drop+']')
                            if not fOps.moveFile(pickUp,drop):
                                logger.critical('File Movement failed ')
                                break
                            else:
                                logger.debug('ACTUAL MOVE FILE ['+pickUp+'] TO ['+sub+']'+drop)
                                moveCnt+=1
                                break

                    print('***********'+fileAbsPath)
                    if isMeta(fileAbsPath):
                        if not fOps.moveFile(fileAbsPath,os.path.join(metaFileDir,file)):
                            logger.critical('File Movement failed ')
                            break
                    else:
                        if not fOps.moveFile(fileAbsPath,os.path.join(nonMetaFileDir,file)):
                            logger.critical('File Movement failed ')
                            break

                else:
                    logger.warning('Unknown Operation')
            else:
                logger.debug('Ignore file' + file)
        logger.info('Total File Avialble [' + str(len(files)) + '] Processed [' + str(validCnt) + '] Ignore [' + str(
            len(files) - validCnt) + ']')
    return True

def isMeta(url):
    try:
        #print(url)
        obj = imgObj(url)
        #print(obj)
        if obj :
            return obj.isMetaFound()
    except :
        print('File not loadable ')
        logger.debug('File '+url+' is not loadable ')
    return False

def duplicateFilter(url,base):
    fileName =os.path.basename(url)
    pong = checkDuplicate(url)
    logger.debug('DUPLICATE TEST OF ['+url+'] resut ['+pong+']')
    if len(pong)>0:
        for x in range(100):
            subDir= os.path.join(base,str(x))
            target = os.path.join(subDir,fileName)
            if os.path.isdir(subDir):   #DIR INDEX found
                if not os.path.exists(target):
                    # no conflict
                    #logger.debug(url+' '+target)
                    fOps.moveFile(url,target)
                    logger.info('MOVE_TO ('+str(x)+') '+url+' TO '+target)
                    return True
                else:
                    pass
                    #logger.debug('DUPLICATE INDEX '+str(x)+' has conflict for '+url)
            else:   #DIR INDEX not found
                fOps.createDir(base,str(x))     # create index dir
                fOps.moveFile(url,target)
                logger.info('MOVE_BY_CREATE_NEW ('+str(x)+') '+url+' TO '+target)
                return True
    return False

def checkDuplicate(url):
    turn    =  booti.gethas(url)
    found  = pelter.get(turn)
    if found:
        logger.info('Duplicate Found ['+url+'=AND='+found+']')
        return found
    else:
        pelter[turn]=url
        return ""

def main():
    print(isMeta('/home/satendra/Desktop/git/ImageSort/sample/IMG-20190428-WA0002.jpg'))

if __name__ == "__main__":
    main()
