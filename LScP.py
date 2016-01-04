#!/usr/bin/env python3
import requests
import threading
import time  
import urllib
import os  

STATIC_PREFIX = "http://www.lschs.org/uploaded/_assets/images/portraits/students/2015-16/"
STATIC_SUFFIX = ".jpg"
DEFAULT_START = 160000
DEFAULT_END = 200000
DEFAULT_THREAD_LIMIT = 2500
DEFAULT_THREAD_START_DELAY = 0.001
DO_DOWNLOAD = True
NOT_IMPORTANT_MSG = True

startSeed = DEFAULT_START
endSeed = DEFAULT_END
threadLimit = DEFAULT_THREAD_LIMIT
threadStartDelay = DEFAULT_THREAD_START_DELAY
threadCount = 0
threadIdAllocation = 0
runMain = True
resultFile = open('lscrawler.log', 'a')

def getThreadId():
    global threadIdAllocation
    threadIdAllocation += 1
    return (threadIdAllocation)

#Make all file write stuff to threads.
class thread_downloadPicture(threading.Thread): 
    def __init__(self, url, name): 
        threading.Thread.__init__(self) 
        self.threadId = getThreadId()
        self.url = url 
        self.name = name 
    def run(self): #Overwrite run() method, put what you want the thread do here
        global threadCount
        prefix = "[Thread." + str(self.threadId) + "] "
        threadCount += 1
        print(prefix + "Start to download " + str(self.name) + ".")
        savePath = "Pictures"
        try:
            if not os.path.exists(savePath):  
                os.makedirs(savePath)
            urllib.request.urlretrieve(self.url, savePath + os.sep + self.name)
        except:
            print(prefix + str(self.name) + " failed to download.")
        else:
            print(prefix + str(self.name) + " has been downloaded succesfully.")
        threadCount -= 1
#Make all file write stuff to threads.
class thread_writeFile(threading.Thread): 
    def __init__(self, file, content): 
        threading.Thread.__init__(self) 
        self.file = file 
        self.content = content 
    def run(self): #Overwrite run() method, put what you want the thread do here
        try:
            self.file.write(self.content)
        except:
            self.file.close()
            print ("[ERROR] Failed to write \"" + self.content + "\" to file.")

#Multithreading!
class thread_try(threading.Thread): 
    def __init__(self, seed, address): 
        threading.Thread.__init__(self) 
        self.threadId = getThreadId() 
        self.seed = seed
        self.address = address 
    def run(self): #Overwrite run() method, put what you want the thread do here 
        global threadCount
        prefix = "[Thread." + str(self.threadId) + "] "
        threadCount += 1
        if NOT_IMPORTANT_MSG:
            print(prefix + "Start to working on with #" + str(self.seed))
        try:
            r = requests.head(self.address)
            statusCode = r.status_code #gets the response code from the webpage
            if statusCode == 200: # if the webpage succesfully connected...
                print (prefix + "Hit 1 target!") # print that it hit a valid webpage...
                print (prefix + "Address: " + self.address + ".]") # and print the webpage number
                #write to file
                thread_writeFile(resultFile, self.address + "\n").start() # write to the file "lscrawler.log" the full webpage address of the valid webpages
                if DO_DOWNLOAD:
                    print(prefix + "Download mode is on, make new thread to download it...")
                    thread_downloadPicture(self.address, str(self.seed) + ".jpg").start()
            else:
                if NOT_IMPORTANT_MSG:
                    print(prefix + "#" + str(self.seed) + " is not a picture. :(") # print webpages that failed as well
        except requests.ConnectionError:
            print(prefix + "Failed to connect...")
        threadCount -= 1
        
class thread_main(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
    def run(self): #Overwrite run() method, put what you want the thread do here 
        seed = startSeed
        while seed <= endSeed:
            if (threadCount < threadLimit)&(runMain):
                thread_try(seed, STATIC_PREFIX + str(seed) + STATIC_SUFFIX).start()
            seed += 1
            time.sleep(threadStartDelay)           
thread_main().start()
input()
runMain = False
resultFile.close()
print("Stoping...")
