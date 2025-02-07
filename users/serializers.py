from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone_number',
                  'address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'address_line1': {'required': True},
            'city': {'required': True},
            'state': {'required': True},
            'country': {'required': True},
            'postal_code': {'required': True},
        }

    def validate(self, data):
        # Add any additional field-level validations here
        if data.get('address_line1') and len(data['address_line1']) < 5:
            raise serializers.ValidationError({
                'address_line1': 'Address must be at least 5 characters long'
            })

        if data.get('postal_code') and not data['postal_code'].strip():
            raise serializers.ValidationError({
                'postal_code': 'Postal code cannot be empty'
            })

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            address_line1=validated_data.get('address_line1', ''),
            address_line2=validated_data.get('address_line2', ''),
            city=validated_data.get('city', ''),
            state=validated_data.get('state', ''),
            country=validated_data.get('country', ''),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
