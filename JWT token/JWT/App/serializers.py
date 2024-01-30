from rest_framework import serializers
from .models import Appmodel

class AppSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appmodel
        fields = '__all__'
        extra_kwargs ={
            'password' : {'write_only':True}
        }


    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance