# -*- coding: utf-8 -*-

# This script is meant to collect online images of characters from myanimelist.net
# This code will save the images in an "images" folder, as to not conflict with
# the "Data" folder already present in the repository. It will also devide characters
# according to narrative genre. None of these structures are expected by the
# Notebooks, so changes to their code or the file structure would be needed.
# It's important to note that the full execution of this file can take a few days
# due to the low transfer limit on the MAL servers.

from bs4 import BeautifulSoup
import requests
import os
import time
import sys
import urllib.request
import shutil

# Cleaning the names of characters to avoid problems when creating their folders
def cleanName(name):
    name = name.replace(":", " ")
    name = name.replace(";", " ")
    name = name.replace("\\", " ")
    name = name.replace("/", " ")
    name = name.replace("\"", "")
    name = name.replace("?", "")
    name = name.replace("\t", " ")
    while name[-1] == " ":
        name = name[:-1]
    return name

# Method to make the actual request and deal with the different responses
# Receives the URL to request from and the current iteration
# Returns the response
def getRequest(url, i):
    waitMin = 5 #In case of bad response, wait this time before trying again
    badResponse = False
    checked = False
    response = requests.get(url)
    while str(response) != "<Response [200]>":
        checked = True
        if badResponse: #Had already had a bad response for this request
            print(response)
            print("Aborting: more than one bad respoonse in a row")
            print(i)
            sys.exit()
        else: #First bad response for this request
            print(response)
            print(i)
            print("Waiting "+str(waitMin)+"min")
            badResponse = True
            time.sleep(waitMin*60)
            response = requests.get(url)
    if checked:
        print("Resuming")
    return response

# Get the narrative genres of the current show
# Receives the soup for the show
# Returns a list of strings representing the different genres, 
# or an empity list if it couldn't find genres in the soup
def getGenres(showSoup):
    infos = showSoup.find_all("div", class_ = "spaceit_pad")
    genreList = []
    for info in infos:
        infoType = info.find("span")
        if infoType != None and not "Genre" in infoType.text:
            continue
        genres = info.find_all("a")
        for genre in genres:
            genreList.append(genre.text)
        break
    return genreList

# Main
def main():
    limit = 10000 #Last show to check in the popularity rank
    start = 0 #Start from this swhow, can be changed in case the last execution aborted, to start from where it stopped. Should be changed in increments of 50
    
    # Variables used to display the current progress
    interval = limit // 100
    percent = start / limit
    
    # List of all existing genres, as strings
    allGenres = []
    
    # Iterating through the pages of shows, each page contains 50 shows
    for i in range(start, limit+1, 50):
        if i % interval == 0:
            print(str(percent)+"%")
            percent += 1
        
        # Requesting the current page of shows
        response = getRequest("https://myanimelist.net/topanime.php?type=bypopularity&limit="+str(i), i)
        soup = BeautifulSoup(response.text, "lxml")
        shows = soup.find_all("tr", class_ = "ranking-list")
        for show in shows:
            # Balancing the number of characters between both roles per show
            showCount = {"Main": 0, "Supporting": 0}
            showPage  = show.find("td", class_ = "title al va-t word-break").a["href"]
            
            # Requesting the current show
            showResponse = getRequest(showPage, i)
            showSoup = BeautifulSoup(showResponse.text, "lxml")
            genres = getGenres(showSoup)
            for genre in genres: #Creating folders for the new genres
                if not os.path.isdir("Images/" + genre):
                    os.makedirs("Images/" + genre)
                    os.makedirs("Images/" + genre + "/Main")
                    os.makedirs("Images/" + genre + "/Supporting")
                    allGenres.append(genre)
            showPage += "/characters"
            
            # Requesting characters from the current show
            showResponse = getRequest(showPage, i)
            showSoup = BeautifulSoup(showResponse.text, "lxml")
            characters = showSoup.find_all("table", class_ = "js-anime-character-table")
            for character in characters:
                divs = character.find_all("div", class_ = "spaceit_pad")
                charPage = divs[0].a["href"]
                role = divs[1].text.split()[0]
                
                # All main characters come before the Supporting characters,
                # so if the character fufills the following condition it means
                # that there are no main characters left in the show and it has
                # already achieved balance between both roles
                if role == "Supporting" and showCount["Supporting"] >= showCount["Main"]:
                    break
                
                # Requesting the current character
                charResponse = getRequest(charPage, i)
                charSoup = BeautifulSoup(charResponse.text, "lxml")
                charImg = charSoup.find("img", class_="lazyload")
                
                # Character has no image or the image has no valid source to
                # download it from
                if not charImg:
                    continue
                if not charImg.has_attr("alt") or not charImg.has_attr("data-src"):
                    continue
                name = charImg["alt"]
                imgLink = charImg["data-src"]
                name = cleanName(name)
                
                # Chekcing if there is already a character with the same name
                exists = False
                for genre in allGenres:
                    if os.path.isfile("Images/"+genre+"/Main/"+name+".png") or os.path.isfile("Binary Images Genre/"+genre+"/Supporting/"+name+".png"):
    					#print("Character already exists:", name)
                        exists = True
                        break
                if exists:
                    continue
                
                # Downloading the image and copying it for each one 
                # of the show's genres
                origPath = "Images/" + genres[0] + "/" + role + "/"
                urllib.request.urlretrieve(imgLink, origPath+name+".png")
                for j in range(1, len(genres)):
                    path = "Images/" + genres[j] + "/" + role + "/"
                    shutil.copyfile(origPath+name+".png", path+name+".png")
                showCount[role] += 1
    
    print("Done")
    
if __name__ == "main":
    main()