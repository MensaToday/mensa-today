# Data Collection

In order to collect data, you should make use of a so called `Collector` to read data from data sources like websites.
Any sort of *data collection* is only meant to update our databases. Therefore, if you need the collected data, you will
have to request it directly from our database afterwards.

## Execution

For any sort of data collector, you can create an instance of your required data collector and then call
the `collector.run()` method which invokes the entire procedure for requesting and saving data.

## Type implementation

Currently, there are **two options** for doing this. Both will extend the base class `Collector` for a more structural
access later on.

---

If you have **static website URLs** which should be scraped **without authentication**, the `NoAuthCollector` is the way
to go.

```python
from typing import List
from bs4 import BeautifulSoup
from utils import NoAuthCollector


class IMensaCollector(NoAuthCollector):
    def build_urls(self) -> List[str]:
        # Return list of urls which should be scraped separately
        return ["https://www.imensa.de/muenster/mensa-da-vinci/montag.html"]

    def scrape(self, document: BeautifulSoup) -> None:
        # Scrape document with BeautifulSoup library + Save data
        pass
```

---

For any other type of collector which e.g. requires URLs depending on each other or requires an entire different file
format, please extend the base `Collector` class and implement your stuff in the `run()` method.

```python
from utils import Collector


class LearnWeb(Collector):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def run(self) -> None:
        # Run authentication and requests + Save data
        pass
```

## Translating

Most data sources are in German and need to be translated into English. Therefore, all translations should be globally
maintained in our `translate.json` file. Keys should be stored in lower case. You can access those translations
via `utils.translate(key)`.