from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SupersSerializer
from .models import Super

@api_view(['GET'])
def super_list(request):
    super = Super.objects.all()

    serializer = SupersSerializer(super, many=True)

    return Response(serializer.data)