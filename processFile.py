import os
import logging
#
# from os.path import basename
# from symbol import nonlocal_stmt
# from urllib.request import FancyURLopener

import util.fileName        as fName
from util.imgMetaData import imgObj
import util.fileDirOSOps    as fOps
import util.fileUnique      as booti
logger = logging.getLogger()

# map of unique file hash and path , hash as key
pelter = {}


filterBase      =   "ImageSort_move"
duplicateRoot   =   "DUPLICATE"
metaDirName         = "FILE_WITH_INFO"
nonMetaDirName      = "FILE_WITH_NO_INFO"


def createMoveFileInfra(baseDir, pattern):
    logger.debug('Inside Dir Creation RootDir['+baseDir.get('rootDir')+'] copy DIR ['+baseDir.get('copyDir')+'] pattern['+str(pattern)+']')

    baseDir['moveDirBase']      =   os.path.join(baseDir.get('copyDir'),filterBase)
    if not fOps.createDir(baseDir.get('copyDir'),filterBase):  #DUMP/ImageSort_move
        logger.critical('Directory ['+baseDir.get('moveDirBase')+'] creation failed')
        return False
    else:
        logger.debug('Created moveDirBase '+baseDir.get('moveDirBase'))

    baseDir['metaFileDir']  =   os.path.join(baseDir.get('moveDirBase'), metaDirName)
    if not fOps.createDir(baseDir.get('moveDirBase'),metaDirName): #DUMP/ImageSort_move/META_FILE
        logger.critical('Directory ['+baseDir.get('metaFileDir')+'] creation failed')
        return False
    else:
        logger.debug('Created metaFileDir '+baseDir.get('metaFileDir'))

    baseDir['nonMetaFileDir']  =   os.path.join(baseDir.get('moveDirBase'),nonMetaDirName)
    if not fOps.createDir(baseDir.get('moveDirBase'),nonMetaDirName): #DUMP/ImageSort_move/NON_META_FILE
        logger.critical('Directory ['+baseDir.get('nonMetaFileDir')+'] creation failed')
        return False
    else:
        logger.debug('Created nonMetaFileDir '+baseDir.get('nonMetaFileDir'))


    baseDir['duplicateBase']  = os.path.join(baseDir.get('moveDirBase'),duplicateRoot)
    #print(duplicateBase)
    if not fOps.createDir(baseDir.get('moveDirBase'),duplicateRoot): # ./filterBase
        # if not fOps.createDir(moveDirBase,duplicateRoot): #./filterBase/duplicateRoot
        logger.critical('Pattern Directory creation Failed ')
        return False
    else:
        logger.debug('Created duplicateBase'+baseDir.get('duplicateBase'))
    #print(duplicateBase)
    for sub in pattern:
            if not fOps.createDir(baseDir.get('moveDirBase'),sub): #./filterBase/pattern
                logger.critical('Sub directory '+sub+' creation failed')
                return False
            else:
                logger.debug('Created pattern '+baseDir.get('moveDirBase')+'>>'+sub)
    return True


def processFullTree(baseDir,opList,op="NONE",pattern=[],breakStructure=True,duplicatFilter=True):
    logger.info('**************************************************')
    logger.info('ROOT IS           ['+str(baseDir.get("rootDir"))+']')
    logger.info('File Type         ['+str(opList)+']')
    logger.info('Operation         ['+op+']')
    logger.info('Pattern           ['+str(pattern)+']')
    logger.info('Move to parent    ['+str(breakStructure)+']')
    logger.info('file type are     ['+ str(opList)+']')
    logger.info('**************************************************')

    # Create mandatory directory structure
    if not createMoveFileInfra(baseDir, pattern):
        logger.debug('Directiry structure creation failed ')
        return False
    #
    # logger.debug('duplicateBase ####'+baseDir.get('duplicateBase'))
    # logger.debug('moveDirBase ####'+baseDir.get('moveDirBase'))
    # logger.debug('metaFileDir ####'+baseDir.get('metaFileDir'))
    # logger.debug('nonMetaFileDir ####'+baseDir.get('nonMetaFileDir'))
    #quit()

    #OVER ALL Statistics
    cntTreeTotalFile        =   0   #ALL files in Tree
    cntTreeProcessFile      =   0   #file we processed
    cntTreeIgnoreFile       =   0   #FIle we ignore
    cntTreeDuplicateFile    =   0   #Files marked as duplicate (
    cntTreeMoveFile         =   0   #File moved from original location(due to duplicate/patttern/action .....)
    cntTreeFailOps          =   0

    for subdir, dirs, files in os.walk(baseDir.get('rootDir')):
        logger.info('-----------------------------------------------------')
        logger.info('Current DIR ' + subdir)

        # Statistics in directory level
        cntTotalFile        =   0   #count all files in dir
        cntProcessFile      =   0   #count of file processed
        cntIgnoreFile       =   0   #count ignore file
        cntDuplicateFile    =   0   #duplicate file count
        cntMoveFile         =   0   #move count
        cntFailOps          =   0

        for file in files:

            cntTotalFile+=1    #count all files in DIR
            fileAbsPath     = os.path.join(subdir,file)

            if fName.getExt(file) in opList or (not opList):
                logger.info('Processing  ['+file+']')
                cntProcessFile += 1

                # filter duplicate files
                if duplicatFilter:
                    if duplicateFilter(fileAbsPath,baseDir.get('duplicateBase')):
                        cntDuplicateFile+=1
                        continue

                if op == "MOVE_FILE":
                    taskDone = False
                    for sub in pattern:
                        if fName.isKeyWordFound(file,sub):
                            pickUp  =   fileAbsPath
                            drop    =   os.path.join(os.path.join(baseDir.get('moveDirBase'),sub) , file)
                            logger.debug('ARG FOR MOVE ['+pickUp+']['+drop+']')
                            if not fOps.moveFile(pickUp,drop):
                                logger.info('File pattern filter move operation failed for '+file)
                                taskDone = True
                                cntFailOps+=1
                                break
                            else:
                                logger.debug('File moved for pattern match  ['+pickUp+'] TO ['+sub+']'+drop)
                                cntMoveFile+=1
                                taskDone = True
                                break
                    if not taskDone:
                        if isMeta(fileAbsPath):
                            if not fOps.moveFile(fileAbsPath,os.path.join(baseDir.get('metaFileDir'),file)):
                                logger.critical('File Movement failed ')
                                cntFailOps+=1
                            else:
                                cntMoveFile+=1
                        else:
                            if not fOps.moveFile(fileAbsPath,os.path.join(baseDir.get('nonMetaFileDir'),file)):
                                logger.critical('File Movement failed ')
                                cntFailOps+=1
                            else:
                                cntMoveFile+=1
                elif op == "NEW_FEATURE":
                    logger.debug('NEW_FEATURE')



            else:
                logger.info('Ignore file [' + file+']')
                cntIgnoreFile+=1

        logger.info('Total File Available [' + str(cntTotalFile) + '] Processed [' + str(cntProcessFile) + '] Ignore [' + str(cntIgnoreFile) + '] File Move ['+str(cntMoveFile)+']')
        cntTreeTotalFile    =   cntTreeTotalFile    +   cntTotalFile
        cntTreeProcessFile  =   cntTreeProcessFile  +   cntProcessFile
        cntTreeIgnoreFile   =   cntTreeIgnoreFile   +   cntIgnoreFile
        cntTreeDuplicateFile=   cntTreeDuplicateFile+   cntDuplicateFile
        cntTreeMoveFile     =   cntTreeMoveFile     +   cntMoveFile
        cntTreeFailOps      =   cntTreeFailOps      +   cntFailOps

    logger.info('================================================================')
    logger.info('Total  File read in            ['+str(cntTreeTotalFile)+']')
    logger.info('       File we process         ['+str(cntTreeProcessFile)+']')
    logger.info('       File we ignore          ['+str(cntTreeIgnoreFile)+']')
    logger.info('       File found duplicate    ['+str(cntTreeDuplicateFile)+']')
    logger.info('       File we move            ['+str(cntTreeMoveFile)+']')
    logger.info('       Failed Tasks            ['+str(cntTreeFailOps)+']')
    logger.info('================================================================')
    return True

def isMeta(url):
    try:
        obj = imgObj(url)
        if obj :
            return obj.isMetaFound()
    except :
        logger.warning('File '+url+' is not loadable ')
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
                    logger.info('DUPLICATE FILE :: MOVE_TO ('+str(x)+') '+url+' TO '+target)
                    return True
                else:
                    pass
                    #logger.debug('DUPLICATE INDEX '+str(x)+' has conflict for '+url)
            else:   #DIR INDEX not found
                fOps.createDir(base,str(x))     # create index dir
                fOps.moveFile(url,target)
                logger.info('DUPLICATE FILE :: MOVE_BY_CREATE_NEW ('+str(x)+') '+url+' TO '+target)
                return True
    return False

def checkDuplicate(url):
    turn    =  booti.gethas(url)
    found  = pelter.get(turn)
    if found:
        logger.debug('Duplicate Found ['+url+'=AND='+found+']')
        return found
    else:
        pelter[turn]=url
        return ""

