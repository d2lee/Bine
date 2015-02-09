from rest_framework import  serializers
from django.contrib.auth import update_session_auth_hash
from bine.models import User, Book, BookNote

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'fullname', 'email', 'birthday', 'sex', 'tagline', 
                  'created_at', 'updated_on', 'password', 'confirm_password')
        read_only_fields = ('created_at', 'updated_on',)
        
        def create(self, validated_data):
            return User.objects.create(**validated_data)
        
        def update(self, instance, validated_data):
            instance.email = validated_data.get('email', instance.username)
            instance.fullname = validated_data.get('fullname', instance.fullname)
            instance.birthday = validated_data.get('birthday', instance.birthday)
            instance.sex = validated_data.get('sex', instance.sex)
            instance.tagline = validated_data.get('tagline', instance.tagline)
            
            instance.save()
            
            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)
            
            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()               
                update_session_auth_hash(self.context.get('request'), instance)
            
            return instance

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'fullname')
        
class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'photo')

class BookNoteSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    book = BookSimpleSerializer(read_only=True)
    
    class Meta:
        model = BookNote
        fields = ('id', 'user', 'book', 'content', 'read_date_from', 'read_date_to', 'preference', 
                  'attach', 'share_to', 'created_at', 'updated_on')
    
    
    