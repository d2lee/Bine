from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash

from bine.models import User, Book, BookNote, BookNoteReply


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


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
        read_only_fields = ('username', 'fullname')


class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'photo')
        read_only_fields = ('title', 'photo')


class BookNoteSerializerMixin(object):
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookNoteViewSerializer
        else:
            return BookNoteWriteSerializer


class BookNoteViewSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    book = BookSimpleSerializer()

    class Meta:
        model = BookNote
        fields = ('id', 'user', 'book', 'content', 'read_date_from', 'read_date_to', 'preference',
                  'likeit', 'attach', 'share_to', 'created_at', 'updated_on')


class BookNoteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNote
        fields = ('id', 'user', 'book', 'content', 'read_date_from', 'read_date_to', 'preference',
                  'attach', 'share_to')


class BookNoteReplySerializerMixin(object):
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookNoteReplyViewSerializer
        else:
            return BookNoteReplyWriteSerializer


class BookNoteReplyViewSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = BookNoteReply
        fields = ('id', 'user', 'content', 'created_at')


class BookNoteReplyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNoteReply
        fields = ('book', 'user', 'content')