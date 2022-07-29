from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from super_types.models import SuperType
from .serializers import SupersSerializer
from .models import Super

@api_view(['GET', 'POST'])
def super_list(request):

    if request.method == 'GET':

        queryset = Super.objects.all()

        heroes = queryset.filter(super_type__type = "Hero")
        villains = queryset.filter(super_type__type = "Villain")

        heroes_serializer = SupersSerializer(heroes, many=True)
        villains_serializer = SupersSerializer(villains, many=True)

        if request.query_params.get('type') == 'hero':
            custom_response = heroes_serializer.data
        elif request.query_params.get('type') == 'villain':
            custom_response = villains_serializer.data
        else:
            custom_response = {
            'Heroes': heroes_serializer.data,
            'Villains': villains_serializer.data
            
                
            }
        return Response(custom_response)

    elif request.method == 'POST':
        serializer = SupersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def super_detail(request, pk):
    super = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SupersSerializer(super)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SupersSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
