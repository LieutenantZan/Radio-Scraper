from lxml import html
import requests
from requests import compat
from datetime import date, timedelta
import time
import csv

# KLBJ Info
# BobFM has the same structure as KLBJ, so put them in a function that cycles through the different pages

#Global variables for song info - my be able to change to locals
songDate = []
songTimestamp = []  # klbjtree.xpath('//div[@class="views-field views-field-field-timestamp"]/div/span/text()')
songTitle = []  # klbjtree.xpath('//div[@class="views-field views-field-field-title"]/div/text()')
songArtist = []  # klbjtree.xpath('//div[@class="views-field views-field-field-artist"]/div/span/text()')
radioStation = []


def printSongs():
    for i in range(len(songTitle)):
        print(radioStation[i], " ", songDate[i], " ", songTimestamp[i], "	 ", songTitle[i], "	by ", songArtist[i])
        i += 1
    return;


def songCollection (url, pages, station, date):
    for p in pages:
        link = requests.compat.urljoin(url, p)
        page = requests.get(link)
        tree = html.fromstring(page.content)

        for i in range(len(tree.xpath('//div[@class="views-field views-field-field-timestamp"]/div/span/text()'))):
            songDate.append(date.strftime('%m/%d/%Y'))
            radioStation.append(station)
        songTimestamp.extend(tree.xpath('//div[@class="views-field views-field-field-timestamp"]/div/span/text()'))
        songTitle.extend(tree.xpath('//div[@class="views-field views-field-field-title"]/div/text()'))
        songArtist.extend(tree.xpath('//div[@class="views-field views-field-field-artist"]/div/span/text()'))

    return;


def getPages (url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    pages = tree.xpath('//*[@class="pagination"]/li/a/@href')
    if len(tree.xpath('//*[@class="pagination"]/li')) > 11:
        # figure out how to deal with the long amount of pages where they show up as ellipses instead of the numbers
        del pages[len(pages) - 1]  # remove the "last page" link
        del pages[len(pages) - 1]  # remove the "next page" link

        page = requests.get(requests.compat.urljoin(url, pages[8]))
        tree = html.fromstring(page.content)
        pages2 = (tree.xpath('//*[@class="pagination"]/li/a/@href'))
        while pages2[0] != '#':
            del pages2[0]
        del pages2[0] # delete the # entry in pages2
        pages.extend(pages2)
    if len(pages) == 0:
        return 0
    if len(pages) > 1:
        del pages[len(pages)-1] # remove the "last page" link
        del pages[len(pages)-1] # remove the "next page" link
    return pages


# Add sorting algorithm that also removes duplicates
# Add function to search Spotify and get song lengths and genres

def checkDuplicates():
    # use enumerate instead of 2 for loops?
    for i in range(len(songDate)):
        for j in range(1, len(songDate)-1):
            if radioStation[i] == radioStation [j]:
                if songDate[i] == songDate[j]:
                    if songTimestamp[i] == songTimestamp[j]: # deleting the items changes the length of the array and ends up giving a "list index out of range" error
                        del radioStation[j]
                        del songDate[j]
                        del songTimestamp[j]
                        del songTitle[j]
                        del songArtist[j]

    return


def writeToCSV(file):
    with open(file, "a", encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for i in range(len(radioStation)):
            writer.writerow([radioStation[i], songDate[i], songTimestamp[i], songTitle[i], songArtist[i]])
    return


def main():
    t1=time.time()
    d = date.today()
    d -= timedelta(days=0)
    for i in range(31):  # It looks like KLBJ and Bob FM hold 30 days of broadcast history i.e. SET TO 31 TO GET ALL THE DATA
        print("Working on page: ",i)
        #KLBJ
        dayURL = 'http://www.klbjfm.com/broadcasthistory?date%5Bvalue%5D%5Bdate%5D=' + d.strftime('%m/%d/%Y')
        pages = getPages(dayURL)
        if pages != 0:
            songCollection(dayURL, getPages(dayURL), 'KLBJ', d)

        # BobFM
        dayURL = 'http://www.1035bobfm.com/broadcasthistory?date%5Bvalue%5D%5Bdate%5D=' + d.strftime('%m/%d/%Y')
        pages = getPages(dayURL)
        if pages != 0:
            songCollection(dayURL, getPages(dayURL), 'Bob FM', d)

        # 101X
        dayURL = 'http://www.101x.com/broadcasthistory?date%5Bvalue%5D%5Bdate%5D=' + d.strftime('%m/%d/%Y')
        pages = getPages(dayURL)
        if pages != 0:
            songCollection(dayURL, getPages(dayURL), '101X', d)

        # KUTX has similar but not exactly the same?

        d = d - timedelta(days=1)
    t2 = time.time()
    print(t2 - t1)
    print((t2 - t1)/60, " minutes")
    # printSongs()
    print(len(songTitle))


    # checkDuplicates()
    # print(len(songTitle))

    writeToCSV(date.today().strftime('%m%d%Y')+".csv")

    return


main()
