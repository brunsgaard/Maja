# What is maja

maja is a small application/script that fetches data from a
[Doodle](http://doodle.com) and inserts the entries into a Google calender.
The approach is pretty naive for now, as regex are used to extract data
from the web page. A better solution would be to read the `xls` file, that
can be exported from doodle.com. I also have some concerns about the date
formats/parsing. 

Example of a run:  

```
(env)➜ Maja git:(master) ✗ python maja.py
1   16:00-21:30  Siv
2   16:00-21:30  Charlotte
6   16:00-21:30  Carina & Ida Bo
7   16:00-21:30  Malte & Rasmus
8   16:00-21:30  Maria, Christen, Janich & Lotten (16.15)
9   16:00-21:30  Emilie, Patricia, Paulina & Simone
11  13:00-17:00  Charlotte, Lasse Bo, Sigrid O & Christen
12  16:00-21:30  Anna, Sophie & Anna Bo
13  16:00-21:30  Luna, Jonas & Patricia
14  16:00-21:30  Simon, Sigrid O, Jonas & Kristoffer
15  16:00-21:30  Mathias, Simone & Anders
16  16:00-21:30  Sophie, Marta, Emilie & Ida Bo
20  16:00-21:30  Siv, Ida H & Katrine
21  16:00-21:30  Luna, Anna Bo, Maria & Kristoffer
22  16:00-21:30  Maja, Simon, Lotten (16.15) & Janich
23  16:00-21:30  Rasmus & Stine
25  13:00-17:00  Paulina, Anna, Stine & Therese
26  16:00-21:30  Lasse Bo & Therese
27  16:00-21:30  Marta, Katrine & Carina
28  16:00-21:30  Malte
30  16:00-21:30  Mathias, Anders & Ida H

Should I continue? (y/n):
```

# Run it
You need a file called `client_secrets.json` containing a
[google API client secret](https://developers.google.com/api-client-library/python/guide/aaa_client_secrets)
located in same folder as `maja.py`
