import os


proxy = os.getenv("PROXY", "False") == "True"

if proxy:
    proxies = {
        'http': 'http://wwwproxy.uni-muenster.de:3128',
        'https': 'http://wwwproxy.uni-muenster.de:3128',
    }
else:
    proxies = None
