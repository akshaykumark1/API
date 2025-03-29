from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def fun2(request):
    """
    This function is used to handle GET request
    It will return all the data from the student model
    """
    if request.method == "GET":
        d = student.objects.all()
        s = sample(d, many=True)
        return JsonResponse(s.data, safe=False)
@csrf_exempt
def fun3(request):
    """
    This function is used to handle GET and POST request
    GET request will return all the data from the student model
    POST request will create a new student object
    """
    if request.method == "GET":
        d = student.objects.all()
        s = model_serializer(d, many=True)
        return JsonResponse(s.data, safe=False)
    elif request.method == "POST":
        """
        This function will create a new student object
        """
        d = JSONParser().parse(request)
        s = model_serializer(data=d)
        if s.is_valid():
            """
            This will save the new student object
            """
            s.save()
            return JsonResponse(s.data)
        else:
            """
            If the data is not valid then it will return the errors
            """
            return JsonResponse(s.errors)
@csrf_exempt
def fun4(request,d):   
    """
    This function is used to handle GET,PUT and DELETE request
    GET request will return a single student object
    PUT request will update a single student object
    DELETE request will delete a single student object
    """
    try:
        demo=student.objects.get(pk=d)
    except student.DoesNotExist:
        return HttpResponse('invalid')
    if request.method == "GET":
        s = model_serializer(demo)
        return JsonResponse(s.data)
    elif request.method == "PUT":
        d = JSONParser().parse(request)
        s = model_serializer(demo, data=d)
        if s.is_valid():
            s.save()
            return JsonResponse(s.data)
        else:
            return JsonResponse(s.errors)
    elif request.method == "DELETE":
        demo.delete()
        return HttpResponse('deleted')                     


@api_view(['GET', 'POST'])
def fun5(request):
    """
    This function is used to handle GET and POST request
    GET request will return all the data from the student model
    POST request will create a new student object
    """
    if request.method == "GET":
        d = student.objects.all()
        s = model_serializer(d.many=True)
        return Response(s.data)
    elif request.method == "POST":
        s = model_serializer(data=request.data) 
        if s.is_valid():
            s.save()
            return JsonResponse(s.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(s.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def fun6(request,d):
    try:
        demo=student.objects.get(pk=d)
    except student.DoesNotExist:
        return response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        s = model_serializer(demo)
        return Response(s.data)
    elif request.method == "PUT":
        s= model_seriazlizers(demo,data,request.data)
        is s.is_valid():
        s.save()
        return Response(s.data)
        else:
            return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        demo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
                    






                 