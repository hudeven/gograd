#-*-coding:utf-8-*-

import re
from helper_functions import findKeywords, lcs

#NOTE ALL ' ' will be converted single letter '.' as regex for matching
POSITION = ['assistant professor','associate professor', 'Post-Doctoral Fellow', 'Teaching Professor', 'PhD student', 'Ph.D. student', 'Master student', 'M.S. student', 'Senior Research Programmer', 'Executive Officer', 'lecturer', 'scientist', 'administrator', 'postdoc', 'master', 'professor', 'PhD']
#print "POSITION:", POSITION
UNIVERSITY = []
university_names_f = open('university_name.txt','r')
universityNames = university_names_f.readlines()
university_names_f.close()
for lines in universityNames:
    if(not re.match(r'[A-Z].edit.', lines)):
        shortLetters = lines.split(' - ')[0].strip()
        UNIVERSITY.extend(shortLetters.split(' or '))
        shortLetters2 = re.sub(r'[^a-zA-Z]', '.', shortLetters)
        if not lines.__contains__(' - ') :
            continue
        longLetters = re.sub(r'\[[0-9]\]', ' ', lines.split(' - ')[1])
        regex_sl = ".*" + reduce((lambda x,y: x + y), map((lambda x: x + ".*"), shortLetters2))
        ss = longLetters.split(',')
        sss = []
        for each_ss in ss:
            sss.extend( each_ss.split(' or ') )
        r = ""
        for s in sss:
            s = s.strip()
            if r=="": r = s
            else: r += ", " + s
            if (re.match( regex_sl, r, re.M)):
                UNIVERSITY.append(r.strip())
                r = ""
#print "UNIVERSITY", UNIVERSITY

INTERESTS = []
interests_f = open('interests.txt','r')
interests = interests_f.readlines()
interests_f.close()
for lines in interests:
    interest = lines.split(' – ')[0].strip()
    INTERESTS.append(interest)
#print "INTERESTS", INTERESTS
#INTERESTS = ['programming languages', 'program verification', 'type theory']


class ResearcherProfile():
    name = None
    url = None
    position = None
    university = None
    photoURL = None
    text = ""
    researchInterests = []
    criticalText = ""
    pageTitle = ""

    def __init__(self):
        self.name = None
        self.url = None
        self.position = None
        self.university = None
        self.photoURL = None
        self.text = ""
        self.criticalText = ""

    def obtainInfo(self, universityflag=True):
        if not self.text:
            print "Empty text"
            return
        pResults = [] # position
        sResults = [] # school/university
        nResults = [] # name
        iResults = [] # research interests.txt
        cResults = "" # critical text
        #Split the sentences
        rawText = []
        self.text = re.sub(r'\n[\n]+', '\n', self.text)
        #self.text = re.sub(r'\s[\s]+', ' ', self.text)
        rawText1 = self.text.split('\n')
        for eachrawtext in rawText1:
            if eachrawtext.strip() == "$" or eachrawtext.strip() == "$$": #hyperlinks are marked by $ at beginning and end
                continue
            if len(eachrawtext.strip().split(' ')) < 5 : # two sentence must have at least 6 words
                rawText.append(eachrawtext.strip())
            else:
                rawText.extend(eachrawtext.split('.'))
        ######main loop#####
        accu = ""
        for i, eachLine in enumerate(rawText):
            #if eachLine == " student$at the $Robotics Institute$of $Carnegie Mellon University$":
            #    print "a"
            #print "i=", i, "<",eachLine,">"
            #Prof. Dr. Mr. Ms. Mrs.
            if(eachLine.endswith(" Prof")\
                or eachLine.endswith(" Mr")\
                or eachLine.endswith(" Ms")\
                or eachLine.endswith(" Mrs")\
                or eachLine.endswith(" Ph")
               ):
                accu += eachLine + "."
                continue
            if accu.strip() and accu.endswith(" Ph.") and eachLine=="D":
                accu += eachLine + "."
                continue
            if accu.strip():
                eachLine = accu + eachLine
                accu = ""
            #print "<", eachLine, ">"
            #A few words and is in the first lines
            if i < 45 and len(eachLine.split(' '))<=7 :
                #Task1 Find Position
                pResults += findKeywords(eachLine, POSITION, flag=re.M|re.I, antiLink=True)
                #there will be $<..>$ in hyperlinks, so it means they will not be considered when detecting faculty positions
                #I did this, because of some hyperlinks in menu has words like "Postdocs" etc.

                #Task2 Find Research Interests
                iResults += findKeywords(eachLine, INTERESTS, re.M|re.I)
                #Task3 Find info of Looking for Student
                #Task4 Find associated schools
                if universityflag : sResults += findKeywords(eachLine, UNIVERSITY, flag=re.M)
                #Task5 Names
                #Note \$ \, are ignored for hpyerlinked names
                if(not re.match(r'(.*(university|professor).*|.*\s.*\s.*\s.*\s.*|.*[<\'\"@\/\{\}\(\)\*%\?=>:\|;#0-9].*)', eachLine.strip(), re.M|re.I)):
                    if( re.match(r'.*\s.*', eachLine.strip(), re.M|re.I)):
                            nResults.append(re.sub(r'\$', ' ', eachLine).strip())
                            #print "Potiential Name List appends", eachLine.strip()
            #Otherwise
            else:
                # I am blabla at blahblah
                if re.match(r'.*I(\sam|\'m)\s(a|an).*at.*', eachLine, re.M|re.I):
                    pResults_tmp = findKeywords(eachLine, POSITION, re.M|re.I)
                    if pResults_tmp : pResults = pResults_tmp
                    if universityflag:
                        sResults_tmp = findKeywords(eachLine, UNIVERSITY, re.M)
                        if sResults_tmp : sResults = sResults_tmp
                # My research is about blahblah
                if re.match(r'(.*my.research.*|.*research.*interests.*|.*research.*focus.*on.*|.*I.*interested.*in.*)', eachLine, re.M|re.I):
                    iResults_tmp = findKeywords(eachLine, INTERESTS, re.M|re.I)
                    if iResults_tmp : iResults = iResults_tmp
                #We collect those words in the first 200 lines...
                if i<200 : iResults += findKeywords(eachLine, INTERESTS, re.M|re.I)
                if i<200 : pResults += findKeywords(eachLine, POSITION, re.M|re.I)
                if universityflag:
                    if i<50 : sResults += findKeywords(eachLine, UNIVERSITY, re.M)
                #I am looking for graduate students
                if re.match(r'(.*work.*with.*me.*|.*students.*please.*contact.*me.*|.*interested.*with.*me|.*looking.*for.*|.*(RA|TA|GA).*available.*|.*position.*available.*|.*postdoc.*available.*)', eachLine, re.M|re.I):
                    cResults += eachLine.strip() + ". "

        if(pResults) : self.position = pResults[0]
        if(iResults) : self.researchInterests = list(set(iResults))
        if universityflag:
            if(sResults) : self.university = sResults[0]
        #TODO if multiple capitcal letter matches, then should return the longest
        if(cResults) : self.criticalText = cResults.strip()
        if(nResults) :
            if self.pageTitle:
                ratiorecord = 0
                for i, name in enumerate(nResults):
                    #print [self.pageTitle.lower(), name.lower()]
                    #print lcs(self.pageTitle.lower(), name.lower())
                    #print 1.0 * len(lcs(self.pageTitle.lower(), name.lower())) / len(name.lower())
                    ratio = 1.0 * len(lcs(self.pageTitle.lower(), name.lower())) / len(name.lower())
                    #TODO better ratio definition?
                    if len(name) >= 7 and ratio >= 0.3:
                        if ratio > ratiorecord:
                            ratiorecord = ratio
                            self.name = name
            else:
                self.name = nResults[0]

    def printProfile(self):
         print "-" * 15
         print "Name:", self.name
         print "URL:", self.url
         print "Position:", self.position
         print "University:", self.university
         print "Research Interests:", self.researchInterests
         print "Photo URL:", self.photoURL
         print "Critical Text:", self.criticalText
         #print "text", self.text

    def escapeNULL(self):
        if(self.name==None): self.name = " "
        if(self.url==None): self.url = " "
        if(self.position==None): self.position = " "
        if(self.university==None): self.university = " "
        if(self.criticalText==None): self.criticalText = " "
        if(self.photoURL==None): self.photoURL= " "
