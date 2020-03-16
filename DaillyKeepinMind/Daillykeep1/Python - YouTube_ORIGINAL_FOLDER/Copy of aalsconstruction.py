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

dirs = os.listdir()

toread = []

for item in dirs:
    if item.find(".csv")!=-1 and item.find("LawProf")!=-1:
        toread.append(item)

##print(toread)

towrite = []
towrite.append(["Name", "School", "Subject", "Years", "Page number", "Star", "Contains (S)"])

subjects = []
##subjects.append("FEDERAL COURTS")
with(open("%s.csv" %("listofsubjects"))) as filename:
    contents = csv.reader(filename)
    for row in contents:
        if row!=[]:
            if row[0].find("[")!=-1:
                rowreplace = row[0][row[0].find("]")+1:]
                subjects.append(rowreplace.lower().replace(" ", ""))

section = "section undefined"
yearsofservice = "years undefined"
pagenum = "pagenum not defined"
print(subjects)
##for elem in subjects:
##    print(elem)
##print(len(subjects))
for item in toread:
    with(open("%s" %(item))) as filename:
        contents = csv.reader(filename)
        rowindex = 0
        contentsrows = []
        for row in contents:
            if row != []:
                if len(row[0].strip())<9 and ("(S" in row[0] or "*" in row[0]):
                    contentsrows[-1][0] = contentsrows[-1][0]+row[0]
                else:
                    contentsrows.append(row)
        for row in contentsrows:
    ##        print(type(row))
    ##        print(row)
            if row == []:
                continue
            rowessence = row[0].lower().replace(" ", "")
            if row[0].strip()=="":
                continue
            if rowessence[0:7]=="lawteac":
                continue
            if rowessence[0:4]=="aals":
                continue
            if rowessence[0:8]=="cross-re":
                continue
            if rowessence[0:8]=="crossref":
                continue
            if rowessence[0:8]=="realprop":
                continue
            if rowessence[0:8]=="behavior":
                continue
            if rowessence[0:8]=="includes":
                continue
            if rowessence[0:8]=="anylawsu":
                continue
            if rowessence[0:8]=="alegalcl":
                continue
            if rowessence[0:8]=="pleading":
                continue
            if rowessence[0:8]=="leastone":
                continue
            if rowessence[0:8]=="referenc":
                continue
            if rowessence[0:8]=="emerging":
                continue
            if rowessence[0:8]=="includes":
                continue
            if rowessence[0:8]=="interest":
                continue
            if rowessence[0:8]=="listofla":
                continue
            if rowessence[0:8]=="andunive":
                continue
            restringvar1 = re.findall("[0-9]+", rowessence)
            if restringvar1!=[]:
                if restringvar1[0]==rowessence:
                    pagenum = rowessence
                    continue
            ith = False
            for elementofsubjects in subjects:
                if row[0].lower().replace(" ", "")[0:8] in elementofsubjects:
##                    print(row)
                    ith = True
                    if row[0]==row[0].upper():
                        newsection = row[0]
                    break
            if rowessence[0:8] == "onetofiv" or rowessence[0:8] == "sixtoten" or rowessence[0:8] == "overteny":
                yearsofservice = row[0]
                if rowessence[0:8] == "onetofiv":
                    section = newsection
                continue
            if ith:
                continue
            star="no"
            ess = "no"
            rowrevise = row[0].replace("„ ", ", ")
            rowrevise = rowrevise.replace(", NYLS", ", Nyls").replace(", LSU", "Lsu").replace("* LSU", "Lsu").replace(", UC", ", Uc").replace("U.C.L.A", "Ucla").replace(" '", "'").replace(" ’", "'").replace("’", "'")
            rowrevise = rowrevise.replace(" UC,", " Uc,").replace(" JAG", " Jag").replace("CUNY", "Cuny").replace("^", "").replace("K3N", "KEN").replace("K.an.", "Kan.").replace("Ml, ", "M., ")
            rowrevise = rowrevise.replace("U C L A", " Ucla").replace(",NYLS", ", Nyls").replace(" LSU", " Lsu").replace("‘", "").replace("tCan.", "Kan.").replace("K.y.", "Ky.").replace("DEFABRITnS", "DEFABRITIIS")
            rowrevise = rowrevise.replace("(S>", "(S)").replace("$", "S").replace("?", "*").replace("Uni v", "Univ").replace("'", "").replace("ofVa", "of Va").replace("of'Va", "of Va").replace("Ind.,I", "Ind., I")
            rowrevise = rowrevise.replace("ofNo", "of No").replace(":", ".").replace("Vanderbilt Legislation", "Vanderbilt").replace(", Ill,", ", III,").replace("IllLsu", "III, Lsu").replace("Chicago-Rent", "Chicago-Kent")
            rowrevise = rowrevise.replace("Southw estern", "Southwestern").replace("St. John s", "St. John's").replace("St. Mary s", "St. Mary's").replace("St. Johns", "St. John's").replace("St. Marys", "St. Mary's")
            if "*" in rowrevise:
                star = "yes"
            if "(S)" in rowrevise:
                ess = "yes"
            rowrevise = rowrevise.replace(" n,", " II,").replace("DePaui", "DePaul").replace("DePauI", "DePaul").replace("Perm State", "Penn State").replace(" m,", " III,").replace("End., Ind", "Ind., Ind").replace(" in,", " III,").replace(" ni,", " III,").replace(" lnd.", "Ind.").replace("JagDEEP", "JAGDEEP").replace("JefTer", "Jeffer")
            rowrevise = rowrevise.replace("W. Va.", "West Virginia").replace("Washbum", "Washburn").replace("ofFlorida", "of Florida").replace("Wash, Seattle", "Wash., Seattle").replace("St.-Louis", "St. Louis").replace("Vi llano va", "Villanova").replace("ofAriz", "of Ariz")
            rowrevise = rowrevise.replace("•", "").replace("!", "l").replace("Clara Trade Regulation", "Clara").replace("(S)", "").replace("*","")
            rowrevise = rowrevise.replace("„ ", ", ").replace(";", ",").replace("Adz. State", "Ariz. State").replace(" .", "").strip()
            rowrevise = rowrevise.replace("1", "I")
            if rowrevise !="":
                ur = rowrevise[-1].upper()
                lr = rowrevise[-1].lower()

                if ur == lr:
                    rowrevise = rowrevise[0:-1].strip()
            
            restringvar = re.findall("[A-Z1 \( \)\“\” \)„ \* \'\`\’,-\.]+", rowrevise)
    ##        print(restringvar)
            if restringvar==[]:
                continue
##            if int(pagenum)>1588 and int(pagenum)<1598:
##                print(rowrevise)
##                print(section)
##                print(yearsofservice)
##                print(newsection)
##                print(pagenum)
##                print("\n\n\n")
            if any(char.isdigit() for char in rowrevise):
                print(rowrevise)
    ##        print(restringvar[0])
    ##        print(str(row[0])[0:len(restringvar[0])-1], "                         ", str(row[0])[len(restringvar[0])-1:])
            towrite.append([rowrevise[0:len(restringvar[0])-1].replace("1", "I"), rowrevise[len(restringvar[0])-1:], section, yearsofservice, pagenum, star, ess])

with open("outputfile.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(towrite)

for rowrow in towrite:
    restringvar1 = re.findall("[0-9]+", rowrow[0])
    if restringvar1!=[]:
        print(rowrow[0])
