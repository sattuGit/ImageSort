import os
import logging
import util.fileName        as fName
import util.imgMetaData     as imgObj
import util.fileDirOSOps    as fOps
import util.fileUnique      as booti
logger = logging.getLogger()
pelter = {}
filterBase = 'ImageSort_move'
duplicateRoot = 'DUPLICATE'
def processFullTree(rootDir,opList,op="NONE",pattern=[],breakStructure=True):
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

    moveDirBase=os.path.join(rootDir,filterBase)
    duplicateBase = os.path.join(moveDirBase,duplicateRoot)
    if fOps.createDir(rootDir,filterBase): # ./filterBase
        for sub in pattern:
            if not fOps.createDir(moveDirBase,sub): #./filterBase/pattern
                logger.critical('Sub directory '+sub+' creation failed')

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

        for file in files:
            fileAbsPath = os.path.join(subdir,file)
            print('Processing...['+fileAbsPath+']')
            logger.info('=====START')
            if fName.getExt(file) in opList or not opList:
                validCnt += 1
                # filter duplicate files
                if duplicateFilter(fileAbsPath,duplicateBase):
                    continue
                else:
                    logger.info('UNIQUE FILE....'+fileAbsPath)

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



                #elif op == "COPY_FILE":
                #    obj = imgObj(os.path.join(subdir , file))
                #    if obj.isMetaFound():
                #        logger.info('MetaData is Available ')
                #        logger.info(str(obj.getMaker()) + "   " + str(obj.getModel()))
                #    else:
                #        logger.info('MetaData NOT FOUND ')
                #        logger.debug(obj)
                #
                else:
                    logger.warning('Unknown Operation')
            else:
                logger.debug('Ignore file' + file)
        logger.info('Total File Avialble [' + str(len(files)) + '] Processed [' + str(validCnt) + '] Ignore [' + str(
            len(files) - validCnt) + ']')

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
    i=0

if __name__ == "__main__":
    main()
