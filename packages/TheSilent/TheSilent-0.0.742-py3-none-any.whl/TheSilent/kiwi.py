import random
import socket
import time
import urllib.parse
import TheSilent.puppy_requests as puppy_requests
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def kiwi(host,delay=0):
    clear()
    hits = []
    init_hosts = []
    hosts = []

    subdomains = ["adfs","analytics","autodiscover","barracuda","ckm","ckm01","ckr01","covid","covidash","destiny","eduphoria","exchange","expe","filter","forms","ftp","gp","hr","mail","mileage","ns1","ns2","old","portal","register","skyward","timeclock","transfinder","vpn","webmail"]

    subdomains = random.sample(subdomains,len(subdomains))
    for _ in subdomains:
        # check reverse dns
        print(CYAN + f"checking for reverse dns on {_}.{urllib.parse.urlparse(host).netloc}")
        dns_host = f"{_}.{urllib.parse.urlparse(host).netloc}"
        time.sleep(delay)
        try:
            hits.append(f"reverse dns {_}.{urllib.parse.urlparse(host).netloc}: {socket.gethostbyaddr(dns_host)}")
        except:
            pass
        try:
            data = puppy_requests.text(urllib.parse.urlparse(host).scheme + "://" + _ + "." + urllib.parse.urlparse(host).netloc)
            hits.append(f"found {_}.{urllib.parse.urlparse(host).netloc}")
        except:
            pass

    clear()
    hits.sort()
    for hit in hits:
        print(CYAN + hit)

    print(f"{len(hits)} results")
