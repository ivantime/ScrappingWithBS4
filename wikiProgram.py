import signal
import sys
import requests
import time
import json
from bs4 import BeautifulSoup
from itertools import combinations
import time
import random

words2Scrap=["Computer", "Glasgow", "United", "Kingdom", "Library", "Fog", "Empires", "Doctor", "Hospital", "Bachelor", 
"Degree", "Internet", "Things", "Information", "Info", "Retrieval", "Retrieve", "Info", "Universe", "University"]

#Source: https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements#answer-32555776
def combs(x):
    return [c for i in range(len(x)+1) for c in combinations(x,i)]


lister1= list(combs(words2Scrap))
lister = []

for item in lister1:
    if (len(item) == 5 or len(item) < 6) and len(item) !=0 :
        lister.append(item)

def sleepingNow():
    randSeconds = random.randint(1, 600)
    print("\n\nzzzzz Sleeping for ",randSeconds," sec(s)")
    time.sleep(randSeconds)
    print("ooooo Awake Now")

def formatSearchTerm4url(typle,index):
    searchTerm=""
    for i,d in enumerate(list(typle[index])):
        if (i!=0):
            searchTerm+="+"+str(d)
        else:
            searchTerm=d
    urlMain= f"https://en.wikipedia.org/w/index.php?search="+ searchTerm

    # get the redirected URL's destination (.url) A.K.A non-Search query URL
    urlMain = requests.get(urlMain).url
    return urlMain

new1stDiscoveredURLs={}
new2ndDiscoveredURLs={}
wikiArray=[]
addedJson={}

def signal_handler(sig, frame):
    #Finished Main Seeds (addedJson)
    if len(addedJson.keys())!=0:
        wikiArray.append(addedJson)
    
    #Finished 2nd Deep Link Crawl
    if len(new1stDiscoveredURLs.keys())!=0:
        wikiArray.append(new1stDiscoveredURLs)
    
    #Finished 3rd Deep Link Crawl
    if len(new2ndDiscoveredURLs.keys())!=0:
        wikiArray.append(new1stDiscoveredURLs)
    
    #Export Json to File
    try:
        wikiJson ={}
        for item in wikiArray:
            for key, value in item.items():
                wikiJson[key]=value
        
        with open('wikiFile.json', 'w') as outfile:
            json.dump(wikiJson, outfile)
        print("Exported to JSON for Wiki URLs as name: \'wikiFile.json\'")
    except Exception as e:
        print("Couldn't export to CSV for Wiki URLs... Stack Trace Here:\n")
        print(e)
    sys.exit(0)

def getLinksFromSearch(lister,index):
    #prepare for Control-C Keyboard Intterupt (get all existing Wiki data into Json)
    signal.signal(signal.SIGINT, signal_handler)
    
    for indexCurr,itemCurr in enumerate(lister):
        
        URL = formatSearchTerm4url(lister,indexCurr)
        print("\n\nCurrently Main Seed:"+str(indexCurr+1)," of ",len(lister))
        if (indexCurr<index+1):
            
            #if using Keyword Search
            sleepingNow()
            connectPassed=True
            try:
                page = requests.get(URL)
            except:
                connectPassed=False
            

            if (connectPassed == True):
                soup = BeautifulSoup(page.content, "html.parser")
                job_elements = soup.find("h1",{"id":"firstHeading"})
                contentTitle = job_elements.text

                if ("Search results" in job_elements.text):
                
                    print("Page is Wiki Search Page: "+URL)
                    #returned page is a search result page with multiple wiki pages
                    job_elements = soup.find("ul",{"class":"mw-search-results"}).find_all("a",href=True)

                    for index1,item1 in enumerate(job_elements):
                        url = "https://en.wikipedia.org"+item1['href']

                        found=False
                        for index,item in enumerate(wikiArray):
                            if (url in item or url in addedJson):
                                found = True

                        if (found==False):
                            contentTxt = ""

                            #if using Keyword Search
                            sleepingNow()
                            connectPassed=True
                            try:
                                page = requests.get(url)
                            except:
                                connectPassed=False


                            if (connectPassed == True):
                                soup = BeautifulSoup(page.content, "html.parser")
                                job_elements = soup.find("h1",{"id":"firstHeading"})
                                contentTitle = job_elements.text
                                job_elements = soup.find("div",{"id":"mw-content-text"}).find_all()
                                for item in job_elements:
                                    try:
                                        contentTxt = contentTxt + item.text
                                    except:
                                        pass

                                print("URL: "+page.url)
                                print("TITLE~\n"+contentTitle)
                                print("content~\n"+contentTxt)

                                addedJson[page.url]={"title":contentTitle,"content":contentTxt}
                                print("***Added URL:", page.url)

                                ####################################
                                #Get 2nd Deep Link from Main Seed
                                potentialLinks = soup.find("div",{"id":"mw-content-text"}).find_all("a", href=True)
                                for link in potentialLinks:
                                    currLink = link['href']
                                    failed = False

                                    if currLink[0] == "#":
                                        failed = True


                                    #if URL is not a reference within the Current Wiki Page
                                    if (failed == False):
                                        #Check if URL is in Store
                                        for index,item in enumerate(wikiArray):
                                            if (currLink in addedJson):
                                                failed = True
                                            jsonData = wikiArray[index]
                                            for key1 in jsonData.keys():
                                                if key1 in currLink:
                                                    failed = True
                                    if ("/wiki/" in currLink and "wikipedia.org" not in currLink):
                                        currLink = "https://en.wikipedia.org" + currLink

                                    if (("search=" in currLink or "wiki/File:" in currLink) and "wikipedia" in currLink):
                                        print("Potential New Discovered URL is a Wiki File/Search (not adding):   "+currLink)
                                    elif (failed==False and "wikipedia" in currLink):
                                        contentTxt = ""

                                        #if using Keyword Search
                                        sleepingNow()
                                        connectPassed=True
                                        try:
                                            page = requests.get(currLink)
                                        except:
                                            connectPassed=False

                                        if (connectPassed == True):
                                            soup = BeautifulSoup(page.content, "html.parser")
                                            job_elements = soup.find("h1",{"id":"firstHeading"})
                                            contentTitle = job_elements.text
                                            job_elements = soup.find("div",{"id":"mw-content-text"}).find_all()
                                            for item in job_elements:
                                                try:
                                                    contentTxt = contentTxt + item.text
                                                except:
                                                    pass

                                            print("URL: "+page.url)
                                            print("TITLE~\n"+contentTitle)
                                            print("content~\n"+contentTxt)

                                            new1stDiscoveredURLs[page.url]={"title":contentTitle,"content":contentTxt}
                                            print("***Added URL:", page.url)

                                        else:
                                            print("cannot connect to URL:"+currLink)
                                    else:
                                        print("Potential New Discovered URL found in Store (not adding):   "+currLink)

                                    print("\n\nCurrently at Main Seed (Depth 2):"+str(indexCurr+1)," of ",len(lister),"\n| Main Seed Link:"+URL)  

                            else:
                                print("cannot connect to URL:"+url)
                        else:
                            print("duplicated URL found in Store (not adding):   ",url)
    
    
                else:
                    print("Page is Wiki Details Page: "+URL)

                    found=False
                    for index,item in enumerate(wikiArray):
                        if (URL in item or URL in addedJson):
                            found = True

                    if (found==False):
                        contentTxt = ""
                        
                        #if using Keyword Search
                        sleepingNow()
                        connectPassed=True
                        try:
                            page = requests.get(URL)
                        except:
                            connectPassed=False


                        if (connectPassed == True):
                            soup = BeautifulSoup(page.content, "html.parser")
                            job_elements = soup.find("h1",{"id":"firstHeading"})
                            contentTitle = job_elements.text
                            job_elements = soup.find("div",{"id":"mw-content-text"}).find_all()
                            for item in job_elements:
                                try:
                                    contentTxt = contentTxt + item.text
                                except:
                                    pass

                            print("URL: "+page.url)
                            print("TITLE~\n"+contentTitle)
                            print("content~\n"+contentTxt)

                            addedJson[page.url]={"title":contentTitle,"content":contentTxt}
                            print("***Added URL:", page.url)

                            ####################################
                            #Get 2nd Deep Link from Main Seed
                            potentialLinks = soup.find("div",{"id":"mw-content-text"}).find_all("a", href=True)
                            for link in potentialLinks:
                                currLink = link['href']
                                failed = False


                                if currLink[0] == "#":
                                    failed = True


                                #if URL is not a reference within the Current Wiki Page
                                if (failed == False):
                                    #Check if URL is in Store
                                    for index,item in enumerate(wikiArray):
                                        if (currLink in addedJson):
                                            failed = True
                                        jsonData = wikiArray[index]
                                        for key1 in jsonData.keys():
                                            if key1 in currLink:
                                                failed = True
                                if ("/wiki/" in currLink and "wikipedia.org" not in currLink):
                                    currLink = "https://en.wikipedia.org" + currLink

                                if (("search=" in currLink or "wiki/File:" in currLink) and "wikipedia" in currLink):
                                    print("Potential New Discovered URL is a Wiki File/Search (not adding):   "+currLink)
                                elif (failed==False and "wikipedia" in currLink):
                                    contentTxt = ""
                                    
                                    #if using Keyword Search
                                    sleepingNow()
                                    connectPassed=True
                                    try:
                                        page = requests.get(currLink)
                                    except:
                                        connectPassed=False

                                    if (connectPassed == True):
                                        soup = BeautifulSoup(page.content, "html.parser")
                                        job_elements = soup.find("h1",{"id":"firstHeading"})
                                        contentTitle = job_elements.text
                                        job_elements = soup.find("div",{"id":"mw-content-text"}).find_all()
                                        for item in job_elements:
                                            try:
                                                contentTxt = contentTxt + item.text
                                            except:
                                                pass

                                        print("URL: "+page.url)
                                        print("TITLE~\n"+contentTitle)
                                        print("content~\n"+contentTxt)

                                        new1stDiscoveredURLs[page.url]={"title":contentTitle,"content":contentTxt}
                                        print("***Added URL:", page.url)

                                    else:
                                        print("cannot connect to URL:"+URL)
                                else:
                                    print("Potential New Discovered URL found in Store (not adding):   "+currLink)

                                print("\n\nCurrently at Main Seed (Depth 2):"+str(indexCurr+1)," of ",len(lister),"\n| Main Seed Link:"+URL)  
                        
                        else:
                            print("cannot connect to URL:"+URL)
                    else:
                        print("duplicated URL found in Store (not adding):   ",URL)

                print("\n\nCurrently at Main Seed (Depth 1):"+str(indexCurr+1)," of ",len(lister),"\n| Main Seed Link:"+URL)     
            
            else:
                print("cannot connect to URL:"+URL)            
        print("\n\nCurrently at Main Seed (Depth 1):"+str(indexCurr+1)," of ",len(lister),"\n| Main Seed Link:"+URL)
    
    #Finished Main Seeds (addedJson)
    if len(addedJson.keys())!=0:
        wikiArray.append(addedJson)
    
    #Finished 2nd Deep Link Crawl
    if len(new1stDiscoveredURLs.keys())!=0:
        wikiArray.append(new1stDiscoveredURLs)
    
    #Finished 3rd Deep Link Crawl
    if len(new2ndDiscoveredURLs.keys())!=0:
        wikiArray.append(new1stDiscoveredURLs)
    
    #Export Json to File
    try:
        wikiJson ={}
        dict1={}

        for item in wikiArray:
            for key, value in item.items():
                wikiJson[key]=value
        dict1["all_content"]=wikiJson
        with open('wikiFile.json', 'w') as outfile:
            json.dump(dict1, outfile)
        print("Exported to JSON for Wiki URLs as name: \'wikiFile.json\'")
    except Exception as e:
        print("Couldn't export to CSV for Wiki URLs... Stack Trace Here:\n")
        print(e)


    

#start with empty dictionary {}
newArray =[]
getLinksFromSearch(lister,len(lister)-1)


#Crawler Flow:
'''
    Go through List of keywords>get URL from Wiki Search> EITHER: 
    ##########(1) 
    [[Depth 1]]
    Wiki Search Returns Wiki Page (Not Search Page):
    Crawl Wiki Page for Title and Content>

    [[Depth 2]]
    Get newly Discovered Links in Wiki Page (known as '2nd Deep Layer')>
    Crawl Wiki Page of newly Discovered Links (in '2nd Deep Layer') for Title and Content>

    ##########[[END for (1)]]




    ##########(2) 
    Wiki Search Returns Wiki Search Page LIST
    [[Depth 1]]
    Wiki Search Returns Wiki Page (Not Search Page):
    Crawl Wiki Page for Title and Content>

    [[Depth 2]]
    Get newly Discovered Links in Wiki Page (known as '2nd Deep Layer')>
    Crawl Wiki Page of newly Discovered Links (in '2nd Deep Layer') for Title and Content>
    ##########[[END for (2)]]

'''