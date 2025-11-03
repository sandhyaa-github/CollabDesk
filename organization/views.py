from django.shortcuts import render
from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView

from organization.models import Organization, OrganizationMember
from organization.serializers import OrganizationSerializer
# Create your views here.


class OrganizationListCreateView(ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_queryset(self):
        return Organization.objects.filter(memberships__user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        org = serializer.save(created_by=self.request.user)
        OrganizationMember.objects.create(
            organization=org, user=self.request.user, role="admin")


class OrganizationDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict access to organizations where user is member or admin
        return Organization.objects.filter(memberships__user=self.request.user)
