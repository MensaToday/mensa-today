from django.core.management.base import BaseCommand, CommandError, \
    CommandParser

from mensa_recommend.source.data_collection import imensa, learnweb, \
    room_mensa_distance
from mensa_recommend.source.data_collection.utils import Collector

data_collectors = {
    "imensa": imensa.IMensaCollector(),
    "room": learnweb.RoomCollector(),
    "room_mensa_distance": room_mensa_distance.RoomMensaDistanceCollector()
}


class Command(BaseCommand):
    """
        The main command for preparing and scraping data.
    """

    help = "Collect data through registered data collectors."

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("-s", "--source", required=True, type=str,
                            help="Select a specific data source collector for "
                                 "execution.")
        parser.add_argument(
            "-p", "--prepare", action="store_true",
            help="Setup specific collector.")

    def handle(self, *args, **options):
        source: str = options["source"].lower()
        prepare = options["prepare"]

        if source in data_collectors.keys():
            collector: Collector = data_collectors[source]

            if prepare:
                collector.prepare()
                self.stdout.write(
                    f"Successfully prepared data collector '{source}'.")
            else:
                collector.run()
                self.stdout.write(
                    f"Successfully ran data collector '{source}'.")
        else:
            raise CommandError(
                f"Unknown data source collector: '{source}'. "
                f"Available collectors: "
                f"{str.join(', ', list(data_collectors.keys()))}")
