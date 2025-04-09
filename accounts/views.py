from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, UserLoginSerializer 
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from rest_framework.authtoken.models import Token
# from projects.permissions import IsNotAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from marketing_executives.models import MarketingExecutive
from hospital_authorities.models import HospitalAuthority



class UserRegistrationApiView(APIView):    
    # permission_classes = [IsNotAuthenticated]
    serializer_class = RegistrationSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"https://hormone-lab-backend.vercel.app/accounts/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({'detail': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://hormonelab.vercel.app/login')
    else:
        return Response({'detail': 'Activation failed. The link may be invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id, 'username': username})
            else:
                return Response({'error': "Invalid Credential"})
        
        return Response(serializer.errors) 

@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def user_details(request): 
    user = request.user 
    data = { 
        'user_id': user.id, 
        'username': user.username, 
        'email': user.email, 
        'first_name': user.first_name, 
        'last_name': user.last_name, 
    } 
    
    # Attempt to get HospitalAuthority details 
    try: 
        ha = HospitalAuthority.objects.get(user=request.user) 
        data['ha'] = ha.id 
    except HospitalAuthority.DoesNotExist: 
        data['ha'] = None 
        
    
    # Attempt to get MarketingExecutive details 
    try: 
        me = MarketingExecutive.objects.get(user=request.user) 
        data['me'] = me.id
    except MarketingExecutive.DoesNotExist: 
        data['me'] = None 
    
    return Response(data)



@api_view(['DELETE'])
def delete_user_and_related(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Delete token if exists
    Token.objects.filter(user=user).delete()

    # Delete related hospital authority if exists
    HospitalAuthority.objects.filter(user=user).delete()

    # Delete related marketing executive if exists
    MarketingExecutive.objects.filter(user=user).delete()

    # Finally, delete the user
    user.delete()

    return Response({"message": f"User {user_id} and related data deleted."}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def all_users_details(request):
    # Get all users
    users = User.objects.all()

    user_data = []
    
    # Iterate over each user and collect details
    for user in users:
        data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        # Check if the user is a HospitalAuthority
        try:
            ha = HospitalAuthority.objects.get(user=user)
            data['ha'] = ha.id
        except HospitalAuthority.DoesNotExist:
            data['ha'] = None

        # Check if the user is a SkillCrafter
        try:
            me = MarketingExecutive.objects.get(user=user)
            data['me'] = me.id
        except MarketingExecutive.DoesNotExist:
            data['me'] = None

        # Append the user data to the list
        user_data.append(data)

    return Response(user_data)



@api_view(['GET']) 
def userid_details(request, user_id):
    try:
        # Fetch user by ID
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=404)

    # Prepare response data
    data = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    # Attempt to get HospitalAuthority details
    try:
        ha = HospitalAuthority.objects.get(user=user)
        data['ha'] = ha.id
    except HospitalAuthority.DoesNotExist:
        data['ha'] = None

    # Attempt to get MarketingExecutive details
    try:
        me = MarketingExecutive.objects.get(user=user)
        data['me'] = me.id
    except MarketingExecutive.DoesNotExist:
        data['me'] = None

    return Response(data)



class UserLogoutApiView(APIView):
    def get(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass
        logout(request)
        
        return redirect('login')