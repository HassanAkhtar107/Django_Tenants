from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
# from django.db.models import Count, Max, Sum
from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer, ClientSerializer
import logging
logger = logging.getLogger(__name__)
from .models import User, Client
from rest_framework import permissions
from django.db import connection
from rest_framework.exceptions import PermissionDenied

class SignupView(generics.GenericAPIView):
    """
    API endpoint for user signup
    """
    
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # if connection.schema_name == "public":
        #     raise PermissionDenied("SignUp not allowed on public domain")
        
        logger.info(f"requestData:{request}")
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    # 'schema_name':request.schema_name,
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Signup failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    """
    API endpoint for user login
    """

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid input',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
      
        user = authenticate(request, email=email, password=password)
        logger.info(f"user: {user}")
        if user is None:
            return Response({
                'error': 'User is not logged in',
                'message': 'Invalid credentials. Please check your email and password.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        tokens = self.get_tokens_for_user(user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_200_OK)

class ProfileView(generics.GenericAPIView):
    """
    API endpoint to get authenticated user profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({
            'user': serializer.data
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    API endpoint for user logout
    """
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({
            "message": "Logged out successfully"
        }, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]
    queryset = User.objects.all()

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        instance=self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "error": "Update failed",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ClientList(generics.ListAPIView):
    serializer_class=ClientSerializer
    permission_classes=[IsAuthenticated, permissions.IsAdminUser]
    queryset=Client.objects.all()



# class CompanyAddView(generics.CreateAPIView):
#     serializer_class=CompanySerializer
#     permission_classes=[AllowAny]
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Request data: {request.data}")
#         serilizer = self.get_serializer(data=request.data)
#         if serilizer.is_valid():
#             serilizer.save()
#             return Response({
#                 "message":"Company added successfully",
#                 "company":serilizer.data
#             }, status=status.HTTP_201_CREATED)

# class BranchesAddView(generics.CreateAPIView):
#     serializer_class=BranchesSerializer
#     permission_classes=[AllowAny]
#     def post(self, request, *args, **kwargs):
#         serilizer=self.get_serializer(data=request.data)
#         if serilizer.is_valid():
#             serilizer.save()
#             return Response({
#                 "message":"Branch added successfully",
#                 "branch":serilizer.data
#             }, status=status.HTTP_201_CREATED)

# class CompinesBranchesData(generics.ListAPIView):
#     serializer_class=CompanySerializer
#     permission_classes=[AllowAny]
#     queryset=Company.objects.prefetch_related('branches').all()
#     def get(self, request, *args, **kwargs):
#         serializer=self.get_serializer(self.get_queryset(), many=True)
#         return Response({
#             "data":serializer.data
#         }, status=status.HTTP_200_OK)

# class DelCompanies(generics.DestroyAPIView):
#     permission_classes = [AllowAny]
#     queryset = Company.objects.all()
#     def delete(self, request, *args, **kwargs):
#         instance=self.get_object()
#         instance.delete()
#         return Response({
#             "message":"Company deleted successfully",
#             "Delete": instance.id
#         }, status=status.HTTP_200_OK)

# class DelBranch(generics.DestroyAPIView):
#     permission_classes = [AllowAny]
#     queryset = CompanyBranches.objects.all()
#     def delete(self, request, *args, **kwargs):
#         instance=self.get_object()
#         instance.delete()
#         return Response({
#             "message":"Branch deleted successfully",
#             "Delete": instance.id
#         }, status=status.HTTP_200_OK)

# class BooksAddView(generics.CreateAPIView):
#     serializer_class=BookSerializer
#     permission_classes=[AllowAny]
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Request data: {request.data}")
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message":"Book added successfully",
#                 "book":serializer.data
#             }, status=status.HTTP_201_CREATED)

# class AutherAddView(generics.CreateAPIView):
#     serializer_class=AutherSerializer
#     permission_classes=[AllowAny]
#     def post(self, request, *args, **kwargs):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message":"Auther added successfully",
#                 "book":serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             "error":"Auther addition failed",
#             "details":serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

# class BooksListView(generics.ListAPIView):
#     serializer_class=BookSerializer
#     permission_classes=[AllowAny]
#     queryset=Books.objects.all()
#     def get(self, request, *args, **kwargs):
#         serializer=self.get_serializer(self.get_queryset(), many=True)
#         logger.info(f"Books List: {serializer.data}")
#         return Response({
#             "data":serializer.data
#         }, status=status.HTTP_200_OK)

# class AutherListView(generics.ListAPIView):
#     serializer_class=AutherSerializer
#     permission_classes=[AllowAny]
#     queryset=Author.objects.all()
#     def get(self, request, *args, **kwargs):
#         serializer=self.get_serializer(self.get_queryset(), many=True)
#         return Response({
#             "data":serializer.data
#         }, status=status.HTTP_200_OK)

# class ValuesAddView(generics.CreateAPIView):
#     serializer_class=valuesSerializer
#     permission_classes=[AllowAny]
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Request data: {request.data}")
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message":"Value added successfully",
#                 "value":serializer.data
#             }, status=status.HTTP_201_CREATED)

# class ValuesListView(generics.ListAPIView):
#     serializer_class=valuesSerializer
#     permission_classes=[AllowAny]
#     queryset=Values.objects.all()
#     def get_queryset(self):
#         return Values.objects.annotate(sum_val=Count('value'))
    
#     def get(self, request, *args, **kwargs):
#         serializer=self.get_serializer(self.get_queryset(), many=True)
#         aggregation=Values.objects.aggregate(sum_val=Sum('value'))
#         return Response({
#             "data":serializer.data,
#             "aggregation":aggregation
#         }, status=status.HTTP_200_OK)
