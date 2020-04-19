import os
import shutil
import filecmp
import logging
logger = logging.getLogger()
def createDir(path,dirName):
    if os.path.isdir(os.path.join(path,dirName)): return True
    #logger.debug(path+' '+dirName)
    target=os.path.join(path,dirName)
    #logger.debug(target)
    try:
        os.mkdir(target)
    except OSError:
        return False
    return True

'''
source : full path with file name 
target : full path with file name 
        in case of missing file name , it wont assume same file name as unix 
        if you provide different file name then move + rename similar to unix mv
'''
def moveFile(source,target,checkIdentical=False,rename=False,patch="#"):
    logger.debug(source+'####'+target)
    identical=False
    if os.path.exists(source):
        logger.debug('FILE EXIST '+source)

        if  os.path.exists(target):
            logger.debug('Target FileName exist '+target)
            if checkIdentical :
                if filecmp.cmp(source,target): identical=True
            if identical and rename:
                target=target+'_Duplicate'
            elif rename and (not identical):
                target=target+patch

            try:
                resPath = shutil.move(source,target)
            except:
                logger.critical('Error whole move file '+source)
                return False

            logger.debug('SHUTIL '+source+'##'+target+'##'+resPath)
            if not os.path.exists(resPath):
                logger.critical('Error whole move file '+source+'||'+resPath)
                return False
            else:
                logger.debug('ACTUAL MOVE DONE'+resPath)
                return True
        else:
            #No Name Conflict
            logger.debug('Target FileName NOT exist '+target)
            try:
                resPath = shutil.move(source,target)
            except:
                logger.critical('Error whole move file '+source)
                return False
            logger.debug('SHUTIL '+source+'##'+target+'##'+resPath)
            if not os.path.exists(resPath):
                logger.critical('Error whole move file '+source)
                return False
            else:
                logger.debug('ACTUAL MOVE DONE'+resPath)
                return True
    else:
        logger.critical('Given Path ['+source+'] is Invalid')
        return False

def main():
    print('Called '+__name__)
    base='/home/satendra/Desktop/git/ImageSort/sample/'
    moveFile(base+'_test.jpg',base+'t2/_Xtest.jpg')

if __name__ == "__main__":
    main()
