from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User
from .serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser




@api_view(['GET'])
def getData(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    json = JSONRenderer().render(serializer.data)
    return Response(serializer.data)

@api_view(['POST'])
def addData(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
