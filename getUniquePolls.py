#! /usr/bin/env python3
import csv

polls = []

def getPolls(fileName):
    with open(fileName, 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, delimiter=',')
        if has_header:
            next(reader)
        for row in reader:
            polls.append(row[2])

getPolls("senate.csv")
getPolls("house.csv")

outFile = open("pollnames.csv","w")
outFile.write("Poll\n")
for poll in sorted(set(polls)):
    outFile.write(poll + "\n")
outFile.close
