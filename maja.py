from __future__ import absolute_import
from random import shuffle

import requests
import re
import json
from collections import defaultdict
import sys
import datetime
from oauth2client import client
from googleapiclient import sample_tools
from collections import namedtuple
import argparse
import httplib2
import os

from googleapiclient import discovery
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from itertools import groupby

__author__ = 'jonas.brunsgaard@gmail.com (Jonas Brunsgaard)'


class TGEntryCollector(object):
    open_ = '16:00', '21:30'
    open_saturday = '13:00', '17:00'

    def __init__(self, url):
        self.url = url
        self.data = self._fetch_json(self.url)

    @staticmethod
    def _fetch_json(url):
        resp = requests.get(url)
        pattern = '.*extend\(true, doodleJS.data, ({"poll":.*})\);'
        match = re.search(pattern, resp.text)
        return json.loads(match.groups()[0])

    @staticmethod
    def parse_date(datestring):
        m, d, y = map(int, datestring[3:].split('/'))
        return datetime.date(2000+y, m, d)

    def __iter__(self):
        Entry = namedtuple('Entry', ['date', 'name'])
        dates = [self.parse_date(d) for d in self.data['poll']['optionsText']]
        participants = self.data['poll']['participants']
        for p in participants:
            mapping = zip(dates, p['preferences'])
            dates_filtered = (date for (date, char) in mapping if char == 'y')
            for date in dates_filtered:
                yield Entry(date, p['name'].title())

    def shifts(self):
        Shift = namedtuple('Shift', ['date', 'text', 'start', 'end'])
        entries = sorted(self)
        for date, sub_iter in groupby(entries, key=lambda t: t[0]):
            names = [e.name for e in sub_iter]
            shuffle(names)
            text = ' &'.join(', '.join(names).rsplit(',', 1))
            start, end = self.open_
            # If Saturday
            if date.weekday() == 5:
                start, end = self.open_saturday
            yield Shift(date, text, start, end)

if __name__ == "__main__":
    url = 'http://doodle.com/4qeiacg36ppi3h92'
    url = 'http://doodle.com/6y3xv3mc9z9trq6w'
    shifts = list(TGEntryCollector(url).shifts())
    storage = file.Storage('calendar' + '.dat')
    credentials = storage.get()
    http = credentials.authorize(http=httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #  flow = client.flow_from_clientsecrets(
    #      'client_secrets.json',
    #      scope='https://www.googleapis.com/auth/calendar')

    events = []
    for date, text, start, end in shifts:
        data = {
            'summary': text,
            'start': {'dateTime': '{}T{}:00.000+02:00'.format(date, start)},
            'end': {'dateTime': '{}T{}:00.000+02:00'.format(date, end)},
        }
        e = service.events().insert(calendarId='primary', body=data)
        print('{:<3} {}-{:<6} {}'.format(date.day, start, end, text))

    while True:
        proceed = raw_input('\nShould I continue? (y/n): ')
        if proceed in ['y', 'n']:
            break

    if proceed == 'y':
        for e in events:
            pass
            # e.execute()
        print('Done!')
    else:
        print('Aborted!')


