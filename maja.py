import requests
import re
import json
from collections import defaultdict
import sys
from datetime import date
from oauth2client import client
from googleapiclient import sample_tools


def parse_date(datestring):
    m, d, y = map(int, datestring[3:].split('/'))
    return date(y + 2000, m, d)


url = 'http://doodle.com/4qeiacg36ppi3h92'
resp = requests.get(url)

pattern = '.*extend\(true, doodleJS.data, ({"poll":.*})\);'
match = re.search(pattern, resp.text)

data = json.loads(match.groups()[0])

options = data['poll']['optionsText']
options = [parse_date(d) for d in options]

dates_from_s = lambda s: [d for (d, p) in zip(options, s) if p == 'y']
d = {e['name']: dates_from_s(e['preferences']) for e in data['poll']['participants']}

res = defaultdict(list)
for k, v in d.iteritems():
    for date in v:
        res[date].append(k)



#TODO: Replace init wth proper solution
service, flags = sample_tools.init(
    sys.argv, 'calendar', 'v3', __doc__, __file__,
    scope='https://www.googleapis.com/auth/calendar')

#TODO: start/end time saterdays
for date, names in res.iteritems():

  event = {
    'summary': ' &'.join(', '.join(names).rsplit(',', 1)) ,
    'start': {
            'dateTime': str(date)+ 'T16:00:00.000+02:00',
            },
    'end': {
            'dateTime': str(date) + 'T21:30:00.000+02:00',
            },
  }

  e = service.events().insert(calendarId='primary', body=event).execute()
