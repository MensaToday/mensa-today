from .utils import Collector
import itertools
from courses.models import Room, RoomMensaDistance
from mensa.models import Mensa
from ..computations.distance_computation import haversine


class RoomMensaDistanceCollector(Collector):
    def prepare(self) -> None:
        pass

    def run(self) -> None:
        self.__mensa_room_distance()

    def __mensa_room_distance(self):
        """Calculate the distance between each room and each mensa and save the
        result into the database

        """
        # Get rooms and mensen out of the database
        rooms = Room.objects.all()
        mensen = Mensa.objects.all()

        # Create the cartesian product between rooms and mensa
        # and iterate over each combination
        for room, mensa in itertools.product(rooms, mensen):

            # Check if lon and lat is not None
            if room.lon and room.lat and mensa.lon and mensa.lat:
                # Calculate distance
                distance = haversine(room.lon, room.lat, mensa.lon, mensa.lat)

                # Save distance between room and mensa
                room_distance = RoomMensaDistance(
                    room=room, mensa=mensa, distance=distance)
                room_distance.save()
