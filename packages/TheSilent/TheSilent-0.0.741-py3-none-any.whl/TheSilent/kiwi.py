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

    subdomains = ["adfs","aes","airwatch","alumni","ams","aplus","asg","atriuum","bbb","bcsdivanticsa","bes","bids","blocker","casarry","ccs","citrix","clinksso","clinkssoor","cobalt","collab-edge","compasslearning","d2l","designthefuture","destiny","dialin","discovervideo","docefill","documentservices","e2010","eaa","ecsinow","ecspowerschool","ees","eforms","email","ess","etcentral","etsts","exchange","expressway","falcon1","filewave","filter","fortis","ftp","helpdesk","hes","hhs","hms","hr","iboss","ibossreporter","inow","inowhome","intranet","jobapplications","kc","les","library","mail","mail2","mdm","mealapps","media","meet","moodle","mytime","nextgen","ns","ns1","ns2","nsa","nutrition","oldmail","parentportal","passwordreset","passwordresetregistration","payroll","pdexpress","portal","readydesk","res","rocket","security","sets","soara","spc","sso","sti","studentportal","support","technology","tes","transportation","vpn","webmail","websets","wiki","workorders","www"]

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
