#! /usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen

## URLS of the website to scrape
rcpURL_SENATE = "https://www.realclearpolitics.com/epolls/latest_polls/senate/"
rcpURL_HOUSE = "https://www.realclearpolitics.com/epolls/latest_polls/house/"

## function to prevent copy pasta of code
def make_csv(pageurl, fileName):
    ## Step 1.  Open the webPage for BeautifulSoup to parse
    ## urlopen is a function from the urlopen library
    webPage = urlopen(pageurl)

    ## open the webPage using BeautifulSoup using the lxml reader
    soup = BeautifulSoup(webPage,"lxml")

    ## open the output file (csv. for writing data to)
    out_file = open(fileName, "w")

    ## How the BeautifulSoup scrapes from the RCP website
    ## a. Grab all of the tables with class = None
    ##    These are the tables of the dates (ie: Monday January 1st)
    tables = soup.findAll('table', { "class" : None})
    ## b. Grab all of the tables with class = sortable
    ##    The sortable tables are all of the information for the CSV files
    sortables = soup.findAll('table', {"class": "sortable"})

    ## Write the header for the CSV file
    out_file.write("Date, Race, Poll, Results, Votes, Spread\n")

    ##  For each Table
    ##    Extract all of the date values
    ##    Extract all of the columns
    ##    For each race:
    ##      Get data in each column for output
    ##      Split the results column on ',' (can have 2-5+ candidates)
    ##      For each person in the results column:
    ##        Output everything to CSV.
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
    ## close the file
    out_file.close()

## Call the functions, give it the URL and the name of the output file.
make_csv(rcpURL_SENATE, "senate.csv")
make_csv(rcpURL_HOUSE, "house.csv")
