#!/usr/bin/env python
import fileinput
import urllib
import urllib.request
import json
from lxml import etree
from lxml.cssselect import CSSSelector

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}
for username in fileinput.input():
    username = username.rstrip()
    url = "https://www.tiktok.com/@" + username
    print(url)
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
        parser = etree.HTMLParser()
        html_string = response.read()
        doc = etree.fromstring(html_string, parser)
        list = doc.cssselect("#__UNIVERSAL_DATA_FOR_REHYDRATION__")
        elt = list[0]
        json_string = elt.text
        data = json.loads(json_string)
        try:
            bioLink = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"]["bioLink"]["link"]
            print("    " + bioLink)
        except KeyError:
            html_filename = "tiktok-%s.html" % username
            json_filename = "tiktok-%s.json" % username
            with open(html_filename, "w") as f:
                f.write(str(html_string))
            print(">>> Wrote %s" % html_filename)
            with open(json_filename, "w") as f:
                f.write(json.dumps(data, indent=4))
            print(">>> Wrote %s" % json_filename)
