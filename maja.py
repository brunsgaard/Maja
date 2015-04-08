from __future__ import absolute_import

from collections import namedtuple
from googleapiclient import discovery
from itertools import groupby
from oauth2client import file
from random import shuffle
from termcolor import colored


import datetime
import httplib2
import json
import re
import requests


__author__ = 'jonas.brunsgaard@gmail.com (Jonas Brunsgaard)'


class DoodlePage(object):

    Entry = namedtuple('Entry', ['date', 'name'])

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

    def entries(self):
        dates = [self.parse_date(d) for d in self.data['poll']['optionsText']]
        participants = self.data['poll']['participants']
        for p in participants:
            mapping = zip(dates, p['preferences'])
            dates_filtered = (date for (date, char) in mapping if char == 'y')
            for date in dates_filtered:
                yield self.Entry(date, p['name'].title())


class TGWorkShift(object):

    Shift = namedtuple('Shift', ['date', 'text', 'start', 'end'])
    open_ = '16:00', '21:30'
    open_saturday = '13:00', '17:00'

    def __init__(self, url):
        self.doodle = list(DoodlePage(url).entries())
        self.entries = list(self.parse_doodle_entries())

    @staticmethod
    def format_names(names):
        return ' &'.join(', '.join(names).rsplit(',', 1))

    def parse_doodle_entries(self):
        entries = sorted(self.doodle)
        for date, sub_iter in groupby(entries, key=lambda t: t[0]):
            names = [e.name for e in sub_iter]
            shuffle(names)
            text = self.format_names(names)
            start, end = self.open_
            # If Saturday
            if date.weekday() == 5:
                start, end = self.open_saturday
            yield self.Shift(date, text, start, end)

    def __str__(self):
        res = []
        for date, text, start, end in self:
            date = '{}/{}'.format(date.day, date.month)
            res.append('{:<3} {}-{:<6} {}'.format(date, start, end, text))
        return '\n'.join(res)

    def __iter__(self):
        for e in self.entries:
            yield e

    def list_entries(self):
        for n, t in enumerate(self.entries):
            date, text, start, end = t
            date_str = '{}/{}'.format(date.day, date.month)
            str_entry = ('{:<4} - {:<4} {}-{:<6} {}'.format(
                '({})'.format(n), date_str, start, end, text))
            if date.weekday() == 5:
                str_entry = colored(str_entry, 'magenta')
            print(str_entry)

    def append_text_to_entry(self, date, text, start, end):
        text = '{} {}'.format(text, raw_input(text + ' '))
        return self.Shift(date, text, start, end)

    def overwrite_text_to_entry(self, date, text, start, end):
        return self.Shift(date, raw_input('New text: '), start, end)

    def modify_entry(self):

        # pick an entry
        while True:
            input_ = raw_input('pick entry: ')
            try:
                n = int(input_)
                entry = self.entries[n]
                break
            except:
                print('Come on Maja, that is not a valid entry, try again')
                pass

        # choose operation
        op = None
        while op not in ['a', 'o']:
            op = raw_input('owerwrite or append text? (o/a): ')
            if op == 'a':
                self.entries[n] = self.append_text_to_entry(*entry)
            if op == 'o':
                self.entries[n] = self.overwrite_text_to_entry(*entry)

    def modify(self):
        self.list_entries()
        while True:
            self.modify_entry()
            self.list_entries()
            if raw_input("Edit another entry?: ") != 'n':
                continue
            break

class CalendarPusher(object):
    pass


if __name__ == "__main__":
    url = 'http://doodle.com/4qeiacg36ppi3h92'
    shifts = TGWorkShift(url)
    shifts.modify()
    shifts.list_entries()
#    print(shifts)
#    storage = file.Storage('calendar' + '.dat')
#    credentials = storage.get()
#    http = credentials.authorize(http=httplib2.Http())
#    service = discovery.build('calendar', 'v3', http=http)
#
#    #  flow = client.flow_from_clientsecrets(
#    #      'client_secrets.json',
#    #      scope='https://www.googleapis.com/auth/calendar')
#
#    events = []
#    for date, text, start, end in shifts:
#        data = {
#            'summary': text,
#            'start': {'dateTime': '{}T{}:00.000+02:00'.format(date, start)},
#            'end': {'dateTime': '{}T{}:00.000+02:00'.format(date, end)},
#        }
#        e = service.events().insert(calendarId='primary', body=data)
#        print('{:<3} {}-{:<6} {}'.format(date.day, start, end, text))
#
#    while True:
#        proceed = raw_input('\nShould I continue? (y/n): ')
#        if proceed in ['y', 'n']:
#            break
#
#    if proceed == 'y':
#        for e in events:
#            pass
#            # e.execute()
#        print('Done!')
#    else:
#        print('Aborted!')
