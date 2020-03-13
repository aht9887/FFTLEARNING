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


mode = input("Enter 1 or read for downloading, enter 2 or write for compiling spreadsheets:")

if str(mode).lower() == "read" or str(mode).lower() == "1":
    method = "download"
else:
    method = "analyze"


##
##data = urllib.request.urlopen("https://www.tcsheriff.org/inmate-jail-info/ice-listing")
##
##datastring = data.read()
##
##soup = BeautifulSoup(datastring, "html.parser")
##
######print(soup.get_text())

url = "https://www.tcsheriff.org/inmate-jail-info/ice-listing"

if method == "download":

    # use firefox to get page with javascript generated content
    with closing(Firefox()) as browser:
         browser.get(url)
    ##     button = browser.find_element_by_name('.pdf')
    ##     button.click()
         # wait for the page to load
         WebDriverWait(browser, timeout=10) ##.until(
    ##         lambda x: x.find_element_by_id('.pdf'))
         # store it to string variable
         page_source = browser.page_source
    soup = BeautifulSoup(page_source, "html.parser")


    ##print(soup.get_text())

    pdflist= []

    docnamelist = []

    pdfs = soup.find_all("a")

    for possibility in pdfs:
    ##    print(possibility)
        linktext = possibility.get("href")
        try:
    ##        print(linktext)
            test=linktext[-4:]
            if test == ".pdf":
                pdflist.append(linktext)
        except TypeError:
            pass

    ##print(pdflist)

    skipped_docs = 0
    for doc in pdflist:
##        print(doc)
        docname  = doc[-23:]
##        print(docname)
        docnamelist.append(docname)
        if not os.path.exists("%s" %(docname)):
            print("adding %s to folder" %(docname))
##            print("https://sheriff.traviscountytx.gov%s" %(doc))
            with urllib.request.urlopen("https://www.tcsheriff.org%s" %(doc)) as response, open(docname, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        else:
            skipped_docs = skipped_docs + 1

    print("Skipped %d documents, already downloaded" %(skipped_docs))

    print("Now convert all .pdf to .xlsx before running next step")

####for name in docnamelist:
######    print("%s" %(name))
####    with open("%s" %(name)) as f:
####        now = PyPDF2.PdfFileReader(name)
######        print(now)
######        print("in here")
####        pages = now.getNumPages()
####        for page in range(pages):
####            extractthispage = now.getPage(page)
######            print(extractthispage.extractText()) 
####            print(extractthispage.getContents()) 
####

if method == "analyze":
    excelfiles = []
    dirs = os.listdir()

    for filename in dirs:
        if re.search("^excel_", filename)!=None:
            excelfiles.append(filename)
    listoflists = []
    for exclfil in excelfiles:
        date = str(exclfil)[6:16]
        listoflists.append(["here is the date", date])
        workbook = xlrd.open_workbook(exclfil)
        worksheet = workbook.sheet_by_index(0)
        numrows = worksheet.nrows
        numcols = worksheet.ncols
        for curr_row in range(numrows):
            rowxlrd = worksheet.row(curr_row)
            rowpy = []
            for curr_cell in rowxlrd:
                appender = str(curr_cell).split(":")[1]
                if str(curr_cell).split(":")[0] == "xldate":
                    dateincellstep1 = xlrd.xldate_as_tuple(float(str(curr_cell).split(":")[1]), workbook.datemode)
##                    print(dateincellstep1)
                    appender = str(dateincellstep1[1]) + "/" + str(dateincellstep1[2]) + "/" + str(dateincellstep1[0])
##                    print(appender)
                if len(str(curr_cell).split(":"))>2:
                    for k in range(len(str(curr_cell).split(":"))):
                        if k>1:
                            appender = appender + ":" + str(curr_cell).split(":")[k]
                appender = appender.replace("\\xa0", " ")
                appender = appender.replace("\\n", " ")
                if appender != "''":
##                    appender = "  ".join(appender.split("  "))
##                    appender = appender.split("  ")
##                    for item in appender:
                    rowpy.append(appender)

##                if appender.find("Charge Disposition Type")>-1:
##                    listoflists.append(["NEW RECORD"])
            listoflists.append(rowpy)
##        if excelfiles.index(exclfil) == 3:
##            print(listoflists)
        listoflists.append(["end of excel file"])
    listoflistsrevise = []
    inserter = []

    for rowrevise in listoflists:
        rowtoappend = []
        fffflag = 0
        for cellrevise in rowrevise:
            cellreviseaftersplit = cellrevise.replace("'Level'", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("'Sentence'", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("'Charge Disposition Type'", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("'Charge Literal'", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("'Charge'", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("'Disposition_Date'", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Level", " ")
            if cellreviseaftersplit.find("Sentenced")==-1:
                cellreviseaftersplit = cellreviseaftersplit.replace("Sentence", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Charge Disposition Type", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Charge Literal", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Charge", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Disposition_Date", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Booking_No", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Booking_Name", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Disposition Date", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Disposition Type", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Booking No", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Booking Name", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Race", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Sex", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Date_of_Birth", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Booking_Date", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Date of Birth", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Booking Date", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Place of Birth", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("Sentenced: ", " ")
            cellreviseaftersplit = cellreviseaftersplit.replace("'", "")
            cellreviseaftersplit = cellreviseaftersplit.replace('"', '')
            if re.match("^Mexico \(Use only[ ]?$", cellreviseaftersplit.strip()):
##                print("HEY!\n\n\n\n\n\n\n\n\n\n")
                cellreviseaftersplit = "Mexico (Use only when state is unknown)"
            cellreviseaftersplit = cellreviseaftersplit.strip()
            cellreviseaftersplit = re.split('  +', cellreviseaftersplit)
            for item in cellreviseaftersplit:
                if item != "":
                    rowtoappend.append(item)
        if rowtoappend != []:
            if str(rowtoappend[0]) == "end of excel file":
                inserter = []
                fffflag = 1
        if len(rowtoappend)>1:
            if str(rowtoappend[0])[0]=="1" and (len(str(rowtoappend[0]).strip())==9 or len(str(rowtoappend[0]).strip())==7) and str(rowtoappend[1]).find(",")>0:
##                listoflistsrevise.append(["NEW RECORD"])
                inserter = rowtoappend
                fffflag = 1
            elif re.match("^Date:",  rowtoappend[0]) and re.match("^Time:", rowtoappend[1]):
                fffflag = 1

            else:
                fffflag = 0
                for inserterindex in range(len(inserter)):
                    rowtoappend.insert(inserterindex, inserter[inserterindex])
        if rowtoappend != [] and fffflag == 0:
            listoflistsrevise.append(rowtoappend)
    listoflists2 = []
    listoflists2.append(["Date", "Booking_No", "Booking_Name", "Race", "Sex", "Date_of_Birth", "Booking_Date", "Place_of_Birth", "Charge", "Charge Literal", "Level", "Sentence", "Disposition_Date", "Disposition_Type"])
    date = ""
    dateedit2 = "01/01/1992"
    intromaterial = ["This is a list of all inmates",
                     "on the first page of this",
                     "listed on the first",
                     "Place of birth is self",
                     "In Custody Inmates",
                     "Travis County Sheriffs Office",
                     "=====>",
                     "the first page of this",
                     "page of this",
                     "^when state is$",
                     "^unknown\)$"]
    for rowrevise2 in listoflistsrevise:
        if re.match("^here is the date", rowrevise2[0]):
##            dateedit = rowrevise2[0].replace("Report Generated:", "").strip()
##            dateedit2 = dateedit[0:dateedit.find(" ")]
            dateedit2 = rowrevise2[1]
##        elif re.match("^Date: ", rowrevise2[0]):
##            dateedit = rowrevise2[0].replace("Date: ", "").strip()
##            dateedit2 = dateedit
        rowappend = []
        flag = 0
        for introcheck in intromaterial:
            if re.match(introcheck, rowrevise2[0]) or re.match("^Report Generated", rowrevise2[0]) or re.match("^Date: ", rowrevise2[0]) or re.match("^here is the date", rowrevise2[0]):
                flag = 1
        if flag !=1:
            rowrevise2.insert(0, dateedit2)
            listoflists2.append(rowrevise2)
    i = 0
    flag = "flag"
    for rowrevise3 in listoflists2:
        flag = "flag"
        iteration = 0
        if i >0:
            while flag == "flag":

                if re.match("^[0-9]+-[0-9]+-[0-9]+$", rowrevise3[0]) or rowrevise3[0]=="error, inserting blank space":
                    flag = "no flag"
                else:
##                    print(rowrevise3[0])
                    rowrevise3.insert(0, "error, inserting blank space")
                    flag = "flag"
                if re.match("^1[0-9]+\.?[0-9]?$", rowrevise3[1]) or rowrevise3[1]=="error, inserting blank space":
                    flag = "no flag"
                else:
##                    print(rowrevise3[1])
                    rowrevise3.insert(1, "error, inserting blank space")
                    flag = "flag"
                if re.match("^[A-Z ]+ *-?[A-Z ]+ *, ?[A-Z ]+ *-?[A-Z ]+ *$", rowrevise3[2]) or rowrevise3[2]=="error, inserting blank space":
                    flag = "no flag"
                else:
##                    print(rowrevise3[2])
                    rowrevise3.insert(2, "error, inserting blank space")
                    flag = "flag"


                if iteration >0:
                    pass
##                    print("end of while loop %f" %(iteration))
                iteration = iteration + 1
##        print(rowrevise3[2])

        i = i+1

    for rowrevise3 in listoflists2:
        if len(rowrevise3)<10:
            pass
        else:
            if len(rowrevise3)==10:
                rowrevise3.insert(10, rowrevise3[9][-2:])
##                print(rowrevise3)
            elif len(rowrevise3[10])==2:
                pass
            else:
                flag_twochar = 0
                rowelemtokeep = ""
                rowelemtodelete = ""
                for rowelem in rowrevise3[9:]:
                    if len(rowelem)==4 and re.match("^[\(]..[\)]", rowelem):
                        rowelemtodelete = rowelem
                if rowelemtodelete != "":
##                    print(rowrevise3)
                    rowrevise3.remove(rowelemtodelete)
##                    print(rowrevise3)
                for rowelem in rowrevise3[9:]:
                    if len(rowelem)==2 and rowrevise3.index(rowelem)!=10:
                        flag_twochar = 1
                        rowelemtokeep = rowelem
                if flag_twochar ==1:
                    rowrevise3.insert(10, rowelemtokeep)
##                    print(rowrevise3)
                




    with open("outputfile.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(listoflists2)
