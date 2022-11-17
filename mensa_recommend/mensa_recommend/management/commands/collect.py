from django.core.management.base import BaseCommand, CommandError, CommandParser

from mensa_recommend.source.data_collection import imensa

from mensa_recommend.source.data_collection.utils import Collector


class Command(BaseCommand):
    help = "Collect data through registered data collectors."
    data_collectors = {
        "imensa": imensa.IMensaCollector()
    }

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("-s", "--source", required=True, type=str,
                            help="Select a specific data source collector for execution.")
        parser.add_argument("-p", "--prepare", action="store_true", help="Setup specific collector.")

    def handle(self, *args, **options):
        source: str = options["source"].lower()
        prepare = options["prepare"]

        if source in self.data_collectors.keys():
            collector: Collector = self.data_collectors[source]

            if prepare:
                collector.prepare()
                self.stdout.write(f"Successfully prepared data collector '{source}'.")
            else:
                collector.run()
                self.stdout.write(f"Successfully ran data collector '{source}'.")
        else:
            raise CommandError(
                f"Unknown data source collector: '{source}'. "
                f"Available collectors: {str.join(', ', list(self.data_collectors.keys()))}")
