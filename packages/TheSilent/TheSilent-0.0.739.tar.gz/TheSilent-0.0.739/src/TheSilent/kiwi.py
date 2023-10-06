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

    directory_traversal = ["/admin/radeditorprovider/dialoghandler.aspx",
                           "/backend",
                           "/backup",
                           "/backup.sql",
                           "/cf/assets",
                           "/commodities.php?id=1",
                           "/config.txt",
                           "/conf.php",
                           "/default.rdp",
                           "/docker-compose.yml",
                           "/etc",
                           "/frameprop.htm",
                           "/global.asa",
                           "/inicis",
                           "/json-rpc",
                           "/jwks-rsa",
                           "/_layouts",
                           "/libraries/joomla/database",
                           "/MultiFileUpload.swf",
                           "/mutillidae"
                           "/nginx.conf",
                           "/package.json",
                           "/pass.txt",
                           "/php?id=1",
                           "/phpMyAdmin/index.php?server=1",
                           "/phpmyadmin/setup",
                           "/php?sql=select",
                           "/pki",
                           "/plugins/pie-register",
                           "/pom.xml",
                           "/private",
                           "/private.properties",
                           "/scada-vis",
                           "/source_code.zip",
                           "/sym404/root",
                           "/uux.aspx",
                           "/wp-config.txt",
                           "/wp-content/plugins",
                           "/wp-content/plugins/contact-form-7",
                           "/wp-content/plugins/elementor",
                           "/wp-content/plugins/simple-forum/admin",
                           "/wp-content/plugins/thecartpress",
                           "/wp-content/plugins/wp-e-commerce",
                           "/wp-content/plugins/wp-filebase/",
                           "/wp-content/themes/avada",
                           "/wp-content/themes/beach_apollo",
                           "/wp-content/themes/centum",
                           "/wp-content/themes/IncredibleWP",
                           "/wp-content/themes/striking_r",
                           "/wp-content/themes/ultimatum",
                           "/wp-content/uploads",
                           "/wp-content/uploads/sites",
                           "/wp-content/uploads/wcpa_uploads",
                           "/wp-content/uploads/wpo_wcpdf",
                           "/wp-includes",
                           "/wp-content/plugins/contact-form-7",
                           "/_vti_bin"]

    # prep work
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
            init_hosts.append(urllib.parse.urlparse(host).scheme + "://" + _ + "." + urllib.parse.urlparse(host).netloc)
        except:
            pass
        

    # more prep work
    for host in init_hosts:
        for _ in directory_traversal:
            hosts.append(f"{host}{_}")
            hosts.append(f"{host}/.{_}")
            hosts.append(f"{host}/./.{_}")
            hosts.append(f"{host}/././.{_}")
            hosts.append(f"{host}/./././.{_}")
            hosts.append(f"{host}/././././.{_}")
            hosts.append(f"{host}/./././././.{_}")
            hosts.append(f"{host}/././././././.{_}")
            hosts.append(f"{host}/./././././././.{_}")
            hosts.append(f"{host}/././././././././.{_}")
            hosts.append(f"{host}/./././././././././.{_}")

    hosts = random.sample(hosts,len(hosts))

    for host in hosts:
        print(CYAN + f"checking {host}")
        time.sleep(delay)
        try:
            data = puppy_requests.text(host)
            hits.append(host)
        except:
            pass

    clear()
    for hit in hits:
        print(CYAN + hit)

    print(f"{len(hits)} results")
