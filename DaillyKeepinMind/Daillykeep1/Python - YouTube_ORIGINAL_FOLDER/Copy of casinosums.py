##from bs4 import BeautifulSoup
##import urllib
##from urllib import request
##import re
##import csv
##import os.path
##import time
##import datetime
##import codecs
##import urllib.request
##import shutil
##import PyPDF2
####from pdfminer3k import PDFParser
##from PyPDF2 import PdfFileWriter, PdfFileReader
##
##import xlrd
import random
##
##from contextlib import closing
##from selenium.webdriver import Firefox # pip install selenium
##from selenium.webdriver.support.ui import WebDriverWait
##
##import http.client
##http.client.HTTPConnection._http_vsn = 10
##http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'


lensums = []
i = 0
while True:
    sums = 0
    i+=1
    draws = []
    while sums<1:
        draws.append(random.uniform(0,1))
        sums = sum(draws)
    lensums.append(len(draws))
    if i%100000==0:
        print(i)
        print("draws:", draws)
##        print "draws:"
        print("sum:", sums)
        print(sum(lensums)/len(lensums))
        
