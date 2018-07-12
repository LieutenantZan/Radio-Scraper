from lxml import html
import requests

# KLBJ Info
page = requests.get('http://www.klbjfm.com/broadcasthistory')
# BobFM has the same structure as KLBJ, so put them in a function that cycles through the different pages

# print(page.text)
klbjtree = html.fromstring(page.content)

songDate = []
songTimestamp = []#klbjtree.xpath('//div[@class="views-field views-field-field-timestamp"]/div/span/text()')
# print(songTimestamp)

songTitle = []#klbjtree.xpath('//div[@class="views-field views-field-field-title"]/div/text()')
# print(songTitle)

songArtist = []#klbjtree.xpath('//div[@class="views-field views-field-field-artist"]/div/span/text()')
# print(songArtist)

# test = klbjtree.xpath('//*[@class="pagination"]/li[2]/a/@href')
test = klbjtree.xpath('//*[@class="pagination"]/li')
# print(test.findclass("next"))
hasNext = True
while hasNext:
    hasNext = False
    test = klbjtree.xpath('//*[@class="pagination"]/li')
    for i in range(len(klbjtree.xpath('//div[@class="views-field views-field-field-timestamp"]/div/span/text()'))):
        songDate.extend(klbjtree.xpath('//*[@class="broadcast-change-date"]/h1/text()'))
    songTimestamp.extend(klbjtree.xpath('//div[@class="views-field views-field-field-timestamp"]/div/span/text()'))
    songTitle.extend(klbjtree.xpath('//div[@class="views-field views-field-field-title"]/div/text()'))
    songArtist.extend(klbjtree.xpath('//div[@class="views-field views-field-field-artist"]/div/span/text()'))

    for i in range(len(test)):
        if test[i].get('class') == "next":
            hasNext = True

            link = klbjtree.xpath('//*[@class="pagination"]/li['+str(i+1)+']/a/@href')
            nextLink = 'http://www.klbjfm.com'+link[0]

            page = requests.get(nextLink)
            # print(page.text)
            klbjtree = html.fromstring(page.content)

            # print(nextLink)

print('done')

# for i in range(len(test)):
    # print(test[i].classes)

    # if test[i].text_content() == "{'class': 'next'}":
    #     print(i)
# print(len(songTitle))
for i in range(len(songTitle)):
    print("Date: ", songDate[i], "Timestamp: ", songTimestamp[i], "	Title: ", songTitle[i], "	Artist: ", songArtist[i])
    # print(i)
    i += 1

