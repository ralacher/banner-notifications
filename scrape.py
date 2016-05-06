#!/usr/bin/env python
''' Script to retrieve grades from Ellucian Banner Web '''
import requests
import time
import sys
from lxml import html
import os
from settings import settings
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

# Previous stores previous grade tuple retrieved from request
previous = None
# Grades stores current grade tuple retrieved from request
grades = None

# Classes stores list of class names defined in settings
classes = settings['CLASSES'] 

# hashed will store hashed value of class names, grades
hashed = None

# Read file containing previous check
if 'grades.txt' in os.listdir(settings['PATH']):
    f = open(settings['PATH'] + 'grades.txt', 'rw')
    hashed = f.read()
else:
    f = open(settings['PATH'] + 'grades.txt', 'w+')
f.close()

# Create and establish session
s = requests.Session()
request = s.get(settings['BASE_URL'] + 'twbkwbis.P_WWWLogin')

# POST login information
response = s.post(settings['BASE_URL'] + 'twbkwbis.P_ValLogin',
                  data=dict(sid=settings['USERNAME'],
                            PIN=settings['PASSWORD']))

# POST semester to retrieve (Fall 2015)
response = s.post(settings['BASE_URL'] + 'bwcklibs.P_StoreTerm',
                  data=dict(term_in=settings['SEMESTER']))

# GET posted grades
response = s.get(settings['BASE_URL'] + 'bwskfshd.P_CrseSchdDetl')

# Create parseable HTML from response
content = html.fromstring(response.content)

# Parse HTMl using XPATH selectors
info = content.xpath('//td[@rowspan]//p[@class="centeraligntext"]/text()')

# Create tuples containing course information
zipped = zip(*[iter(info)]*5)
grades = [z[-1] for z in zipped]

# Create message for e-mail 
message = str(zip(classes, grades))

# Create new hash from message content
new_hashed = str(hash(message))

# If previous grade hash is equal to new hash, don't do anything
# Grades haven't been posted
if new_hashed == hashed:
    pass

# Otherwise a new grade has been posted -- send e-mail notification
# Create e-mail message
elif settings['EMAIL'] == True:
   msg = MIMEText(message)
    msg['From'] = ''
    msg['To'] = ''
    msg['Subject'] = ''

    # Pipe message to sendmail
    p = Popen(['/usr/sbin/sendmail', '-t', '-oi'], stdin=PIPE)
    p.communicate(msg.as_string())

    # Open grades and overwrite hashed message with new hashed message
    f = open(settings['PATH'] + 'grades.txt', 'w+')
    f.write(new_hashed)
    f.close()

# Don't send email, just print to stdout
else:
    print message
