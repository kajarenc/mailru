# -*- coding: utf-8 -*-
__author__ = 'kajarenc'
import urllib2
import unicodedata
import requests
from bs4 import BeautifulSoup


callsNumber = 0
noSkillNumber = 0
noUrlNumber = 0


def superFunction(firstName, lastName):
    global callsNumber
    global noSkillNumber
    global noUrlNumber
    print firstName, lastName
    BASE_URL = 'http://go.mail.ru/search?fm=1&q='
    callsNumber += 1
    print "HOP"

    def unicode_normalizer(text):
        try:
            return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        except:
            return text.encode('ascii', 'ignore')

    firstName = firstName
    lastName = lastName
    person = ' '.join((firstName, lastName))

    req = requests.get(BASE_URL + person.replace(' ', '+').lower())
    html = unicode_normalizer(req.text)
    soup = BeautifulSoup(html)
    print soup.head
    cashedCopies = soup.findAll('a', {'class': 'saved-url'})

    def correct_url(x):
        linkDiv = x.find_parent('li', {'class': 'result__li'})
        if linkDiv is None:
            return False
        else:
            if firstName.lower() in [bText.get_text().lower() for bText in linkDiv.findAll('b')] and lastName.lower() \
                    in [bText.get_text().lower() for bText in linkDiv.findAll('b')]:
                return True
            return False


    c = filter(lambda x: 'linkedin' in x.get('href') and correct_url(x), cashedCopies)
    superlink = ""
    try:
        superlink = c[0].get('href')
        print superlink
    except IndexError:
        noUrlNumber += 1
        return
        # print "AYAYAYAYAYAYtry again"
    res = {}

    response = urllib2.urlopen(superlink)
    html = response.read()
    soup = BeautifulSoup(html)
    info = soup.findAll('div', {'class': 'saved-body'})[0]

    try:
        h3 = soup.find_all("h3", text=u'Навыки')
        outerDiv = h3[0].parent.parent
        skillList = [elem.text for elem in outerDiv.find_all('p')]
        skillDict = {'skills': skillList}
        for key, value in skillDict.iteritems():
            print key, '->'
            for skill in value:
                print skill
    except IndexError:
        noSkillNumber += 1
        print "NO SKILLS :("

    table = info.find('table')
    if table != None:
        for tr in table.findAll('tr'):
            print tr.contents[0], '->', tr.text[len(tr.contents[0]):]
    scraped_information = []

    for h2_tag in info.findAll('h2'):
        myDict = {
            h2_tag.string: h2_tag.find_next_sibling('div').get_text() if h2_tag.find_next_sibling('div') else None}
        scraped_information.append(myDict)
    for dict in scraped_information:
        for key in dict:
            if key and dict[key]:
                try:
                    print key.encode('utf-8'), '->', dict[key].encode('utf-8'), '\n'
                except LookupError:
                    print "APSOS"


import time

with open('baba') as f:
    for line in f:
        if (len(line)):
            try:
                time.sleep(300)
                superFunction(line.split()[0], line.split()[1])
            except:
                pass
f.closed
print "---------------------------------------------------"
print noSkillNumber
print noUrlNumber
print callsNumber
