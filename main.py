from util.imgMetaData import imgObj
import util.fileName as fop
import os
import logging
logging.basicConfig(filename="ImageSorting.log",format='%(asctime)s %(levelname)s %(message)s',filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)

#rootDir =os.getcwd()
rootDir='/home/satendra/Desktop/10042020_mobileBackup/'
rootDir='/home/satendra/Desktop/8feb2020_bck'
opList = ['.JPG','.PNG']

logger.info('--------------------------------------------------')
logger.info('            PROCESSING DIRs                       ')
logger.info('            '+rootDir)
logger.info('Current valid file type are :'+str(opList))
logger.info('--------------------------------------------------')

for subdir, dirs, files in os.walk(rootDir):
    logger.info('--------------------------------------------------')
    logger.info('Current DIR '+subdir)
    #logger.info('Total Files available '+str(len(files)))
    validCnt=0
    for file in files:
        if fop.getExt(file) in opList:
            logger.info('Processing '+file)
            print(subdir+'/'+file)
            validCnt+=1
            obj= imgObj(subdir+'/'+file)
            if obj.isMetaFound():
                logger.info('MetaData is Available ')
                logger.info(str(obj.getMaker())+"   "+str(obj.getModel()))
            else:
                logger.info('MetaData NOT FOUND ')
                logger.debug(obj)
        else:
            logger.debug(fop.getExt(file))
            logger.info('Ignore file'+file)
    logger.info('Total File Avialble ['+str(len(files))+'] Processed ['+str(validCnt)+'] Ignore ['+str(len(files)-validCnt)+']')
