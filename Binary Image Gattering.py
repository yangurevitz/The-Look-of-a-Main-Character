# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os
import time
import sys
import urllib.request

waitMin = 5

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

def getRequest(url, i):
    badResponse = False
    checked = False
    response = requests.get(url)
    while str(response) != "<Response [200]>":
        checked = True
        if badResponse:
            print(response)
            print("Abortando")
            print(i)
            sys.exit()
        else:
            print(response)
            print(i)
            print("Esperando 5min")
            badResponse = True
            time.sleep(waitMin*60)
            response = requests.get(url)
    if checked:
        print("Voltando")
    return response

target = 5000
limit = 10000
start = 15006
count = {"Main": 4873, "Supporting": 4684}
interval = target // 100
percent = {"Main": int(count["Main"]/target*100)+1, "Supporting": int(count["Supporting"]/target*100)+1}

for i in range(start, limit+1, 50):
    if count["Main"] >= target and count["Supporting"] >= target:
        break
    response = getRequest("https://myanimelist.net/topanime.php?type=bypopularity&limit="+str(i), i)
    soup = BeautifulSoup(response.text, "lxml")
    shows = soup.find_all("tr", class_ = "ranking-list")
    for show in shows:
        showCount = {"Main": 0, "Supporting": 0}
        showPage  = show.find("td", class_ = "title al va-t word-break").a["href"]
        showPage += "/characters"
        showResponse = getRequest(showPage, i)
        showSoup = BeautifulSoup(showResponse.text, "lxml")
        characters = showSoup.find_all("table", class_ = "js-anime-character-table")
        for character in characters:
            divs = character.find_all("div", class_ = "spaceit_pad")
            charPage = divs[0].a["href"]
            role = divs[1].text.split()[0]
            if role == "Supporting" and showCount["Supporting"] >= showCount["Main"]:
                break
            charResponse = getRequest(charPage, i)
            charSoup = BeautifulSoup(charResponse.text, "lxml")
            charImg = charSoup.find("img", class_="lazyload")
            if not charImg:
                continue
            if not charImg.has_attr("alt") or not charImg.has_attr("data-src"):
                continue
            name = charImg["alt"]
            imgLink = charImg["data-src"]
            name = cleanName(name)
            if os.path.isfile("Binary Images/Main/"+name+".png") or os.path.isfile("Binary Images/Supporting/"+name+".png"):
                #print("Character already exists:", name)
                continue
            path = "Binary Images/" + role + "/"
            urllib.request.urlretrieve(imgLink, path+name+".png")
            showCount[role] += 1
            count[role] += 1
            if count[role]%interval == 0:
                print(role, str(percent[role]) + "%")
                percent[role] += 1

print("Concluido")