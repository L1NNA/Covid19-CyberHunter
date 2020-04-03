from urllib.request import Request, urlopen
import re
import whois
import socket

GOV_LIST = [".gov", "cic", ".ca", "cic", "cra", "canada", ".edu"]

def get_txt(url, tags):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    file = urlopen(req)
    res = []
    for line in file:
        i = line.decode("utf-8").strip()
        if i[0] !="#":
            m = re.search('https?://([A-Za-z_0-9.-]+).*', i)
            ip = "N/A"
            web_url = "N/A"
            domain = i
            domain_info = {}
            tmp = {}
            if m:
                domain = m.group(1)
                web_url = i
            try:
                domain_info = whois.whois(domain).__dict__
                ip = socket.gethostbyname(i)
                pass
            except Exception:
                pass

            tmp = {"url" : web_url, "domain" : domain, "tag" : tags, "whois" : domain_info, "ip" : ip}
            if "good" in tags and any(substring in i for substring in GOV_LIST):
                tmp["tag"] = tags + ["offical"]
            elif "good" in tags:
                tmp["tag"] = tags + ["other"]
            res.append(tmp)

    return res


    # return [{"url" : i, "domain" : i.split("/")[2], "tag" : tag} for line in file if (i := line.decode("utf-8").strip())]
    # return [{"url" : i, "domain" : i.split("/")[2], "tag" : tags} for i in (line.decode("utf-8").strip() for line in file) if i]


def get_vetted():
    url = "https://blacklist.cyberthreatcoalition.org/vetted/url.txt"
    return get_txt(url, ["bad", "vetted"])
def get_unvetted():
    url = "https://blacklist.cyberthreatcoalition.org/unvetted/url.txt"
    return get_txt(url, ["bad", "unvetted"])

def get_good():
    url = "https://raw.githubusercontent.com/Cyber-Threat-Coalition/goodlist/master/hostnames.txt"
    return get_txt(url, ["good"])

def get_data():
    return get_vetted() + get_unvetted()

print(get_good())