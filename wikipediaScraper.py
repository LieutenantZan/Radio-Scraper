# Scrape Wikipedia to get more info on the songs from the radio scraper.
# Go through each layer of the csv generated from the radioScraper.py the search for it in Wikipedia.
#   Then, go through, select the first link because that is probably the right one
#   Once there, get info about the song such as year of release, length, genre, etc.Do for all songs in the CSV
#   Maybe create a dictionary of songs so that you don't have to search Wikipedia every time.
# Use gracenote.com for the info insead?

from lxml import html
import requests
from requests import compat
import time
import csv
from selenium import webdriver

song = []
artist = []
genres = []
songLength = []
releaseDate = []

def readCSV(file):
    with open(file, "r", encoding='utf-8', newline='') as csv_file: # use r+ for read and write. a+ might also work??
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            # print(', '.join(row)) #prints entire row at once
            # print(', '.join([row[3],row[4]])) # song name, artist
            #remove header here? Also need to remove LA Lloyd rock countdown and stuff
            song.append(row[3])
            artist.append(row[4])
    return


# def searchWiki():
#     page = requests.get('https://www.wikipedia.org')
#     tree = html.fromstring(page.content)
#     tree.xpath('//*[@id="searchInput"]')
#     return


def getInfo(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    info = tree.xpath('//*[@id="mw-content-text"]/div/table/tr')
    for entry in info:
        try:
            if entry.xpath('th/text()')[0] == 'Released':
                releaseDate.append(entry.xpath('td/text()'))
                print(entry.xpath('td/text()'))
        except IndexError:
            print('error')

    return

def main():
    readCSV('testData.csv')

    for i in range(len(song)):
        driver = webdriver.Chrome()
        driver.get('https://www.wikipedia.org')
        time.sleep(3)
        searchBox = driver.find_element_by_id('searchInput')
        s = song[i] + " " + artist[i]
        searchBox.send_keys(s)
        searchBox.submit()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@class="mw-search-results"]/li/div/a').click()
        time.sleep(3)
        print(driver.current_url)

        getInfo(driver.current_url)

        driver.quit()
    return


main()
