import geoip2.database
import requests

def getIP(url):
    try:
        rsp = requests.get(url, stream=True)
        return rsp.raw._fp.fp.raw._sock.socket.getpeername()[0]
    except Exception:
        return None

def getGeoInfo(ip):
    if ip is not None:
        reader = geoip2.database.Reader('utils/GeoLite2-City.mmdb')
        response = reader.city(ip)
        return {"country" : response.country.name, "city" : response.city.name}
    else:
        return {"country" : "N/A", "city" : "N/A"}\


# def observe_geoip(self, req: UrlBasedRequest, mis: MissionStatus):
#     url = req.url
#     try:
#         rsp = requests.get(url, stream=True)
#         ip = rsp.raw._fp.fp.raw._sock.socket.getpeername()[0]
#         reader = geoip2.database.Reader('utils/GeoLite2-City.mmdb')
#         response = reader.city(ip)
#         return {"ip" : ip, "country" : response.country.name, "city" : response.city.name}
#     except Exception:
#         return {"ip" : "N/A", "country" : "N/A", "city" : "N/A"}

for i in [{"url" : "https://google.ca"}]:
    print(i["url"])
    i["ip"] = getIP(i["url"])
    geo_info = getGeoInfo(getIP(i["url"]))
    i["country"] = geo_info["country"]
    i["city"] = geo_info["city"]
    print(i)