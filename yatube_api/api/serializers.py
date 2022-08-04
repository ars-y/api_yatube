from rest_framework import serializers

from posts.models import Post, Comment, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=('user', 'following',)
        )
    ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                {
                    'follower': ('Нельзя подписаться на себя самого.')
                }
            )
        return data

    class Meta:
        model = Follow
        fields = '__all__'
