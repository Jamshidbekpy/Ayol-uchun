from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class PhoneLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            user = authenticate(request=self.context.get('request'), username=phone, password=password)
            if not user:
                raise serializers.ValidationError(_("Invalid phone or password."))
            if not user.is_active:
                raise serializers.ValidationError(_("User account is inactive."))
        else:
            raise serializers.ValidationError(_("Must include 'phone' and 'password'."))

        attrs['user'] = user
        return attrs
