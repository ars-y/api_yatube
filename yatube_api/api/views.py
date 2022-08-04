from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend


from posts.models import Post, Group, User
from api.serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer
)
from api.permissions import AuthorOrReadOnly
from api.paginations import PostPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AuthorOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = (
        'user__username',
        'following__username',
    )

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
