#!/usr/bin/env python
''' Script to retrieve grades from Ellucian Banner Web '''
import requests
import time
import sys
import mandrill
from lxml import html

from settings import settings

# MailChimp Client
mandrill_client = mandrill.Mandrill(settings['MAILCHIMP_KEY'])

# Previous stores previous grade tuple retrieved from request
previous = None
# Grades stores current grade tuple retrieved from request
grades = None

# Run until all grades are posted
while True:
    # Create and establish session
    s = requests.Session()
    request = s.get(settings['BASE_URL'] + 'twbkwbis.P_WWWLogin')

    # POST login information
    response = s.post(settings['BASE_URL'] + 'twbkwbis.P_ValLogin',
                      data=dict(sid=settings['USERNAME'],
                                PIN=settings['PASSWORD']))

    # POST semester to retrieve (Fall 2015)
    response = s.post(settings['BASE_URL'] + 'bwcklibs.P_StoreTerm',
                      data=dict(term_in='201508'))

    # GET posted grades
    response = s.get(settings['BASE_URL'] + 'bwskfshd.P_CrseSchdDetl')

    # Create parseable HTML from response
    content = html.fromstring(response.content)

    # Parse HTMl using XPATH selectors
    info = content.xpath('//td[@rowspan]//p[@class="centeraligntext"]/text()')

    # Create tuples containing course information
    zipped = zip(*[iter(info)]*5)
    grades = [z[-1] for z in zipped]

    # If previous grade tuple is equal to current grade tuple, don't do anything
    # Grades haven't been posted
    if previous == grades:
        pass

    # Otherwise a new grade has been posted -- send e-mail notification
    else:
        # Try to send e-mail notification
        try:
            # Create message
            message = {
                'from_email': settings['MY_EMAIL'],
                'from_name': settings['MY_NAME'],
                'subject': 'Grades Posted',
                'html': '<p>Grades are updated: %s</p>' % grades,
                'to': [{
                    'email': settings['MY_EMAIL'],
                    'name': settings['MY_NAME'],
                    'type': 'to'}]
            }

            # Send message
            result = mandrill_client.messages.send(message=message,
                                                   async=False,
                                                   ip_pool='Main Pool')
        except mandrill.Error, e:
            # Ignore errors
            pass

    # Exit if all grades are posted
    # u'\xa0' is blank character returned for grades that haven't been posted
    if u'\xa0' not in grades:
        sys.exit(0)

    # Set previous to current query
    previous = grades
    # Sleep for 10 minutes
    time.sleep(600)
