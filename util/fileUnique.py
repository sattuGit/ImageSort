import hashlib
import os
CHUNKSIZE = 65536   #1024*64
def gethas(url):
    if not os.path.exists(url): return ""
    file_hash = hashlib.md5()
    with open(url, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(CHUNKSIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(CHUNKSIZE) # Read the next block from the file
    return file_hash.hexdigest() # Get the hexadecimal digest of the hash

def main():
    print(gethas('/home/satendra/Desktop/git/ImageSort/sample/_test.jpg'))

if __name__ == "__main__":
    main()
