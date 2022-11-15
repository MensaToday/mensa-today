import sys
from utils import Collector
from imensa import IMensaCollector

if __name__ == "__main__":
    collector_type = sys.argv[0]
    collector: Collector

    if collector_type == "mensa":
        collector = IMensaCollector()
    else:
        raise Exception(f"Unknown collector type: {collector_type}")

    collector.run()
