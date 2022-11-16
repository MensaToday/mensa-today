import sys
from utils import Collector
from imensa import IMensaCollector
import imensa

if __name__ == "__main__":
    if len(sys.argv) > 0:
        if sys.argv[0] == "collect":
            if len(sys.argv) < 2:
                raise Exception("Unknown collector type: None")

            collector_type = sys.argv[1]
            collector: Collector

            if collector_type == "mensa":
                collector = IMensaCollector()
            else:
                raise Exception(f"Unknown collector type: {collector_type}")

            collector.run()
        if sys.argv[0] == "setup":
            imensa.insert_static()
