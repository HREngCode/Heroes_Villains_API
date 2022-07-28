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
        super_type_class = request.query_params.get('super_types')
        queryset = Super.objects.all()
        if super_type_class:
            queryset = queryset.filter(super_type__type=super_type_class)
        else:
            super_type = SuperType.objects.all()
            super_type_dictionary = {}

            for super_type in super_type:
                supers = Super.objects.filter(super_type__type=super_type.id)
                supers_serializer = SupersSerializer(supers, many=True)
                super_type_dictionary[super_type.type] = {
                    "supers": supers_serializer.data
                }
            return Response(super_type_dictionary)
        serializer = SupersSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
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
