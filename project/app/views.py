from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import student
from .serializers import sample, model_serializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins



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


@api_view(['GET','POST'])
def fun5(req):
    if req.method=='GET':
        d=student.objects.all()
        s=model_serializer(d,many=True)
        return Response(s.data)
    
    elif req.method=='POST':
        s=model_serializer(data=req.data)
        if s.is_valid():
            s.save()
            return JsonResponse(s.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(s.errors,status=status.HTT_40000_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def fun6(request,d):
    try:
        demo = student.objects.get(pk=d)
    except student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        s = model_serializer(demo)
        return Response(s.data)

    elif request.method == "PUT":
        s = model_serializer(demo, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        demo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class fun7(APIView):
    def get(self, request):
        demo = student.objects.all()
        s = model_serializer(demo, many=True)
        return Response(s.data)

    def post(self, request):
        s = model_serializer(data=request.data)
        if s.is_valid():
            s.save()
            return JsonResponse(s.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(s.errors, status=status.HTTP_400_BAD_REQUEST)

class fun8(APIView):
    def get(self, request, d):
        try:
            demo = student.objects.get(pk=d)
            s = model_serializer(demo)
            return Response(s.data)
        except student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, d):
        try:
            demo = student.objects.get(pk=d)
            s = model_serializer(demo, data=request.data)
            if s.is_valid():
                s.save()
                return Response(s.data)
            else:
                return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        except student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, d):
        try:
            demo = student.objects.get(pk=d)
            demo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class genericapiview(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = model_serializer
    queryset = student.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class update(generics.GenericAPIView,mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class = model_serializer
    queryset = student.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        return self.retrieve(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
