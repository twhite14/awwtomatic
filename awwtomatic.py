#Awwtomatic v0.4
#Automatically fetches the source code of http://www.reddit.com/r/aww/ and downloads .png, .jpg, .jpeg, .gifv, and .gif files from imgur.
#To be implemented: downloading files on imgur pages, downloading imgur albums, checking if a file exists already (under the same name or an md5 check.)

#urllib is used to obtain the HTML of /r/aww and to acquire the images from imgur.
import urllib
import time

DEBUG = True

#Make sure that the User-Agent isn't the default so reddit doesn't disrupt things.
class awwURLOpener(urllib.FancyURLopener):
  version = '<platform>:awwtomatic:0.4 (by /u/<redditUsername>)'
  
def addToAllFoundURLs(textDocument, appendToThis):
  awwSearchIndex = 0
  awwCurrentIndex = 0
  awwEndIndex = 0
  #Next line was determined by reading the reddit source code. Constant substrings may be changed if reddit changes format.
  awwSearchSubstring = '<a class="title may-blank " href="'
  #Find all references to imgur links from submissions, as determined by the structure of the /r/aww source code.
  while(awwSearchIndex != -1): 
    awwSearchIndex = localAwwTxt.find(awwSearchSubstring,awwCurrentIndex + 1,len(localAwwTxt))
    awwCurrentIndex = awwSearchIndex + len(awwSearchSubstring)
    awwEndIndex = localAwwTxt.find('"',awwCurrentIndex,len(localAwwTxt))
    #Append valid entries to the list
    if(awwSearchIndex != -1):
      allFoundURLs.append(localAwwTxt[awwCurrentIndex:awwEndIndex])
  #Finished with the given page
  
urllib._urlopener = awwURLOpener()

mainURL = 'http://www.reddit.com/r/aww/'
acquisitionPageURL = mainURL
pageLinkSearchSubstring = '/r/aww/?count='

#Lists which will contain imgur references.
allFoundURLs = []   #URLs that have not been trimmed yet
newFoundURLs = []   #URLs that have been trimmed down to just the imgur identifier

for i in xrange(0,4):
  #Get the source code for the page of interest, store it to a file locally.
  if(DEBUG):  print 'Acquiring ' + acquisitionPageURL
  #Open the applicable page source.
  localAwwTxt = urllib.urlopen(acquisitionPageURL).read()
  addToAllFoundURLs(localAwwTxt, allFoundURLs)
  nextPageSearchSubstring = pageLinkSearchSubstring + str((i + 1) * 25)
  nextPageNear = localAwwTxt.find(nextPageSearchSubstring)
  nextPageBegin = localAwwTxt.rfind('"', 0, nextPageNear) + 1
  nextPageEnd = localAwwTxt.find('"', nextPageBegin, len(localAwwTxt))
  acquisitionPageURL = localAwwTxt[nextPageBegin:nextPageEnd]
  acquisitionPageURL = acquisitionPageURL.replace('amp;', '') #Required since ampersand symbols (&) are read in as &amp; for some reason.
  time.sleep(3)
  
#Open acquired images history file in read/write mode
try:
  acquiredTxt = open('acquired.txt', 'r+')
except IOError:
  acquiredTxt = open('acquired.txt', 'w')
  acquiredTxt.close()
  acquiredTxt = open('acquired.txt', 'r+')

#Set up some variables.
entries = 0
directURL = 0
imgurPage = 0
imgurAlbum = 0
falseEntries = 0

folder = 'downloads/'

#Trim the found URLs down to only the imgur identifiers
#This is necessary since links on reddit may have the extension .jpg when they are in fact .gif or .gifv files
for url in allFoundURLs:
  trimSearchSubstring = '.com/'
  preUniqueID = url.find(trimSearchSubstring) + len(trimSearchSubstring)
  #Check if this is a direct link to an image, get the ending point accordingly.
  if(url.find('.',preUniqueID,len(url)) != -1):
    postUniqueID = url.find('.',preUniqueID,len(url))
  #If it's an album or page link this will execute instead
  else:
    postUniqueID = len(url)
  #Go back to the beginning of the file, search it for the ID, if it doesnt exist add the ID to newFoundURLs
  acquiredTxt.seek(0,0)
  if(acquiredTxt.read().find(url[preUniqueID:postUniqueID]) == -1):
    acquiredTxt.seek(0,2)
    acquiredTxt.write(url[preUniqueID:postUniqueID] + '\n')
    newFoundURLs.append(url[preUniqueID:postUniqueID])
acquiredTxt.close()
    
#Go to imgur and obtain the files individually.
for url in newFoundURLs:
  obtainAlbumSearchSubstring = 'a/'
  obtainPageSearchSubstringNOT = '.'
  obtainPNGSearchSusbtring  = '.png'
  obtainJPGSearchSusbtring  = '.jpg'
  obtainJPEGSearchSusbtring = '.jpeg'
  obtainGIFVSearchSusbtring = '.gifv'
  obtainGIFSearchSusbtring  = '.gif'
  #Check for album
  if(url.find(obtainAlbumSearchSubstring) != -1):
    #To be implemented
    
    if(DEBUG):  print '  Failed Album.'
    #entries = entries + 1
    imgurAlbum = imgurAlbum + 1
    
  #Check if this is a link to a page (does not contain a .)
  elif(url.find(obtainPageSearchSubstringNOT) == -1):
    pageSearchStringPNG = '<link rel="image_src"'
    pageSearchStringWEBM = 'gifUrl:'
    pageImgurURLPreamble = 'http://imgur.com/'
    #Open the imgur source.
    localImgurTxt = urllib.urlopen(pageImgurURLPreamble + url).read()
    
    #Determine if the file can be saved as a .PNG
    if(localImgurTxt.find(pageSearchStringPNG) != -1):
      pageNearIndex = localImgurTxt.find(pageSearchStringPNG) + len(pageSearchStringPNG)            #Get close to the URL using a known place in the source code
      pageBeginIndex = localImgurTxt.find('"', pageNearIndex, len(localImgurTxt)) + 1               #The first " after the pageNearIndex is one before the beginning of the URL
      pageEndIndex = localImgurTxt.find('"', pageBeginIndex + 1, len(localImgurTxt))                #The first " after the pageBeginIndex is the end of the URL
      newFoundURLs.append(localImgurTxt[pageBeginIndex:pageEndIndex])                               #Append the found URL to the end of the list so it gets the image on a future pass
      if(DEBUG):  print '  GOT IMGURPAGE (.png)  Will save file on future pass.'
    
    #Determine if the file can be saved as a .WEBM
    elif(localImgurTxt.find(pageSearchStringWEBM) != -1):
      pageNearIndex = localImgurTxt.find(pageSearchStringWEBM) + len(pageSearchStringWEBM)          #Get close to the URL using a known place in the source code
      pageBeginIndex = localImgurTxt.find("'", pageNearIndex, len(localImgurTxt)) + 1               #The first ' after the pageNearIndex is one before the beginning of the URL
      pageEndIndex = localImgurTxt.find("'", pageBeginIndex + 1, len(localImgurTxt))                #The first ' after the pageBeginIndex is the end of the URL
      #This is specific for .gif files since the page is formatted differently
      gifURLPreamble = 'http:'
      newFoundURLs.append(gifURLPreamble + localImgurTxt[pageBeginIndex:pageEndIndex])              #Append the found URL to the end of the list so it gets the image on a future pass
      if(DEBUG):  print '  GOT IMGURPAGE (.webm) Will save file on future pass.'
      
    else:
      falseEntries = falseEntries + 1
      if(DEBUG):  print '  Failed IMGURPAGE'
    imgurPage = imgurPage + 1  
    
  #Search for .png files and download
  elif(url.find(obtainPNGSearchSusbtring) != -1):
    extensionBegin = url.find(obtainPNGSearchSusbtring)
    urllib.urlretrieve(url[0:extensionBegin] + '.png', folder + url[19:extensionBegin] + '.png')
    if(DEBUG):
      print url
      print '  GOT .PNG'
    entries = entries + 1
    directURL = directURL + 1
    
  #Search for .jpg files and download as .png
  elif(url.find(obtainJPGSearchSusbtring) != -1):
    extensionBegin = url.find(obtainJPGSearchSusbtring)
    urllib.urlretrieve(url[0:extensionBegin] + '.png', folder + url[19:extensionBegin] + '.png')
    if(DEBUG):
      print url
      print '  GOT .JPG'
    entries = entries + 1
    directURL = directURL + 1
    
  #Search for .jpeg files and download as .png
  elif(url.find(obtainJPEGSearchSusbtring) != -1):
    extensionBegin = url.find(obtainJPEGSearchSusbtring)
    urllib.urlretrieve(url[0:extensionBegin] + '.png', folder + url[19:extensionBegin] + '.png')
    if(DEBUG):
      print url
      print '  GOT .JPEG'
    entries = entries + 1
    directURL = directURL + 1
    
  #Search for .gifv files and download as .webm
  #Must be placed before .gif check or .gif fires in its place
  elif(url.find(obtainGIFVSearchSusbtring) != -1):
    extensionBegin = url.find(obtainGIFVSearchSusbtring)
    urllib.urlretrieve(url[0:extensionBegin] + '.webm', folder + url[19:extensionBegin] + '.webm')
    if(DEBUG):
      print url
      print '  GOT .GIFV'
    entries = entries + 1
    directURL = directURL + 1
    
  #Search for .gif files and download as .webm
  elif(url.find(obtainGIFSearchSusbtring) != -1):
    extensionBegin = url.find(obtainGIFSearchSusbtring)
    urllib.urlretrieve(url[0:extensionBegin] + '.webm', folder + url[19:extensionBegin] + '.webm')
    if(DEBUG):  
      print url
      print '  GOT .GIF'
    entries = entries + 1
    directURL = directURL + 1
    
  else:
    if(DEBUG):
      print url
      print '  Failed Other,'
    falseEntries = falseEntries + 1

if(DEBUG):
  print str(entries) + ' valid entries.'
  print str(falseEntries) + ' invalid entries.'
  print str(imgurAlbum) + ' albums'
  print str(imgurPage) + ' pages'
  print str(directURL) + ' images'
