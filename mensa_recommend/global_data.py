import os


production = os.getenv("PRODUCTION", "True") == "True"

if production:
    proxies = {
        'http': 'http://wwwproxy.uni-muenster.de:3128',
        'https': 'http://wwwproxy.uni-muenster.de:3128',
    }
else:
    proxies = {}
