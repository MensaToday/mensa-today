from mensa_recommend.source.data_collection.learnweb import (LearnWebCollector,
                                                             run)
from mensa_recommend.source.computations.decryption import decrypt

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def register(request):

    ziv_id = request.data['username']
    ziv_password = request.data['password']
    ziv_password = decrypt(ziv_password)

    user = request.user
