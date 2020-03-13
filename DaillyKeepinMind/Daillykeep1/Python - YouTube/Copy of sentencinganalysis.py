from bs4 import BeautifulSoup
import urllib
from urllib import request
import re
import csv
import os.path
import time
from ftfy import fix_text

year = ["2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004"]
year = ["2015"]
amendments_list = []

amendments_list.append(["amendment number", "section", "year", "amendment or original"])

for j in range(len(year)):
    if int(year[j])>=2014:
        URLs = ["1", "2-c", "2-d", "2-e-k", "2-l-x", "3", "4", "5", "6", "7", "8"]
    elif int(year[j])<2014:
        URLs = ["1", "2a-c", "2d", "2e-k", "2l-x", "3", "4", "5", "6", "7", "8"]
    for i in range(len(URLs)):
        print(URLs[i])
        print(year[j])
        if int(year[j])>=2014:
            data = urllib.request.urlopen("http://www.ussc.gov/guidelines-manual/%s/%s-chapter-%s" %(year[j], year[j], URLs[i]))
        elif int(year[j])<2014:
            data = urllib.request.urlopen("http://www.ussc.gov/guidelines-manual/%s/%s-chapter%s" %(year[j], year[j], URLs[i]))
        datastring = data.read()
        datastring = datastring.decode('utf-8')
        datastring = datastring.replace("\xa0", " ")
        datastring = datastring.replace("\u25cf", "")
        datastring = datastring.replace("\u2010", "-")
        datastring = datastring.replace("Â", " ")
        datastring = datastring.replace("\u2011", "-")
        datastring = datastring.replace("\n", " ")
        datastring = " ".join(datastring.split())
    ##    datastring = datastring.replace("><", "> <")
        datastring = datastring.replace("</strong> <strong>", " ")
        datastring = datastring.replace("</strong><strong>", "")
        datastring = datastring.replace("<strong></strong>", "")
        datastring = datastring.replace("</u> <u>", " ")
        datastring = datastring.replace("</u><u>", "")
        datastring = datastring.replace("<strong><p>", "<p><strong>")
        datastring = datastring.replace("</p></strong>", "</strong></p>")
    ##    datastring = datastring.replace("* * * * *", "BREAKBREAKBREAK")
        datastring = datastring.replace('<br /><p class="style6">* * * * *</p>', "")
        datastring = datastring.replace('* * * * *', "")
        datastring = datastring.replace(".</p><p", ".</p> <p")
        datastring = " ".join(datastring.split())
##        datastring = fix_text(datastring)
        datastring = " ".join(datastring.split())
        datastring = datastring.replace("</strong> <strong>", " ")
        datastring = datastring.replace("</u></strong><strong><u>", "")
        datastring = datastring.replace("</u></strong><u>", "<strong>")
        datastring = datastring.replace("</strong>)</u>", ")</strong></u>")
        datastring = datastring.replace("</br> </br><u>Historical", "</p> <p><u>Historical")
##        datastring = datastring.replace("<br/> <br /><u>Historical", "</p> <p><u>Historical")
        datastring = datastring.replace("<br /> <br /><u>Historical", "</p> <p><u>Historical")
        datastring = datastring.replace("</u> <u>", " ")
        datastring = " ".join(datastring.split())
        datastring = datastring.replace("</strong> <strong>", " ")
        datastring = datastring.replace("</u> <u>", " ")
        datastring = datastring.replace("</p><p>", "</p> <p>")
        datastring = " ".join(datastring.split())
        datastring = datastring.replace("</u></strong><u> </u><strong><u>", " ")
        datastring = datastring.replace("</u> <u>", " ")
        datastring = " ".join(datastring.split())
        

        
        
        soup = BeautifulSoup(datastring, "html5lib")

        souptext = soup.prettify()

        if int(year[j])==2010:
            main_div = soup.find("div", id="content")
        else: ##if int(year[j])>2010:
            main_div = soup.find("div", id="main")

        checklist_strong = main_div.find_all(["strong", "h2"])
    ##    print(checklist_strong,"\n\n\n\n\n\n\n\n\n\n")
        checklist_h2 = main_div.find_all("h2")
    ##    print(checklist_h2, "\n\n\n\n\n\n\n\n\n\n")
        checklist_stronger = main_div.find_all("u")
        
        checklist_strongest = []
        for entry in checklist_strong:
            restr = str(entry)
            gttxt = entry.get_text()
    ##        if gttxt == gttxt.upper():
    ##            print(gttxt)
            
            if re.search('^§[0-9][A-Z][0-9]\.[0-9]', gttxt) or entry in checklist_h2 or (re.search('^[0-9]\.', gttxt) and gttxt==gttxt.upper()):
                checklist_strongest.append(entry)
    ##            print(gttxt)
        checklist_strong = checklist_strongest
    ##    print(checklist_strong)
        checklist_u = main_div.find_all("u")
        checklist_p = main_div.find_all(["p", "table"])
        checklist_appnote = main_div.find_all("u", text=re.compile("Application Note"))
        checklist_hist = main_div.find_all("u", text=re.compile("Historical Note"))
        checklist_back = main_div.find_all("u", text=re.compile("Background"))
    ##    print(checklist_hist)
    ##    print(checklist_back)
    ##    print(checklist_appnote)

        

                                        


    ##    print(main_div("strong"))
    ##    print(main_div("u"))
    ##    print(main_div("p"))
        rowtowrite=[]
        rowtowrite2=[]
        rowtowrite.append(["section", "guidelines", "statutory provisions", "commentary", "application note", "background", "historical note"])
        rowtowrite2.append(["section", "guidelines", "base offense level", "specific offense characteristics", "cross reference", "special instructions", "commentary", "statutory provisions", "application note", "background", "historical note", "guidelines WC", "commentary WC", "application note WC", "background WC", "historical note WC", "statutory provisions WC", "guidelines CC", "commentary CC", "application note CC", "background CC", "historical note CC", "statutory provisions CC", "inccount", "dec count", "parens start count", "max offense level", "first offense level", "max adjustment", "first adjustment", "base offense word count", "specific characteristics word count", "cross ref word count", "spec instr word count", "base offense cc", "specific offense cc", "cross ref cc", "spec instr cc"])
        wordcount = 0
        charcount = 0
        textcheck = ""
        maindivwdct = [""]
        runlen = 0
        runlen2 = 0


        for elem in checklist_strong:
            guidelines=[]
            histnote=[]
            applnote=[]
            backgrd=[]
            commntry=[]
            statprov=[]
    ##        print("beginning new element")
    ##        print(elem.parent)
            hstflg = -1
            apntflg = -1
            bkgrdflg = -1
            stprvflg = -1
            cmmflg = -1

            base_off_flag = 0
            spec_char_flag = 0
            cross_ref_flag = 0
            spec_instr_flag = 0

            base_off = []
            off_levels_source = " "
            adjust_source = " "
            spec_char = []
            cross_ref = []
            spec_instr = []
            marker = ""


            cleanelem = elem.get_text()
            cleanelem = str(cleanelem)
            cleanelem = cleanelem.strip()
            cleanelem = " ".join(cleanelem.split())
            
            maindivwdct.append(cleanelem)
            

    ## MASTER for loop
            for elmnt in elem.next_elements:
                elmntstr = str(elmnt)
                histnoteflag = elmntstr.find("<u>Historical Note")
                appnoteflag = elmntstr.find("<u>Application Note")
                backgrdflag = elmntstr.find("<u>Background")
                statprovflag = elmntstr.find("<u>Statutory Provision")
                commflag = max(elmntstr.find('<p class="style3">Commentary'), elmntstr.find('<p class="style3">Introductory Commentary'))

                if histnoteflag !=-1:
                    hstflg = -1
                    apntflg = -1
                    bkgrdflg = -1
                    stprvflg = -1
                    cmmflg = -1
                    hstflg = histnoteflag
                if appnoteflag !=-1:
                    hstflg = -1
                    apntflg = -1
                    bkgrdflg = -1
                    stprvflg = -1
                    cmmflg = -1
                    apntflg = appnoteflag
                if backgrdflag !=-1:
                    hstflg = -1
                    apntflg = -1
                    bkgrdflg = -1
                    stprvflg = -1
                    cmmflg = -1
                    bkgrdflg = backgrdflag
                if statprovflag !=-1:
                    hstflg = -1
                    apntflg = -1
                    bkgrdflg = -1
                    stprvflg = -1
                    cmmflg = -1
                    stprvflg = statprovflag
                if commflag !=-1:
                    hstflg = -1
                    apntflg = -1
                    bkgrdflg = -1
                    stprvflg = -1
                    cmmflg = -1
                    cmmflg = commflag


                            

                if (re.search('^[0-9]\.', gttxt) and gttxt==gttxt.upper()):
                    break
                if elmntstr.find("BREAKBREAKBREAK") != -1:
                    break
                if elmnt in checklist_strong and elmnt != elem:
                    break
                if elmnt in checklist_p and elmnt not in checklist_strong: ##elmntstr.find("strong")==-1:
                    if elmntstr!=[] and re.match('^<p><strong>§[0-9][A-Z][0-9]\.[0-9]', elmntstr)==None:
                        if elmnt.get_text()==elmnt.get_text().upper() and re.search('^[0-9]\.', elmnt.get_text()):
                            break
                        if hstflg!=-1:
                            histnote.append(elmnt.get_text())
                        elif apntflg !=-1:
                            applnote.append(elmnt.get_text())
                        elif bkgrdflg!=-1:
                            backgrd.append(elmnt.get_text())
                        elif cmmflg!=-1:
                            commntry.append(elmnt.get_text())
                        elif stprvflg!=-1:
                            statprov.append(elmnt.get_text())
                        else:
                            guidelines.append(elmnt.get_text())
                            gline = elmnt.get_text()
                            if marker != "":
                                if chr(ord(marker)+1) == gline[1]:
                                    base_off_flag = 0
                                    spec_char_flag = 0
                                    cross_ref_flag = 0
                                    spec_instr_flag = 0
                            if (re.match("^\(.\) Base Offense Level", gline)):
                                base_off_flag = 5
                                spec_char_flag = 0
                                cross_ref_flag = 0
                                spec_instr_flag = 0
                                marker = gline[1]
                            if (re.match("^\(.\) Specific Offense Characteristic", gline)):
                                base_off_flag = 0
                                spec_char_flag = 5
                                cross_ref_flag = 0
                                spec_instr_flag = 0
                                marker = gline[1]
                            if (re.match("^\(.\) Cross Reference", gline)):
                                base_off_flag = 0
                                spec_char_flag = 0
                                cross_ref_flag = 5
                                spec_instr_flag = 0
                                marker = gline[1]
                            if (re.match("^\(.\) Special Instruction", gline)):
                                base_off_flag = 0
                                spec_char_flag = 0
                                cross_ref_flag = 0
                                spec_instr_flag = 5
                                marker = gline[1]
                            if base_off_flag>0:
                                base_off.append(gline)
                                off_levels_source = off_levels_source + " " + (str(elmnt))
                            elif spec_char_flag>0:
                                spec_char.append(gline)
                                adjust_source = adjust_source + " " + str(elmnt)
                            elif cross_ref_flag>0:
                                cross_ref.append(gline)
                            elif spec_instr_flag>0:
                                spec_instr.append(gline)
                        maindivwdct.append(elmnt.get_text())
                    

    ##
    ##
    ##        
    #### guidelines for loop
    ##        for elmnt in elem.next_elements:
    ##            elmntstr = str(elmnt)
    ####            print("elem is", elem)
    ####            print("elmnt is", elmnt)
    ####            print("\n\n\n\n\n\n")
    ####            time.sleep(5)
    ##            histnoteflag = elmntstr.find("<u>Historical Note")
    ##            appnoteflag = elmntstr.find("<u>Application Note")
    ##            backgrdflag = elmntstr.find("<u>Background")
    ##            statprovflag = elmntstr.find("<u>Statutory Provision")
    ##            commflag = max(elmntstr.find('<p class="style3">Commentary'), elmntstr.find('<p class="style3">Introductory Commentary'))
    ####            print(elem, "that was elem", elmntstr, "that was elmntstr")
    ####            inchstr = (elmnt in checklist_strong)
    ####            print(inchstr)
    ####            print("\n\n\n\n\n")
    ####            time.sleep(1)
    ##            if (re.search('^[0-9]\.', gttxt) and gttxt==gttxt.upper()):
    ##                break
    ##            if elmntstr.find("BREAKBREAKBREAK") != -1:
    ##                break
    ##            if elmnt in checklist_strong and elmnt != elem:
    ##                break
    ##            if elmnt in checklist_p and elmnt not in checklist_strong: ##elmntstr.find("strong")==-1:
    ##                if [-1, -1, -1, -1, -1] != [commflag, histnoteflag, appnoteflag, backgrdflag, statprovflag]:
    ##                    break
    ##                elif elmnt.get_text()==elmnt.get_text().upper() and re.search('^[0-9]\.', elmnt.get_text()):
    ##                    break
    ##                else:
    ##                    if elmntstr!=[] and re.match('^<p><strong>§[0-9][A-Z][0-9]\.[0-9]', elmntstr)==None:                        
    ##                        guidelines.append(elmnt.get_text())
    ####                        print(elmnt.get_text())
    ####                        print(fix_text(elmnt.get_text()))
    ####                        print("\n")
    #### histnote for loop
    ##        hflgs = []
    ##        for elmnt in elem.next_elements:
    ##            elmntstr = str(elmnt)
    ##            histnoteflag = elmntstr.find("<u>Historical Note")
    ##            if histnoteflag>-1:
    ##                histnoteflag =2
    ##            hflgs.append(histnoteflag)
    ##            appnoteflag = elmntstr.find("<u>Application Note")
    ##            statprovflag = elmntstr.find("<u>Statutory Provision")
    ##            backgrdflag = elmntstr.find("<u>Background")
    ##            commflag = max(elmntstr.find('<p class="style3">Commentary'), elmntstr.find('<p class="style3">Introductory Commentary'))
    ##            if (re.search('^[0-9]\.', gttxt) and gttxt==gttxt.upper()):
    ##                break
    ##            if elmntstr.find("BREAKBREAKBREAK") != -1:
    ##                break
    ##            if elmnt in checklist_strong and elmnt != elem:
    ##                break
    ##            if elmnt in checklist_p and elmnt not in checklist_strong: ##elmntstr.find("strong")==-1:
    ##                if 2 in hflgs:
    ##                    if elmntstr!=[] and re.match('^<p><strong>§[0-9][A-Z][0-9]\.[0-9]', elmntstr)==None:
    ##                        if [-1, -1, -1, -1] != [commflag, appnoteflag, backgrdflag, statprovflag]:
    ##                            break
    ##                        elif elmnt.get_text()==elmnt.get_text().upper() and re.search('^[0-9]\.', elmnt.get_text()):
    ##                            break
    ##                        histnote.append(elmnt.get_text())
    ##                        
    #### appnote for loop
    ##        aflgs = []
    ##        for elmnt in elem.next_elements:
    ##            elmntstr = str(elmnt)
    ##            histnoteflag = elmntstr.find("<u>Historical Note")
    ##            appnoteflag = elmntstr.find("<u>Application Note")
    ##            statprovflag = elmntstr.find("<u>Statutory Provision")
    ##            if appnoteflag>-1:
    ##                appnoteflag =2
    ##            aflgs.append(appnoteflag)
    ##
    ##            backgrdflag = elmntstr.find("<u>Background")
    ##            commflag = max(elmntstr.find('<p class="style3">Commentary'), elmntstr.find('<p class="style3">Introductory Commentary'))
    ##            if (re.search('^[0-9]\.', gttxt) and gttxt==gttxt.upper()):
    ##                break
    ##            if elmntstr.find("BREAKBREAKBREAK") != -1:
    ##                break
    ##            if elmnt in checklist_strong and elmnt != elem:
    ##                break
    ##            if elmnt in checklist_p and elmnt not in checklist_strong: ##elmntstr.find("strong")==-1:
    ##                if 2 in aflgs:
    ##                    if elmntstr!=[] and re.match('^<p><strong>§[0-9][A-Z][0-9].[0-9]', elmntstr)==None:
    ##                        if [-1, -1, -1, -1] != [commflag, histnoteflag, backgrdflag, statprovflag]:
    ##                            break
    ##                        elif elmnt.get_text()==elmnt.get_text().upper() and re.search('^[0-9]\.', elmnt.get_text()):
    ##                            break
    ##                        applnote.append(elmnt.get_text())
    ##
    #### backnote for loop
    ##        bflgs = []
    ##        for elmnt in elem.next_elements:
    ##            elmntstr = str(elmnt)
    ##            histnoteflag = elmntstr.find("<u>Historical Note")
    ##            appnoteflag = elmntstr.find("<u>Application Note")
    ##            backgrdflag = elmntstr.find("<u>Background")
    ##            statprovflag = elmntstr.find("<u>Statutory Provision")
    ##            commflag = max(elmntstr.find('<p class="style3">Commentary'), elmntstr.find('<p class="style3">Introductory Commentary'))
    ##            if backgrdflag>-1:
    ##                backgrdflag =2
    ##            bflgs.append(backgrdflag)
    ##
    ##            if (re.search('^[0-9]\.', gttxt) and gttxt==gttxt.upper()):
    ##                break
    ##            if elmntstr.find("BREAKBREAKBREAK") != -1:
    ##                break
    ##            if elmnt in checklist_strong and elmnt != elem:
    ##                break
    ##            if elmnt in checklist_p and elmnt not in checklist_strong: ##elmntstr.find("strong")==-1:
    ##                if 2 in bflgs:
    ##                    if elmntstr!=[] and not re.search('^<p><strong>§[0-9][A-Z][0-9]\.[0-9]', elmntstr):
    ##                        if [-1, -1, -1, -1] != [commflag, appnoteflag, histnoteflag, statprovflag]:
    ##                            break
    ##                        elif elmnt.get_text()==elmnt.get_text().upper() and re.search('^[0-9]\.', elmnt.get_text()):
    ##                            break
    ##                        backgrd.append(elmnt.get_text())
    ##
    #### commentary for loop
    ##        cflgs = []
    ##        for elmnt in elem.next_elements:
    ##            elmntstr = str(elmnt)
    ##            histnoteflag = elmntstr.find("<u>Historical Note")
    ##            appnoteflag = elmntstr.find("<u>Application Note")
    ##            backgrdflag = elmntstr.find("<u>Background")
    ##            statprovflag = elmntstr.find("<u>Statutory Provision")
    ##            commflag = max(elmntstr.find('<p class="style3">Commentary'), elmntstr.find('<p class="style3">Introductory Commentary'))
    ##            if commflag>-1:
    ##                commflag =2
    ##            cflgs.append(commflag)
    ##
    ##            if (re.search('^[0-9]\.', gttxt) and gttxt==gttxt.upper()):
    ##                break
    ##            if elmntstr.find("BREAKBREAKBREAK") != -1:
    ##                break
    ##            if elmnt in checklist_strong and elmnt != elem:
    ##                break
    ##            if elmnt in checklist_p and elmnt not in checklist_strong: ##elmntstr.find("strong")==-1:
    ##                if 2 in cflgs:
    ##                    if elmntstr!=[] and re.match('^<p><strong>§[0-9][A-Z][0-9]\.[0-9]', elmntstr)==None:
    ##                        if [-1, -1, -1, -1] != [backgrdflag, appnoteflag, histnoteflag, statprovflag]:
    ##                            break
    ##                        elif elmnt.get_text()==elmnt.get_text().upper() and re.search('^[0-9]\.', elmnt.get_text()):
    ##                            break
    ##                        commntry.append(elmnt.get_text())
    ##
    ##
    #### statutory provisions for loop
    ##        sflgs = []
    ##        for elmnt in elem.next_elements:
    ##            elmntstr = str(elmnt)
    ##            histnoteflag = elmntstr.find("<u>Historical Note")
    ##            appnoteflag = elmntstr.find("<u>Application Note")
    ##            backgrdflag = elmntstr.find("<u>Background")
    ##            statprovflag = elmntstr.find("<u>Statutory Provision")
    ##            commflag = max(elmntstr.find('<p class="style3">Commentary'), elmntstr.find('<p class="style3">Introductory Commentary'))
    ##            if statprovflag>-1:
    ##                statprovflag =2
    ##            sflgs.append(statprovflag)
    ##
    ##            if (re.search('^[0-9]\.', gttxt) and gttxt==gttxt.upper()):
    ##                break
    ##            if elmntstr.find("BREAKBREAKBREAK") != -1:
    ##                break
    ##            if elmnt in checklist_strong and elmnt != elem:
    ##                break
    ##            if elmnt in checklist_p and elmnt not in checklist_strong: ##elmntstr.find("strong")==-1:
    ##                if 2 in sflgs:
    ##                    if elmntstr!=[] and re.match('^<p><strong>§[0-9][A-Z][0-9]\.[0-9]', elmntstr)==None:
    ##                        if [-1, -1, -1, -1] != [backgrdflag, appnoteflag, commflag, histnoteflag]:
    ##                            break
    ##                        elif elmnt.get_text()==elmnt.get_text().upper() and re.search('^[0-9]\.', elmnt.get_text()):
    ##                            break
    ##                        statprov.append(elmnt.get_text())
    ##

    ##        print(guidelines)
    ##        print(commntry)
    ##        print(applnote)
    ##        print(backgrd)
    ##        print(histnote)

            off_levels_source = BeautifulSoup(off_levels_source)
            adjust_source = BeautifulSoup(adjust_source)

            levels = off_levels_source.find_all("strong")
##            if year[j]=="2013" and URLs[i]=="2e-k":
##                print(levels)

            lvls = []
            maxofflvl = ""
            firstofflvl = ""

            if levels !=[]:
                for lvl in levels:
                    lvls.append(int(lvl.get_text()))
                maxofflvl = max(lvls)
                firstofflvl = lvls[0]

            adjustments_list = adjust_source.find_all("strong")
            adjst = []
            maxadjst = ""
            firstadjst = ""

            if adjustments_list != []:
                for item in adjustments_list:
                    try:
                        adjst.append(int(item.get_text()))
                    except ValueError:
                        pass
                maxadjst = max(adjst)
                firstadjst = adjst[0]
            
            guidelinesstr = " ".join(guidelines)
            commntrystr = " ".join(commntry)
            applnotestr = " ".join(applnote)
            backgrdstr = " ".join(backgrd)
            histnotestr = " ".join(histnote)
            statprovstr = " ".join(statprov)
            maindivwdctstr = " ".join(maindivwdct)
            baseoffstr = " ".join(base_off)
            speccharstr = " ".join(spec_char)
            crossrefstr = " ".join(cross_ref)
            specinstrstr = " ".join(spec_instr)
            

            guidelinesstr = guidelinesstr.strip()
            commntrystr = commntrystr.strip()
            applnotestr = applnotestr.strip()
            backgrdstr = backgrdstr.strip()
            histnotestr = histnotestr.strip()
            statprovstr = statprovstr.strip()
            maindivwdctstr = maindivwdctstr.strip()
            baseoffstr = baseoffstr.strip()
            speccharstr = speccharstr.strip()
            crossrefstr = crossrefstr.strip()
            specinstrstr = specinstrstr.strip()

            guidelinesstr = " ".join(guidelinesstr.split())
            commntrystr = " ".join(commntrystr.split())
            applnotestr = " ".join(applnotestr.split())
            backgrdstr = " ".join(backgrdstr.split())
            histnotestr = " ".join(histnotestr.split())
            statprovstr = " ".join(statprovstr.split())
            maindivwdctstr = " ".join(maindivwdctstr.split())
            baseoffstr = " ".join(baseoffstr.split())
            speccharstr = " ".join(speccharstr.split())
            crossrefstr = " ".join(crossrefstr.split())
            specinstrstr = " ".join(specinstrstr.split())


            guidelinesstr = guidelinesstr.strip()
            commntrystr = commntrystr.strip()
            applnotestr = applnotestr.strip()
            backgrdstr = backgrdstr.strip()
            histnotestr = histnotestr.strip()
            statprovstr = statprovstr.strip()
            maindivwdctstr = maindivwdctstr.strip()
            baseoffstr = baseoffstr.strip()
            speccharstr = speccharstr.strip()
            crossrefstr = crossrefstr.strip()
            specinstrstr = specinstrstr.strip()

            

            gwc = 0
            cwc = 0
            awc = 0
            bwc = 0
            hwc = 0
            swc = 0

            glen = 0
            clen = 0
            alen = 0
            blen = 0
            hlen = 0
            slen = 0

            
            gwc = len(guidelinesstr.split())
            cwc = len(commntrystr.split())
            awc = len(applnotestr.split())
            bwc = len(backgrdstr.split())
            hwc = len(histnotestr.split())
            swc = len(statprovstr.split())
            bowc = len(baseoffstr.split())
            scwc = len(speccharstr.split())
            crwc = len(crossrefstr.split())
            siwc = len(specinstrstr.split())
            
            glen = len(guidelinesstr)
            clen = len(commntrystr)
            alen = len(applnotestr)
            blen = len(backgrdstr)
            hlen = len(histnotestr)
            slen = len(statprovstr)
            bolen = len(baseoffstr)
            sclen = len(speccharstr)
            crlen = len(crossrefstr)
            silen = len(specinstrstr)

            cleantext = main_div.get_text()
            cleantext = str(cleantext)
            cleantext = cleantext.strip()
            cleantext = " ".join(cleantext.split())

            if int(year[j])==2014:
                delpoint = histnotestr.find("was deleted")
                if delpoint != -1:
                    delnote = histnotestr[delpoint:]
                    histnotestr = histnotestr[0:delpoint]
                else:
                    delnote = ""
                point = max(histnotestr.find("Amended effective"),histnotestr.find("amended effective"))
                if point !=-1:
                    histnoteA = histnotestr[0:point]
                    histnoteB = histnotestr[point:]
                else:
                    histnoteA = histnotestr
                    histnoteB = ""
##                print(histnoteA)
##                print(histnoteB)
                effdate = re.findall("[0-9][0-9][0-9][0-9]", histnoteA)
                effamendsec = histnoteA[histnoteA.find("see Appendix"):histnoteA.find(")",histnoteA.find("see Appendix"))]
                effamend = re.findall("[0-9]+", effamendsec)
                effrange = re.findall("[0-9]+\-[0-9]+", histnoteA)
                if effrange != []:
                    effrange = str(effrange[0])
                    effrangeA = int(effrange[0:effrange.find("-")])
                    effrangeB = int(effrange[effrange.find("-")+1:])
                    for k in range(effrangeB-(effrangeA+1)):
                        effamend.append(str(list(range(effrangeA+1, effrangeB))[k]))
                
                

                p = 0
                for t in effamend:
                    amendments_list.append([t, cleanelem, str(effdate[0]), "effective"])
                    
                amenddate = re.findall("[0-9][0-9][0-9][0-9]", histnoteB)
                amendmentlist = re.finditer("see Appendix C", histnoteB)
                
                for yr in amendmentlist:
                    section = histnoteB[yr.start(): histnoteB.find(")", yr.start())]
                    amendappend = re.findall("[0-9]+", section)
                    amendrange = re.findall("[0-9]+\-[0-9]+", section)
                    if amendrange != []:
                        amendrange = str(amendrange[0])
                        amendrangeA = int(amendrange[0:amendrange.find("-")])
                        amendrangeB = int(amendrange[amendrange.find("-")+1:])
                        for k in range(amendrangeB-(amendrangeA+1)):
                            amendappend.append(str(list(range(amendrangeA+1, amendrangeB))[k]))
                    for u in amendappend:
                        amendments_list.append([u, cleanelem, amenddate[p], "amended"])
                    p = p+1

                deldate = re.findall("[0-9][0-9][0-9][0-9]", delnote)
                dellist = re.finditer("see Appendix C", delnote)

                p = 0
                
                for yr in dellist:
                    section = delnote[yr.start(): delnote.find(")", yr.start())]
                    delappend = re.findall("[0-9]+", section)
                    delrange = re.findall("[0-9]+\-[0-9]+", section)
                    if delrange != []:
                        delrange = str(delrange[0])
                        delrangeA = int(delrange[0:delrange.find("-")])
                        delrangeB = int(delrange[delrange.find("-")+1:])
                        for q in range(delrangeB-(delrangeA+1)):
                            delappend.append(str(list(range(delrangeA+1, delrangeB))[q]))
                    for r in delappend:
                        amendments_list.append([r, cleanelem, deldate[p], "deleted"])
                    p = p+1


            textjoin = [cleanelem, guidelinesstr, commntrystr, statprovstr, applnotestr, backgrdstr, histnotestr]
            textjoin2 = [guidelines, commntry, applnote, backgrd, histnote, statprov]
            textjoin3 = ""
            for joiner in textjoin:
                textjoin3 = textjoin3 + " " + joiner
    ##            runlen = runlen + len(joiner)
    ##            if len(joiner)>0:
    ##                runlen = runlen + 1
    ####        print(textjoin3)
            textcheck = textcheck + " " + textjoin3
    ##        print(textcheck[0:50])
            textcheck = " ".join(textcheck.split())
    ##        print(textcheck[0:100])
    ##        runlen2 = runlen2 + len(textjoin3)
    ##
            maindivwdctstr = " ".join(maindivwdctstr.split())


            wordcount = wordcount + gwc + cwc + awc + bwc + hwc + swc + len(cleanelem.split())
    ##        print(cleanelem)
    ##        print(len(cleanelem.split()))
    ##        print(len(cleanelem))
            charcount = charcount + glen + clen + alen + blen + hlen + slen + len(cleanelem.strip()) + 1 + min(glen, 1) + min(clen, 1) + min(alen, 1) + min(blen, 1) + min(hlen, 1) + min(slen, 1)
    ##        print(charcount)
    ##        print(cleanelem)
    ##        print(len(cleanelem))

    ##        print(len(cleanelem), glen, clen, alen, blen, hlen, slen)
    ##        print(cleanelem, guidelinesstr, commntrystr, applnotestr, backgrdstr, histnotestr, statprovstr)
    ##        print(maindivwdctstr[0:charcount])



    ##        if charcount > 100:
    ##            print(charcount, cleantext[charcount-50:charcount+8], "\n", maindivwdctstr[charcount-50:charcount+8])
    ##        else:
    ##            print(charcount, cleantext[0:charcount+8], "\n", maindivwdctstr[0:charcount+8])

            inccount = 0
            deccount = 0
            parenscount = 0
            shallcount = 0
            mightcount = 0

            for thing in textjoin:
                inc_plus = re.findall("(I|i)ncrease", thing)
                add_plus = re.findall("(A|a)dd", thing)
                dec_plus = re.findall("(D|d)ecrease", thing)
                sub_plus = re.findall("(S|s)ubtract", thing)
                shall_plus = re.findall("(S|s)hall", thing)
                must_plus = re.findall("(M|m)ust", thing)
                might_plus = re.findall("(M|m)ight", thing)
                could_plus = re.findall("(C|c)ould", thing)
                can_plus = re.findall("(C|c)an", thing)
                may_plus = re.findall("may", thing)
                inccount = inccount+len(inc_plus) + len(add_plus)
                deccount = deccount+len(dec_plus) + len(sub_plus)
                shallcount = shallcount + len(shall_plus) + len(must_plus)
                mightcount = mightcount + len(might_plus) + len(could_plus) + len(can_plus) + len(may_plus)
    ##            print(inc_plus, add_plus, dec_plus, sub_plus, shall_plus, must_plus, might_plus)
    ##            print(len(inc_plus), len(add_plus), len(dec_plus), len(sub_plus), len(shall_plus), len(must_plus), len(might_plus))

            for thinger in textjoin2:
                for line2read in thinger:
                    parens_plus = re.findall("^\([A-Za-z0-9]i*v*\)", line2read)
                    parenscount = parenscount + len(parens_plus)
                    

            words1 = maindivwdctstr.split()
            words2 = cleantext.split()

    ##        print(words1[0:10])
    ##        print(words2[0:10])



            
            rowtowrite.append([cleanelem, guidelines, commntry, statprov, applnote, backgrd, histnote])
            rowtowrite2.append([cleanelem, guidelinesstr[0:20000], baseoffstr[0:20000], speccharstr[0:20000], crossrefstr[0:20000], specinstrstr[0:20000], commntrystr[0:20000], statprovstr[0:20000], applnotestr[0:20000], backgrdstr[0:20000], histnotestr[0:20000], gwc, cwc, awc, bwc, hwc, swc, glen, clen, alen, blen, hlen, slen, inccount, deccount, parenscount, maxofflvl, firstofflvl, maxadjst, firstadjst, bowc, scwc, crwc, siwc, bolen, sclen, crlen, silen])

        for wor in range(len(words1)):
            if words1[wor]!=words2[wor]:
                print(words1[wor], words2[wor])
    ##            time.sleep(1)
                break
    ##
    ##        if wor%1000==0:
    ##            print("still going")
    ##            print(wor)

    ##    print(cleantext[-100:])
    ##    print(textcheck[-100:])

        for ltr in range(len(cleantext)):
            if cleantext[ltr]!=maindivwdctstr[ltr]:
                print("\n", cleantext[ltr-5:ltr+100], "\n", maindivwdctstr[ltr-5:ltr+100])
    ##            time.sleep(1)
                break
    ##
    ##        if lt%1000==0:
    ##            print("still going")
    ##            print(ltr)


        print(wordcount, len(cleantext.split()), len(maindivwdctstr.split()))
    ##    print(maindivwdctstr[0:100])
        print(charcount-1, len(cleantext), len(textcheck), len(maindivwdctstr))
                      
    ##    print(str(main_div.get_text()).split())
        
        filename = ("usscg_%s_sec_%s.csv" %(year[j], URLs[i]))
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect = 'excel')
            writer.writerows(rowtowrite)

        filename_2 = ("usscg_%s_sec_%s_lens_word_counts.csv" %(year[j], URLs[i]))
        with open(filename_2, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect = 'excel')
            writer.writerows(rowtowrite2)

    if year[j]=="2014":
        filename_3 = ("usscg_amendments_list.csv")
        with open(filename_3, 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, dialect = 'excel')
            writer.writerows(amendments_list)



    ##    print(cleantext[0:1000])
            
    ##    for child in main_div.find_all("strong"):
    ##        print(child)
    ##        print(type(child))
    ##        for children in child.contents:
    ##            print(children.next)
    ##        print(type(main_div))
    ##        print(type(main_div.div))   
                
    ##
    ##    for sibling in soup.div.next_elements:
    ##        ##print(sibling)
    ##        print(j)
    ##        j = j+1
