from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Appmodel
from .serializers import AppSerializers
import jwt
import datetime



# Create your views here.

class Register(APIView):
    def post(self,request):
        serializer = AppSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class Login(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = Appmodel.objects.filter(email=email).first() 

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload ={
            'id' : user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        '''
        return Response({
            'jwt' : token
            })
        '''

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    
class Userview(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('INVALID')
        
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated')
        
        user = Appmodel.objects.filter(id=payload['id']).first()
        serializer = AppSerializers(user)
        return Response(serializer.data)

class Logout(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : ' Logout Successfully '
        }

        return response
    