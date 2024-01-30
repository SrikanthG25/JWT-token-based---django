from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException , AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from .models import Usermodel
from .serializers import UserSerializers
from .Authentication import create_access_token ,create_refresh_token , decode_acsess_token ,decode_refresh_token



# Create your views here.

class Register(APIView):
    def post(self,request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = Usermodel.objects.filter(email=email).first() 

        if user is None:
            raise APIException('User not found')
        
        if not user.check_password(password):
            raise APIException('Incorrect password')
        
        serializer = UserSerializers(user)
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        
        response = Response()
        response.set_cookie(key='refreshToken',value=refresh_token, httponly=True)
        response = {
            'token' : access_token
        }
        return response
    

class Userview(APIView):
    def get(self,request):
            user = get_authorization_header(request).split()

            if user and len(user) == 2:
                token = user[1].decode('utf-8')
                id = decode_acsess_token(token)
                user = Usermodel.objects.filter(pk=id).first()
                return Response(UserSerializers(user).data) 
            raise AuthenticationFailed('UnAuthorized to retry')

class Refresh(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })
    
class Logout(APIView):
    def post(self,_):
        response = Response()
        response.delete_cookie(key='refreshToken')
        response.data = {
            'message' : ' Logout Successfully '
        }

        return response

'''     
        payload ={
            'id' : user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # return Response({
        #     'jwt' : token
        #     })


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
            raise APIException('INVALID')
        
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise APIException('UnAuthenticated')
        
        user = Usermodel.objects.filter(id=payload['id']).first()
        serializer = UserSerializers(user)
        return Response(serializer.data)

class Logout(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : ' Logout Successfully '
        }

        return response
    
        
'''