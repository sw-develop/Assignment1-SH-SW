from rest_framework import serializers

from article.models import Article, Comment, CComment


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = (
            'id',
            'username',
            'title',
            'content',
            'views',
        )

    def validate(self, data):
        if 'username' in data.keys():
            raise serializers.ValidationError({'username': 'Could not be modified'})
        return super(ArticleSerializer, self).validate(data)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'id',
            'username',
            'content',
        )

    def validate(self, data):
        if 'username' in data.keys():
            raise serializers.ValidationError({'username': 'Could not be modified'})
        return super(CommentSerializer, self).validate(data)


class CCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CComment
        fields = (
            'id',
            'username',
            'content',
        )

    def validate(self, data):
        if 'username' in data.keys():
            raise serializers.ValidationError({'username': 'Could not be modified'})
        return super(CCommentSerializer, self).validate(data)