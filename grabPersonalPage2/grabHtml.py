#-*-coding:utf-8-*-

import re
from sgmllib import SGMLParser

class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.content = ""
        self.imgURL = []
        self.title = None
        self.Ignore = False
        self.lastContent = ""

    def start_img(self, attr):
        for eachAttr in attr:
            if eachAttr[0]=="src" and re.match(r'.*(jpg|gif|jpeg)',eachAttr[1], re.M|re.I) :
                 self.imgURL.append(eachAttr[1])

    #TODO the page may contain this: <meta http-equiv="refresh" content="0;url=B"> Refer to # http://blog.csdn.net/terry_tusiki/article/details/8364220

    def handle_data(self, data):
        if not self.Ignore:
            if data.strip():
                for each in re.sub(r'(\t|\n|\r)', ' ', data).split(' '):
                    #print "each=",each
                    if each.strip():
                        self.content += each.strip() + " "
                self.lastContent = data

    def unknown_starttag(self, tag, attr):
        if not (tag=="a" or tag=="b"):
            self.content += "\n"

        if tag=="script":
            self.Ignore = True

        if tag=="a":
            self.content += "$"


    def unknown_endtag(self, tag):
        if tag=="a":
            self.content = self.content.strip() + "$"

        if not (tag=="a" or tag=="b"):
            self.content = self.content.strip() + "\n"

        if tag=="title":
            self.title = self.lastContent.strip()
            #print "Title:", self.title

        if tag=="script":
            self.Ignore = False
