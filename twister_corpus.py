from re import sub
from html.parser import HTMLParser
from urllib.request import urlopen


class TwisterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.twisters = []
        self.toggle = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p' and dict(attrs).get('class', None) == 'TXT':
            self.toggle = True
        else:
            self.toggle = False

    def handle_endtag(self, tag):
        self.toggle = False

    def handle_data(self, data):
        if self.toggle:
            self.twisters.append(data)
            self.toggle = False


def fetch_twisters():
    url = 'http://www.uebersetzung.at/twister/en.htm'
    parser = TwisterParser()
    parser.feed(urlopen(url).read().decode())
    return [sub(r'[".,!?]','',t) for t in parser.twisters]
