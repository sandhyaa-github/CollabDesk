from rest_framework import serializers

from organization.models import Organization, OrganizationMember


class OrganizationMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = OrganizationMember
        fields = ['id', 'user_email', 'user_name', 'role', 'joined_at']


class OrganizationSerializer(serializers.ModelSerializer):
    members = OrganizationMemberSerializer(
        source="memberships", many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'created_at', 'members']

    def create(self, validated_data):
        org = Organization.objects.create(**validated_data)
        return org
