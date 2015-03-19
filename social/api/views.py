from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLogin
from rest_framework.response import Response
from social.permissions import IsOwnerOrReadOnly
from social.api.serializers import *


class FacebookLogin(SocialLogin):
    adapter_class = FacebookOAuth2Adapter


class RetrieveCurrentUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        data = User.objects.filter(username=self.request.user)
        return HttpResponse(data)


class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithGroupsSerializer


class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithGroupsSerializer


@login_required()
@api_view(['GET', 'POST'])
def MyProfile(request):
    if request.method == 'POST':
        s = request.user.profile
        s.bio = request.data['bio']
        s.save()
        return Response({'bio': request.data['bio']})
        # request.query_params
    else:
        bio = request.user.profile.bio
        return Response({'bio': bio})


class ListCreatePost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = ListPostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class RetrieveUpdateDestroyPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = ViewPostSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CreateComment(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class RetrieveUpdateDestroyComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ListCreateGroup(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = ListGroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class RetrieveUpdateDestroyGroup(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = ViewGroupSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CreateUserInGroup(generics.CreateAPIView):
    queryset = UserInGroup.objects.all()
    serializer_class = UserInGroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    # def perform_create(self, serializer, **kwargs):
    #     group = self.request.QUERY_PARAMS.get(self.request.data['group_id'])
    #     serializer.save(user = self.request.user, group = group)


class Feed(generics.ListAPIView):
    serializer_class = ListPostSerializer

    def get_queryset(self):
        user = self.request.user
        groups = user.groups
        posts = Post.objects.filter(group__members = user)
        print posts[0]
        return posts
# @login_required()
# @api_view(['GET'])
# def CreateUserInGroup(request):
#
#     m = request
#
#     if request.method == 'POST':
#         s = request.user.profile
#         s.bio = request.data['bio']
#         s.save()
#         return Response({'bio': request.data['bio']})
#         # request.query_params
#     else:
#         bio = request.user.profile.bio
#         return Response({'bio': bio})
