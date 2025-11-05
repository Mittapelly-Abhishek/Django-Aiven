from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from . models import UsersTable
from . serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
import json
import cloudinary
import cloudinary.uploader
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
            id=req.POST.get("user_id")
            name=req.POST.get("user_name")
            email=req.POST.get("user_email")
            mobile=req.POST.get("user_mob")
            image=req.FILES.get("profile")

            img_url=cloudinary.uploader.upload(image)

            new_user=UsersTable.objects.create(user_id=id,user_name=name,user_email=email,user_mobile=mobile,profile_pic=img_url["secure_url"])

            return JsonResponse({"msg":"user created successfully","details":list(new_user.values())})
        
        except Exception as e:
            return JsonResponse({"error":str(e)},status=400)
    return JsonResponse({"error": "Only POST method is allowed"})


@csrf_exempt
def update_user(req, id):

    if req.method in ["PUT", "PATCH"]:
        try:
            single_user = UsersTable.objects.get(user_id=id)
        except UsersTable.DoesNotExist:
            return HttpResponse("User not found", status=404)

        try:
            user_data = json.loads(req.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        partial_update = True if req.method == "PATCH" else False

        serializer = UserSerializer(single_user, data=user_data, partial=partial_update)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse("User updated successfully", status=200)
        return JsonResponse(serializer.errors, status=400)

    return HttpResponse("Only PUT and PATCH methods are allowed", status=405)


@csrf_exempt   
def delete_user(req,id):
    if req.method=="DELETE":
        
        try:
            emp=UsersTable.objects.get(user_id=id)
        except UsersTable.DoesNotExist:
            return HttpResponse("user not found",status=404)
        emp.delete()
        return HttpResponse("user deleted successfully",status=204)
    else:
        return HttpResponse("only delete method is allowed")

