import os
import shutil
import logging
logger = logging.getLogger()
def createDir(path,dirName):
    logger.debug(path+' '+dirName)
    target=os.path.join(path,dirName)
    logger.debug(target)
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
def moveFile(source,target):
    logger.debug(source+'####'+target)
    if os.path.exists(source) and (not(os.path.exists(target))):
        logger.debug('source found target not found ')
        try:
            if not os.path.exists(shutil.move(source,target)):
                return False
        except:
            return False
    return True

def main():
    print('Called '+__name__)

if __name__ == "__main__":
    main()
