from urllib.request import Request, urlopen

def get_txt(url, tag):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    file = urlopen(req)
    file.readline()
    # return [{"url" : i, "domain" : i.split("/")[2], "tag" : tag} for line in file if (i := line.decode("utf-8").strip())]
    return [{"url" : i, "domain" : i.split("/")[2], "tag" : tag} for i in (line.decode("utf-8").strip() for line in file) if i]


def get_vetted():
    url = "https://blacklist.cyberthreatcoalition.org/vetted/url.txt"
    return get_txt(url, "vetted")
def get_unvetted():
    url = "https://blacklist.cyberthreatcoalition.org/unvetted/url.txt"
    return get_txt(url, "unvetted")
def get_data():
    return get_vetted() + get_unvetted()

# print(get_data()[1])