from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, filters
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
import logging
from django_filters.rest_framework import DjangoFilterBackend

from common.utils import UserPagination, UserFilter
from user.serializers import UserSerializer

# Create your views here.

User = get_user_model()
logger = logging.getLogger('user')


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(
                "User registration failed for payload: %s", request.data)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = UserFilter

    def get(self, request):
        try:
            search = request.query_params.get('search')
            users = User.objects.all().exclude(is_superuser=True)
            if search:
                users = users.filter(
                    Q(username__icontains=search)
                    | Q(first_name__icontains=search)
                    | Q(email__icontains=search)
                )
            user_filter = UserFilter(request.query_params, queryset=users)
            users = user_filter.qs.distinct()

            ordering = request.query_params.get('ordering')
            if ordering:
                users = users.order_by(ordering)
            else:
                users = users.order_by('id')

            paginator = self.pagination_class()
            paginated_users = paginator.paginate_queryset(users, request)

            serializer = UserSerializer(paginated_users, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logger.exception("User list failed for payload: %s", request.data)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRetrieveUpdateDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(
                "User detail failed for payload: %s", request.data)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:

            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Exception as e:
            logger.exception(
                "User update failed for payload: %s", request.data)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Exception as e:
            logger.exception(
                "User update failed for payload: %s", request.data)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception(
                "User delete failed for payload: %s", request.data)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
