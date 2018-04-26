#! /usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen

rcpURL_SENATE = "https://www.realclearpolitics.com/epolls/latest_polls/senate/"
rcpURL_HOUSE = "https://www.realclearpolitics.com/epolls/latest_polls/house/"

def make_csv(pageurl, fileName):
    webPage = urlopen(pageurl)

    soup = BeautifulSoup(webPage,"lxml")

    out_file = open(fileName, "w")
    tables = soup.findAll('table', { "class" : None})
    sortables = soup.findAll('table', {"class": "sortable"})
    out_file.write("Date, Race, Poll, Results, Votes, Spread\n")
    for i in range(0,len(tables)):
        date = tables[i].find('td', { "class" : "date" })
        races = sortables[i].findAll('td', { "class" : "lp-race" })
        polls = sortables[i].findAll('td', { "class" : "lp-poll" })
        results = sortables[i].findAll('td', { "class" : "lp-results" })
        spread = sortables[i].findAll('td', { "class" : "lp-spread" })
        for i in range(0,len(races)):
            da = date.find('b').contents[0].replace(',','')
            ra = races[i].find('a').contents[0]
            po = polls[i].find('a').contents[0]
            re = results[i].find('a').contents[0].split(',')
            sp = spread[i].find('span').contents[0]
            for r in re:
                out_file.write(da + ',' + ra + ',' + po + ',' + r.lstrip().replace(' ',',') + ',' + sp + '\n')
    out_file.close()

make_csv(rcpURL_SENATE, "senate.csv")
make_csv(rcpURL_HOUSE, "house.csv")
