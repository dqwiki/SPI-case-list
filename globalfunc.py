# -*- coding: utf-8 -*-
"""
(C) 2016 DeltaQuad (enwp.org/User:DeltaQuad)

This file is part of DeltaQuadBot.

DeltaQuadBot is free software: you can redistribute it and/or modify
it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DeltaQuadBot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU AFFERO GENERAL PUBLIC LICENSE for more details.

You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
along with DeltaQuadBot. If not, see <https://www.gnu.org/licenses/agpl.txt>.
"""

from datetime import datetime
import sys
import platform
import time
import json
import re

import localconfig
import mwclient
import login

masterwiki =  mwclient.Site('en.wikipedia.org')
masterwiki.login(login.username,login.password)

page = masterwiki.pages["User:AmandaNP/Clerks list"]
clerks = page.text()

def callAPI(params):
    return masterwiki.api(**params)

def getCurrentCases(category):
    category = "Category:" + category
    params = {'action': 'query',
        	'list': 'categorymembers',
        	'cmtitle': category,
                'cmnamespace':'4',
                'cmlimit':'500',
                'format':'json',
                'rawcontinue':'1'
                }
    raw = callAPI(params)
    reg = raw["query"]["categorymembers"]
    reg = formatArray(reg)
    return reg

def getCurrentCasesBeta():
    print "Null"

def formatArray(database):
    i = 0
    cases = []
    for entry in database:
        cases = cases + [entry["title"]]
    return cases

def getAllCases(ctype):
    if ctype=="inprogress":return getCurrentCases('SPI cases currently being checked')
    if ctype=="endorsed":return getCurrentCases('SPI cases awaiting a CheckUser')
    if ctype=="relist":return getCurrentCases('SPI cases relisted for a Checkuser')
    if ctype=="curequest":return getCurrentCases('SPI cases requesting a checkuser')
    if ctype=="checked":return getCurrentCases('SPI cases CU complete')
    if ctype=="ADMIN":return getCurrentCases('SPI cases needing an Administrator')
    if ctype=="declined":return getCurrentCases('SPI cases declined for checkuser by clerk')
    if ctype=="cudeclined":return getCurrentCases('SPI cases declined for checkuser by CU')
    if ctype=="open":return getCurrentCases('SPI cases awaiting review')
    if ctype=="moreinfo":return getCurrentCases('SPI cases requesting more information')
    if ctype=="hold":return getCurrentCases('SPI cases on hold by clerk')
    if ctype=="cuhold":return getCurrentCases('SPI cases on hold by checkuser')
    if ctype=="close":return getCurrentCases('SPI cases awaiting archive')
    if ctype=="clerk":return getCurrentCases('SPI cases needing a Clerk')

def getHistory(title):
    params = {'action':'query',
              'prop':'revisions',
              'titles':title,
              'rvlimit':'500',
              'rvprop':'timestamp|user|comment|size',
              'format':'json',
              'rawcontinue':'1'}
    history = callAPI(params)
    full = history["query"]["pages"]
    for singleid in full:
        pageid = singleid
    history = history["query"]["pages"][pageid]['revisions']
    return history
def getFiler(revisions):
        i=0
        for revision in revisions:
            try:
                if "Archiving case to ".lower() in revision["comment"].lower():# or "archiving" in revision["comment"].lower():
                    return revisions[i-1]["user"],datetime.strptime(revisions[i-1]["timestamp"], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d')
            except:
                null=1 #nullifier due to "commenthidden"
            i+=1
        last = revisions.pop()
        return [last["user"],datetime.strptime(last["timestamp"], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d')]
                
def getLastEdit(title):
    history=getHistory(title)
    last = history[0]
    timestamp = last["timestamp"]
    time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d %Hh%M UTC')
    time = time.replace(" ".join(time.split(" ")[0:2]), "{{Date table sorting|"+" ".join(time.split(" ")[0:2])+"}}")
    return [last["user"],time]
def getLastClerk(title):
    revisions = getHistory(title)
    i=0
    while True:
        try:last = revisions[i]
        except:
                return "None"
        try:
                if "archive" in last["comment"].lower() or "archiving" in last["comment"].lower():
                    return "None"
                if last["user"] in clerks:
                    return last["user"]
        except:
                null=1#placeholder
        i+=1
    return "None"
    

def formatTableRow(case, status,filer,dateFiled,lastEdit,timestamp,lastClerk):
    return "{{SPIstatusentry|" + case + "|" + status + "|" + filer + "|{{Date table sorting|" + dateFiled + "}}|" + lastEdit + "|" + timestamp + "|" + lastClerk +"}}"

def caseHistoryCompile(caseTypes):
        table=""
        for entry in caseTypes:
                caselist=getAllCases(entry)
                if caselist == None:
                    continue
                for case in caselist:
                    history=getHistory(case)
                    filer=getFiler(history)
                    lastEdit=getLastEdit(case)
                    lastClerk=getLastClerk(case)
                    if lastClerk=="None":lastClerk=""
                    dateFiled=filer[1]
                    filer = filer[0]
                    timestamp = lastEdit[1]
                    lastEdit = lastEdit[0]
                    filer="[[User:"+filer+"|"+filer+"]]"
                    lastEdit="[[User:"+lastEdit+"|"+lastEdit+"]]"
                    try:table+=formatTableRow(case.split("/")[1],entry,filer,dateFiled,lastEdit,timestamp,lastClerk)+"\n"
                    except:
                            print 'Main SPI page ignored'
        return table

def addHeader(name):
        return "<noinclude>\n== "+name+" ==\n</noinclude>"

def makeTable(content,first):
        if first:
                tabletop="""
{|class="wikitable sortable" width="100%"
!Investigation!!Status!!Filer!!Date filed!!Last user edit!!timestamp!!Last clerk/CU edit
|-
"""
        if not first:tabletop="""<noinclude>
{|class="wikitable sortable" width="100%"
!Investigation!!Status!!Filer!!Date filed!!Last user edit!!timestamp!!Last clerk/CU edit
</noinclude>|-
"""
        tablebottom="<noinclude>|}"
        return tabletop + content + tablebottom
def caseProcessor():
    #print "CU results table"
    categories=["checked"]
    cursftable = addHeader("CU Result Cases")+makeTable(caseHistoryCompile(categories),True)
    #print "!!!DONE!!!"
    #print "CU endorsed table"
    categories=["endorsed","relist"]
    cueftable = addHeader("CU Endorsed Cases")+makeTable(caseHistoryCompile(categories),False)
    #print "!!!DONE!!!"
    #print "CU review table"
    categories=["curequest"]
    curftable = addHeader("CU Review Cases")+makeTable(caseHistoryCompile(categories),False)
    #print "!!!DONE!!!"
    #print "CU decline table"
    categories=["declined","cudeclined"]
    cudftable = addHeader("CU Declined Cases")+makeTable(caseHistoryCompile(categories),False)
    #print "!!!DONE!!!"
    #print "Open table"
    categories=["open"]
    oftable = addHeader("Open Cases")+makeTable(caseHistoryCompile(categories),False)
    #print "!!!DONE!!!"
    #print "Wait table"
    categories=["inprogress","ADMIN","moreinfo","hold","cuhold","clerk"]
    wftable = addHeader("Waiting Cases")+makeTable(caseHistoryCompile(categories),False)
    #print "!!!DONE!!!"
    #print "Archive table"
    categories=["close"]
    arcftable = addHeader("To Archive Cases")+makeTable(caseHistoryCompile(categories),False)
    #print "!!!DONE!!!"
    #print "Processing master table..."
    
    final = "__NOEDITSECTION__\n"+cursftable + cueftable + curftable + cudftable + oftable + wftable + arcftable
    #print "!!!DONE!!!"
    #print "----POSTING----"
    page = masterwiki.pages["User:AmandaNP/SPI case list"]
    page.save(final, "Updating SPI caselist")
    #print "!!!DONE!!!"
caseProcessor()
