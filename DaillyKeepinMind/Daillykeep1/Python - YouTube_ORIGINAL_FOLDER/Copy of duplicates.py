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
from PyPDF2 import PdfFileWriter, PdfFileReader

import xlrd

from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait

import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'



coderlist=[]
with open("duplicatesanalysis.csv" , "r") as csvfile:
    datareader = csv.reader(csvfile)
    mylist=list(datareader)
##    mylist=sorted(mylist, key = lambda x: (x[1], x[2], x[4]))
codercol = mylist[0].index("codesheet")
columnheaders = mylist[0]
for i in range(len(mylist)-1):
    
    if mylist[i][1]==mylist[i+1][1] and mylist[i][2]==mylist[i+1][2] and mylist[i][4]==mylist[i+1][4]:
        codesheetstring = [str(mylist[i][codercol]) + " " + str(mylist[i+1][codercol])]            
        if codesheetstring not in coderlist:
            coderlist.append(codesheetstring)
##            print(mylist[i][len(mylist[i])-1])

##print(coderlist)

duplicatetally = []

duplicatetally.append(mylist[0])
j = 1
for row in coderlist:
    rowtoadd = []
    for index1 in range(codercol):
##        print(index1)
        rowtoadd.append(int(0))
    rowtoadd.append(row[0])
    for index2 in range(len(mylist[0])-codercol-1):
        rowtoadd.append(int(0))
    duplicatetally.append(rowtoadd)
##    print(len(duplicatetally[j]))
##    print(len(mylist[0]))
##    print(codercol)
##    print(duplicatetally[j].index(row[0]))
    j+=1

tallylist= []
for anotherrow in coderlist:
    tallylist.append([anotherrow[0],  0])
print(tallylist)

for i in range(len(mylist)-1):
    
    if mylist[i][1]==mylist[i+1][1] and mylist[i][2]==mylist[i+1][2] and mylist[i][4]==mylist[i+1][4]:
        codesheetstring = [str(mylist[i][codercol]) + " " + str(mylist[i+1][codercol])]
        coderow = coderlist.index(codesheetstring)+1
        tallylist[coderow-1][1]+=1
        for index3 in range(len(mylist[0])):
            if mylist[i][index3]!=mylist[i+1][index3]: ## and type(mylist[i][index3]) is int:
##                print(type(mylist[i][index3]))
##                print(index3)
                if type(duplicatetally[coderow][index3]) is int:
                    duplicatetally[coderow][index3]=duplicatetally[coderow][index3]+1

print(tallylist)

duplicatetallysecond = []
for i in range(len(duplicatetally)):
    duplicatetallysecondrow=[]
    for column in range(len(duplicatetally[i])):
        if type(duplicatetally[i][column]) is int:
            duplicatetallysecondrow.append(duplicatetally[i][column]/tallylist[i-1][1])
        else:
            duplicatetallysecondrow.append(duplicatetally[i][column])

    duplicatetallysecond.append(duplicatetallysecondrow)
        
        
with open("duplicates_report.csv", "w", newline="") as csvwritefile:
    datareader  = csv.writer(csvwritefile)
    for rowwriter in duplicatetally:
        datareader.writerow(rowwriter)

with open("duplicates_report2.csv", "w", newline="") as csvwritefile:
    datareader  = csv.writer(csvwritefile)
    for rowwriter in duplicatetallysecond:
        datareader.writerow(rowwriter)
