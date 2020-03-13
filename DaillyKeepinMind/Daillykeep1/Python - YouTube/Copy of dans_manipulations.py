from bs4 import BeautifulSoup
import urllib
from urllib import request
import re
import csv
import os.path
import time
import datetime
import codecs
import urllib.request
import shutil
import PyPDF2
##from pdfminer3k import PDFParser

import xlrd

from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait




import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

listofcsvs = ["cat",
              "cerd",
              "cedaw",
              "crc",
              "iccpr",
              "icescr"]

for filetoopen in listofcsvs:
    csvlist = [["year", "country", "sign date" + "_" + str(filetoopen), "ratify date"+ "_" + str(filetoopen), "reservation_dummy"+ "_" + str(filetoopen), "signature_year"+ "_" + str(filetoopen), "ratification_year"+ "_" + str(filetoopen),"signature_timer"+ "_" + str(filetoopen), "ratification_timer"+ "_" + str(filetoopen), "ratification_dummy"+ "_" + str(filetoopen)]]
    with(open("%s.csv" %(filetoopen))) as filename:
        contents = csv.reader(filename)
        for row in contents:
            csvrowlist=[]
            signyear = "NA"
            ratifyyear = "NA"
            objections = 0
            signyearflag = False
            ratifyyearflag = False
            signyeardiff = "NA"
            ratifyyeardiff = "NA"
            ratifydummy=0
            if str(row[0].strip())[0:11] == "Participant":
                print(filetoopen)
                print(row)
            if row[0].strip()!="" and row[0].strip()[0:11]!="Participant":
                csvrowlist = []
                country = row[0].replace("\xa0", "").strip()
                signdate = row[1].replace("\xa0", "").strip()
                ratifydate = row[2].replace("\xa0", "").strip()
                while re.search("[0-9]$", country):
                    objections = 1
                    country = country[0:-1].strip().rstrip(",").strip().rstrip(",")
                if signdate != "":
                    signyearre = re.search("[0-9]{4}", signdate)
                    if signyearre:
                        signyear = signyearre.group(0)
                        signyearflag = True
                if ratifydate != "":
                    ratifyyearre = re.search("[0-9]{4}", ratifydate)
                    if ratifyyearre:
                        ratifyyear = ratifyyearre.group(0)
                        ratifyyearflag = True
                        ratifydummy=1

                for year in range(1949, 2014):
                    csvrowlist=[]
                    if signyearflag:
                        signyeardiff = year - int(signyear)
                    if ratifyyearflag:
                        ratifyyeardiff = year - int(ratifyyear)
                        if ratifyyeardiff<0:
                            ratifydummy=0
                        else:
                            ratifydummy=1
                    for thing in [year, country, signdate, ratifydate, objections, signyear,  ratifyyear, signyeardiff, ratifyyeardiff, ratifydummy]:
                        csvrowlist.append(thing)
                    csvlist.append(csvrowlist)
    with(open("%s_dan.csv" %(filetoopen), "w", newline="\n")) as filename:
        spamwriter = csv.writer(filename)
        for row in csvlist:
            if row!=[]:
                spamwriter.writerow(row)
        

csvlist = [["year", "country", "join date" + "_" + str("oecd"), str("oecd")+"_member"]]
with(open("oecd.csv")) as filename:
    contents = csv.reader(filename)
    for row in contents:
        csvrowlist=[]
        joinyear = "NA"
        objections = 0
        joinyearflag = False
        ratifyyearflag = False
        signyeardiff = "NA"
        ratifyyeardiff = "NA"
        ratifydummy=0
        joinyearflag2 = "problem"
        joinflag = "none"
        if row[0].strip()!="" and row[0].strip()[0:11]!="Participant":
            csvrowlist = []
            country = row[0].replace("\xa0", "").strip()
            if country == "Country":
                continue
            joindate = row[1].replace("\xa0", "").strip()
            if joindate != "":
                joinyearre = re.search("[0-9]{4}", joindate)
                if joinyearre:
                    joinyear = joinyearre.group(0)
                    joinyearflag = True
            for year in range(1949, 2014):
                csvrowlist=[]
                if joinyearflag:
                    if year <int(joinyear):
                        joinflag = 0
                    else:
                        joinflag = 1
                    joinyeardiff = year - int(joinyear)
                if ratifyyearflag:
                    ratifyyeardiff = year - int(ratifyyear)
                for thing in [year, country, joinyear, joinflag]:
                    csvrowlist.append(thing)
                csvlist.append(csvrowlist)
with(open("%s_dan.csv" %("oecd"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)



csvlist = [["year", "country", "join date" + "_" + str("nato"), str("nato")+"_member"]]
with(open("nato.txt")) as filename:
    contents = filename.readlines()
    i = 0
    for row in contents:
        csvrowlist=[]
        joinyear = "NA"
        objections = 0
        joinyearflag = False
        ratifyyearflag = False
        signyeardiff = "NA"
        ratifyyeardiff = "NA"
        ratifydummy=0
        joinyearflag2 = "problem"
        joinflag = "none"
        if row.strip()!="":
            csvrowlist = []
            if i<1:
                country = row.replace("\xa0", "").strip()
                i += 1
                continue
            else:
                joindate = row.replace("\xa0", "").strip()
                i = 0
            for year in range(1949, 2014):
                csvrowlist=[]
                if i==0:
                    if year <int(joindate):
                        joinflag = 0
                    else:
                        joinflag = 1
                    joinyeardiff = year - int(joindate)
                if ratifyyearflag:
                    ratifyyeardiff = year - int(ratifyyear)
                for thing in [year, country, joindate, joinflag]:
                    csvrowlist.append(thing)
                csvlist.append(csvrowlist)
with(open("%s_dan.csv" %("nato"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)

csvlist = [["year", "country", "join date" + "_" + str("un"), str("un")+"_member"]]
countrieslist_un = []
with(open("un2.txt")) as filename:
    contents = filename.readlines()
    i = 0
    for row in contents:
        csvrowlist=[]
        joinyear = "NA"
        objections = 0
        joinyearflag = False
        ratifyyearflag = False
        signyeardiff = "NA"
        ratifyyeardiff = "NA"
        ratifydummy=0
        joinyearflag2 = "problem"
        joinflag = "none"
##        print(row.strip())
        if row.strip()!="":
##            print(row.strip()[0:10])

##            print(row.strip())
            csvrowlist = []
##            print(i)
            if row.strip()[-7:]=="Members":
                i = 0
            if i<5:
                country = row.replace("\xa0", "").strip()
                if i==0:
                    joindate = country[0:4]
                i += 1
                if i==2:
                    countries = row.split(",")
##                    print(countries)
                    for country_element in countries:
                        if country_element.replace("[+]", "").strip() == "Yemen" and joindate=="1967":
                            countrieslist_un.append([joindate, "Democratic Yemen"])
                        else:
                            countrieslist_un.append([joindate, country_element.replace("[+]", "").strip()])
                    continue
                if row.strip()[0:10] == "Go back to":
                    i = 0
    for row in countrieslist_un:
        joindate = row[0]
        country = row[1]
        for year in range(1949, 2014):
            csvrowlist=[]
            if year<int(joindate):
                joinflag = 0
            else:
                joinflag = 1
            for thing in [year, country, joindate, joinflag]:
                csvrowlist.append(thing)
            csvlist.append(csvrowlist)

##    print(countrieslist_un)
with(open("%s_dan.csv" %("un"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)


csvlist = [["year", "country", "join date" + "_" + str("wto"), str("wto")+"_member"]]
countrieslist_un = []
with(open("wto.txt")) as filename:
    contents = filename.readlines()
    i = 0
    for row in contents:
        csvrowlist=[]
        joinyear = "NA"
        objections = 0
        joinyearflag = False
        ratifyyearflag = False
        signyeardiff = "NA"
        ratifyyeardiff = "NA"
        ratifydummy=0
        joinyearflag2 = "problem"
        joinflag = "none"
        date = ""
##        print(row.strip())
        if row.strip()!="":
            m = re.search("\d", row)
            if m:
                country = row[0:m.start()]
                date = row[m.start():]
                joinyearre = re.search("[0-9]{4}", date)
                if joinyearre:
                    joinyear = joinyearre.group(0)

            else:
                print("No digit in that string")
 
            csvrowlist = []
            for year in range(1949, 2014):
                csvrowlist=[]
                if year<int(joinyear):
                    joinflag = 0
                else:
                    joinflag = 1
                for thing in [year, country.strip(), joinyear, joinflag]:
                    csvrowlist.append(thing)
                csvlist.append(csvrowlist)

with(open("%s_dan.csv" %("wto"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)


csvlist = [["year", "country", "join date" + "_" + str("gatt"), str("gatt")+"_member"]]
countrieslist_un = []
with(open("gatt.txt")) as filename:
    contents = filename.readlines()
    i = 0
    for row in contents:
        csvrowlist=[]
        joinyear = "NA"
        objections = 0
        joinyearflag = False
        ratifyyearflag = False
        signyeardiff = "NA"
        ratifyyeardiff = "NA"
        ratifydummy=0
        joinyearflag2 = "problem"
        joinflag = "none"
        date = ""
##        print(row.strip())
        if row.strip()!="":
            m = re.search("\d", row)
            if m:
                country = row[0:m.start()]
                date = row[m.start():]
                joinyearre = re.search("[0-9]{4}", date)
                if joinyearre:
                    joinyear = joinyearre.group(0)

            else:
                print("No digit in that string")
 
            csvrowlist = []
            for year in range(1949, 2014):
                csvrowlist=[]
                if year<int(joinyear):
                    joinflag = 0
                else:
                    joinflag = 1
                for thing in [year, country.strip(), joinyear, joinflag]:
                    csvrowlist.append(thing)
                csvlist.append(csvrowlist)

with(open("%s_dan.csv" %("gatt"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)

csvlist = [["year", "cow", "country", "civilwar"]]
with(open("intrastatewardata_v4_1.csv")) as filename:
    contents = csv.reader(filename)
    for row in contents:
        csvrowlist=[]
        startyear=0
        endyear=0
        cow=0
        if row[10]!="-8" and row[10] != "StartYear1" and row[10]!="":
            startyear=int(row[10])
            endyear=int(row[13])
            if endyear==-7:
                endyear=2015
            cow = max(row[3], row[5])
            if cow == row[3]:
                country=row[4]
            else:
                country=row[6]
            if cow!="-8":
                for year in range(startyear, endyear+1):
                    csvrowlist=[year, cow, country, 1]
                    csvlist.append(csvrowlist)
        if row[16]!="-8" and row[16] != "StartYear2" and row[16]!="":
            startyear=int(row[16])
            endyear=int(row[19])
            if endyear==-7:
                endyear=2015
            cow = max(row[3], row[5])
            if cow == row[3]:
                country=row[4]
            else:
                country=row[6]

            if cow!="-8":
                for year in range(startyear, endyear+1):
                    csvrowlist=[year, cow, country, 1]
                    csvlist.append(csvrowlist)
            
with(open("%s_dan.csv" %("civilwar"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)



csvlist = [["year", "cow", "country", "iswar"]]
with(open("Inter-StateWarData_v4.0.csv")) as filename:
    contents = csv.reader(filename)
    for row in contents:
        csvrowlist=[]
        startyear=0
        endyear=0
        cow=0
        if row[8]!="-8" and row[8] != "StartYear1" and row[8]!="":
            startyear=int(row[8])
            endyear=int(row[11])
            if endyear==-7:
                endyear=2015
            cow = int(row[3])
            country = row[4]
            if cow!=-8:
                for year in range(startyear, endyear+1):
                    csvrowlist=[year, cow, country, 1]
                    csvlist.append(csvrowlist)
        if row[14]!="-8" and row[14] != "StartYear2" and row[14]!="":
            startyear=int(row[14])
            endyear=int(row[17])
            if endyear==-7:
                endyear=2015
            cow = int(row[3])
            if cow!=-8:
                for year in range(startyear, endyear+1):
                    csvrowlist=[year, cow,country,  1]
                    csvlist.append(csvrowlist)
            
with(open("%s_dan.csv" %("interstatewar"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)


csvlist = [["year", "cow", "country", "imports", "exports"]]
with(open("national_trade_3.0.csv")) as filename:
    contents = csv.reader(filename)
    for row in contents:
        if row[0]!="ccode":
            year = row[2]
            cow = row[0]
            country = row[1]
            imports = row[3]
            exports = row[4]
            if imports == "-9":
                imports = ""
            if exports == "-9":
                exports = ""
            csvrowlist=[year, cow, country, imports, exports]
            csvlist.append(csvrowlist)
            
with(open("%s_dan.csv" %("trade"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)

csvlist = [[]]
WDIkeeps = ["GDP per capita (constant 2005 US$)",
            "GDP per capita (current US$)"]
POPkeeps = ["Population, total"]

gdprowlist = []
poprowlist = []

gdplist = []
poplist = []

with(open("WDI_Data.csv")) as filename:
    contents = csv.reader(filename)
    for row in contents:
        csvrowlist=[]
        if row[0]=="Country Name":
            for indexno in range(0, 4):
                gdprowlist.append(row[indexno])
                poprowlist.append(row[indexno])

            for indexno in range(4,len(row)):
                gdprowlist.append("gdp"+str(row[indexno]))
                poprowlist.append("pop"+str(row[indexno]))

            gdplist.append(gdprowlist)
            poplist.append(poprowlist)

        elif row[2] in WDIkeeps:
            gdplist.append(row)
        elif row[2] in POPkeeps:
            poplist.append(row)

with(open("%s_dan.csv" %("gdp"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in gdplist:
        if row!=[]:
            spamwriter.writerow(row)
with(open("%s_dan.csv" %("pop"), "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in poplist:
        if row!=[]:
            spamwriter.writerow(row)

