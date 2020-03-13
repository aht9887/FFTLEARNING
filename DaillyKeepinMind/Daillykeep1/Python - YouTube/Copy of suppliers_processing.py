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

lineendings = ["|",
               "~",
               "'",
               '"',
               "^",
               "_"]

csvlist = [[]]
with(open("output_as_one_final.csv" )) as filename:
    contents = csv.reader(filename)
    row21 = []
    flag = ""
    supplymasterlist = []
    for row in contents:
        csvrowlist=[]
        supplyrowlist = []
        count = ""
        ticker = ""
        name = ""
        country = ""
        ticker = row[0].strip()
        if ticker == "":
            continue
        ticker = ticker.rstrip("_").strip()

        if ticker == "Ticke r":
            ticker = "Ticker"
        if ticker == "Ticker":
            csvlist.append(["", "", ""])
        else:
            count = ticker[0:ticker.find(")")].strip()
            ticker = ticker[ticker.find(")")+1:].strip()
        ticker_wo_country = ticker[0:-2].strip()
        if ticker_wo_country == ticker_wo_country.upper():
            ticker2 = "".join(ticker_wo_country.split())
##            if ticker2 != ticker_wo_country:
##                print(ticker_wo_country, ticker2)
            ticker = ticker2 + " " + ticker[-2:]
        name = row[1].strip()
        country = (row[2].strip())
        if country != "Country":
            country = country[0:2].upper()
        for element in lineendings:
            name = name.rstrip(element)
        csvlist.append([count, ticker, name, country])
##        if name!="":
##            if name[-1] == "1":
##                print(name, ticker, country)
##        if name == "--" or len(name)<3:
##            if country != "--" and country !="—" and country !="":
##                print(count,  ticker, name, country)
##                print(ticker)
##                print(name)
##                print(country)
##        if country == "":
##            if len(name)<3:
##                print(count, ticker, name, country)
        if count.strip() == "21":
            row21 = [count, ticker, name, country]
        elif ticker.upper().strip() == "TICKER":
            pass
        else:
            if count.upper()=="NO SUPPLIER":
                count = ""
                ticker = "no suppliers"
                name = "no suppliers"
                country = "no suppliers"
            else:
                if int(count)!=22 and int(count)!=int(supplymasterlist[-1][4])+1:
##                    print(count)
                    savedcount = count
                    flag = 1
                    continue
            if flag ==1:
##                print(count)
                if int(savedcount)+1!=int(count):
                    print(savedcount, count)
                    print(row21)
                    print(count, ticker, name, country)
                    print("This is a problem")
                flag = 0
            for entry in row21:
                supplyrowlist.append(entry)
            for entry in [count, ticker, name, country]:
                supplyrowlist.append(entry)
            supplymasterlist.append(supplyrowlist)
with(open("output_as_one_revised.csv", "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in csvlist:
        if row!=[]:
            spamwriter.writerow(row)
with(open("output_as_suppliers.csv", "w", newline="\n")) as filename:
    spamwriter = csv.writer(filename)
    for row in supplymasterlist:
        if row!=[]:
            spamwriter.writerow(row)



primaries = ["CMI US",
             "DE US",
             "CAT US",
             "HOG US",
             "IR US",
             "BC US"]

primaries_strings = ["Cummins",
                     "Deere",
                     "Caterpillar",
                     "HarleyDavidson",
                     "IngersollRand",
                     "Brunswick_parent_Mercury_Marine"]

for i in range(len(primaries)):
    supplierstosupplierslist = []
##    with(open("output_as_suppliers.csv")) as filename:
##        contents = csv.reader(filename)
    print(i)
    tickersearch = primaries[i]
    sheetname = primaries_strings[i]
    supplierstosupplierslist = []
    print(tickersearch)        
    for row in supplymasterlist:
        if row[1]==tickersearch:
            supplierstosupplierslist.append(row)
    supplierslist2 = [["focal_index", "focal_ticker", "focal_name","focal_country","supply_index","supply_ticker","supply_name","supply_country","supply_supplier_index","supply_supplier_ticker","supply_supplier_name","supply_supplier_country"]]
    for row in supplierstosupplierslist:
##            with(open("output_as_suppliers.csv")) as filename:
##                contents = csv.reader(filename)
        for row2 in supplymasterlist:
            addingrow = list(row)
            if row[5]==row2[1]:
                for rowitem in row2[4:8]:
                    addingrow.append(rowitem)
                supplierslist2.append(addingrow)
            
    with(open("%s.csv" %(sheetname), "w", newline="\n")) as filename2:
        spamwriter = csv.writer(filename2)
        for rowtowrite in supplierslist2:
            if rowtowrite!=[]:
                spamwriter.writerow(rowtowrite)

