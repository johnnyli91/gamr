from rest_framework import serializers
from social.models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('pk', 'bio', 'picture', 'gender', 'dob', 'location')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('pk', 'username', 'profile')


class ListPostSerializer(serializers.ModelSerializer):
    owner_info = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = (
            'pk',
            'owner_info',
            'text',
            'timestamp',
            'comment_count',
            'like_count',
            'group',
            'group_name'
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'owner_name', 'text', 'timestamp')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('pk', 'owner_name')


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'owner_name', 'text', 'post', 'timestamp')


class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('pk', 'owner_name', 'post')


class ViewPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    owner_info = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = (
            'pk',
            'owner_info',
            'text',
            'timestamp',
            'group',
            'group_name',
            'comments',
            'likes'
        )


class ViewGroupSerializer(serializers.ModelSerializer):
    posts = ListPostSerializer(many=True, read_only=True)
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = (
            'pk',
            'name',
            'owner',
            'description',
            'posts',
            'members'
        )


class ListGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'pk',
            'name',
            'owner_username',
            'description',
            'member_count'
        )


class UserInGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInGroup
        fields = ('owner', 'group')


class BasicGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name', 'description', 'member_count')


class UserWithGroupsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    groups = BasicGroupSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('pk', 'username', 'profile', 'groups')


