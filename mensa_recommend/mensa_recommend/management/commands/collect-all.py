import time
import traceback

from django.core.management import BaseCommand

from mensa_recommend.management.commands.collect import data_collectors
from mensa_recommend.source.data_collection.utils import Collector


class Command(BaseCommand):
    """
        The main command for preparing and scraping all types of data.
        Use collect.py for a more accurate access.
    """

    def handle(self, *args, **options):
        t = time.time()
        for key in data_collectors.keys():
            try:
                collector: Collector = data_collectors[key]

                self.stdout.write(f"Preparing '{key}'...")
                collector.prepare()

                self.stdout.write(f"Running '{key}'...")
                collector.run()
            except Exception as e:
                self.stderr.write(f"Got exception while handling collector "
                                  f"'{key}': {e}")
                self.stderr.write(traceback.format_exc())
        self.stdout.write(f"Done in {round(time.time() - t, 2)}s")
