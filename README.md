# What is maja

maja is a small application/script that fetches data from a doodle and inserts
result in a Google calender. The approach for now is pretty simple as regex
are used to extract data from the website directly. A better solution would be
to read the `xls` file, that can be exported from doodle.com. I also have some
concerns about the date formats/parsing, right now the approch is very naive,
and small changes may break the app, again using the `xls` file 'may' resolve
this issue.

This code is work in progress, feel free to use it, but do not expect it to
work ;)

# Run it
You need a file called `client_secrets.json` containing a
[google API client secret](https://developers.google.com/api-client-library/python/guide/aaa_client_secrets)
located in same folder as `maja.py`
