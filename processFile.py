import os
import logging
import util.fileName        as fName
import util.imgMetaData     as imgObj
import util.fileDirOSOps   as fOps
logger = logging.getLogger()

def processFullTree(rootDir,opList,op="NONE",pattern=[],breakStructure=True):
    logger.debug('ROOT IS           ['+rootDir+']')
    logger.debug('File Type         ['+str(opList)+']')
    logger.debug('Operation         ['+op+']')
    logger.debug('Pattern           ['+str(pattern)+']')
    logger.debug('Move to parent    ['+str(breakStructure)+']')
    #quit()
    logger.info('--------------------------------------------------')
    logger.info('            PROCESSING DIRs                       ')
    logger.info('            ' + rootDir)
    logger.info('Current valid file type are :' + str(opList))
    logger.info('--------------------------------------------------')
    moveDirBase=os.path.join(rootDir,'ImageSort_move')
    if fOps.createDir(rootDir,'ImageSort_move'):
        for sub in pattern:
            if not fOps.createDir(moveDirBase,sub):
                logger.critical('Sub directory '+sub+' creation failed')
    else:
        logger.critical('Directory creation Failed ')
    #quit()
    print('--'+moveDirBase)
    for subdir, dirs, files in os.walk(rootDir):
        logger.info('--------------------------------------------------')
        logger.info('Current DIR ' + subdir)
        validCnt = 0
        moveCnt = 0

        for file in files:
            if fName.getExt(file) in opList or not opList:
                logger.info('Processing file [' + file +']')
                validCnt += 1
                if op == "MOVE_FILE":
                    isFoundPattern = False
                    for sub in pattern:
                        if isFoundPattern: continue
                        if fName.isKeyWordFound(file,sub):
                            isFoundPattern = True
                            targetDir = os.path.join(moveDirBase,sub)
                            logger.debug(moveDirBase+'####'+sub+'####'+targetDir)
                            if not fOps.moveFile(os.path.join(subdir , file),os.path.join(targetDir , file)):
                                logger.critical('File Movement failed ')
                                continue
                        else:
                            continue


                elif op == "MOVE_FILE":
                    obj = imgObj(os.path.join(subdir , file))
                    if obj.isMetaFound():
                        logger.info('MetaData is Available ')
                        logger.info(str(obj.getMaker()) + "   " + str(obj.getModel()))
                    else:
                        logger.info('MetaData NOT FOUND ')
                        logger.debug(obj)
                else:
                    logger.warning('Unknown Operation')
            else:
                logger.debug(fName.getExt(file))
                logger.info('Ignore file' + file)
        logger.info('Total File Avialble [' + str(len(files)) + '] Processed [' + str(validCnt) + '] Ignore [' + str(
            len(files) - validCnt) + ']')
