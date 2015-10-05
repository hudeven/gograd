#-*-coding:utf-8-*-

import urllib2, os, sys, re
from sgmllib import SGMLParser
from urlparse import urljoin
import pdb
import psycopg2

from researcher_profile import ResearcherProfile
from helper_functions import *
from grabHtml import URLLister

def main():
    conn = psycopg2.connect("dbname=myproject user=myprojectuser host='localhost' password='lovelinhui1314#'")
   
    ppURL_f = open("ppURL.txt", "r")
    university = None
    for line in ppURL_f:
      try:
        if not line.strip():
            continue 
        #From ppURL.txt read Name + URL
        if line[0]=='#':
            if line[1:]:
                university = line[1:].split("http")[0].strip()
            else:
                university = None
            continue
        name = None
        myURL = None 
        line_s = line.split('|', 1)
        if(len(line_s) == 2):
            name = line_s[0].strip()
            myURL = line_s[1].strip()
            #print "Name", line_s[0]
            #print "URL", line_s[1]
        else:
            myURL = line_s[0].strip()
            #print "URL", line_s[0]
 
        #From online web, read Content
        try:
            print "="*30
            print "Fetching", myURL, "......"
            parser = URLLister()
            parser.reset()
            usock = urllib2.urlopen(myURL, timeout=30)
            print "SUCCEED. Code=",usock.code
            myURL = usock.geturl()
            parser.feed(usock.read())
            usock.close()
            parser.close()
            #TODO redirecting page
        except Exception,e:
            print "FAILED. ERROR=", e
            continue

        rp = ResearcherProfile()
        if myURL: rp.url = myURL
        rp.text = parser.content
        if parser.imgURL:
            eachImg = parser.imgURL[0]
            rp.photoURL = urljoin(myURL, eachImg)
        if parser.title:
            rp.pageTitle = parser.title
        #    rp.photoURL.append(obtainImage(urljoin(myURL,eachImg), "media/"))
        rp.obtainInfo(universityflag=False)
        if name : rp.name = name #Overwite names because names are ready in ppURL
        if university: rp.university = university #Overwrite university because already collected
        rp.printProfile()
        rp.escapeNULL()


        #Save to Postgres
        cur = conn.cursor()
        cur.execute("INSERT INTO blog_researcherprofile (name, url, position, university, interests, photo_url, critical_text) VALUES(%s, %s, %s, %s, %s, %s, %s)", (rp.name, rp.url, rp.position, rp.university, rp.researchInterests, rp.photoURL, rp.criticalText))
        conn.commit()
        cur.execute("SELECT * FROM blog_researcherprofile")
        #print cur.fetchall()
      except Exception,e:
          conn.close()
          conn = psycopg2.connect("dbname=myproject user=myprojectuser host='localhost' password='lovelinhui1314#'")
          print e
          pass
    conn.close()
    ppURL_f.close()

if __name__ == "__main__":
    main()
