from rest_framework import serializers
from apps.accounts.utils import send_sms_code, check_code

class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def create(self, validated_data):
        send_sms_code(validated_data['phone'])
        return validated_data

class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        phone = data['phone']
        code = data['code']
        is_valid, message = check_code(phone, code)
        if not is_valid:
            raise serializers.ValidationError(message)
        return data
