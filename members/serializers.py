from rest_framework import serializers
from .models import TeamMember

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

    def validate_phone(self, value):
        # Ensure the phone number contains only digits.
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value
