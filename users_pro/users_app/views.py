from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from . models import UsersTable
from . serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def get_users(req):
    data=UsersTable.objects.all()
    all_users=UserSerializer(data,many=True)
    return JsonResponse({"all_users":all_users.data})

def get_user(req,id):
    try:
        single_user=UsersTable.objects.get(user_id=id)
        serializer=UserSerializer(single_user)
        return JsonResponse({"user_data":serializer.data})
    
    except UsersTable.DoesNotExist:
        return HttpResponse("user not found",status=404)


@csrf_exempt
def reg_user(req):
    if req.method == "POST":
        try:
            user_data=json.loads(req.body)
            serializer=UserSerializer(data=user_data)
            if serializer.is_valid():  
                serializer.save()
                return JsonResponse({"message": "User created successfully"}, status=201)
            
            return JsonResponse(serializer.errors, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Only POST method is allowed"})

