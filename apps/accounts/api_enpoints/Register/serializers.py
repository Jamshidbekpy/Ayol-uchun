from django.contrib.auth import get_user_model
from rest_framework import serializers
import re
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=False)
    phone = serializers.RegexField(
        regex=r'^\+998\d{9}$',
        error_messages={
            "invalid": "Phone number must start with '+998' and be 13 digits long."
        }
    )
    
    password = serializers.CharField(max_length=15, write_only=True)

    class Meta:
        model = User
        fields = ('phone', 'password')

    def validate_phone(self, value):
        # Allow only specific Uzbekistan codes
        if not re.match(r'^\+998(90|91|93|94|95|97|98|99|33|88)\d{7}$', value):
            raise serializers.ValidationError(
                "Only these codes are allowed: 90, 91, 93, 94, 95, 97, 98, 99, 33, 88."
            )
        return value

    def create(self, validated_data):
        # Password should be hashed
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ActivationSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')

        if not phone or not code:
            raise serializers.ValidationError("Phone and code are required.")

        return attrs