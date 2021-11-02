
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from article.models import Article, Comment, CComment, ViewLog
from article.serializers import ArticleSerializer, CommentSerializer, CCommentSerializer


class ArticleViewSet(viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated(), ]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny(), ]
        return self.permission_classes

    def create(self, request):
        """
        POST /articles/
        data params
        - title(required)
        - content(required)
        - category_id(required)
        """
        data = request.data
        #  if request.user.is_anonymous:
        #     raise NotAuthenticated
        if not data['title'] or not data['content'] or not data['category_id']:
            return Response({"error": "title, content, category_id are required field."},
                            status=status.HTTP_400_BAD_REQUEST)

        category = get_object_or_404(Article, id=data['category_id'])
        article = Article.objects.create(title=data['title'], content=data['content'], category_id=category.id,
                                         username=request.user.username)
        return Response(self.get_serializer(article).data)

    def list(self, request):
        """
        GET /articles/
        query params
        -content
        -title
        """
        content = request.query_params.get('content')
        title = request.query_params.get('title')
        searching_options = dict()
        if content is not None:
            searching_options['content__icontains'] = content
        if title is not None:
            searching_options['title__icontains'] = title

        articles = Article.objects.filter(**searching_options)
        paginator = self.paginator
        paginated_posts = paginator.paginate_queryset(articles, request)
        return paginator.get_paginated_response(self.get_serializer(paginated_posts, many=True).data)

    def retrieve(self, request, pk):
        """
        GET /articles/{article_id}/
        """
        article = get_object_or_404(Article, id=pk)
        if not request.user.is_anonymous:
            _, is_created = ViewLog.objects.get_or_create(user_id=request.user.id, article_id=pk)
            if is_created:
                article.views += 1
                article.save()

        rtn = self.get_serializer(article).data
        return Response(rtn)

    def partial_update(self, request, pk):
        """
        PATCH /posts/{post_id}/
        """
        article = get_object_or_404(Article, id=pk)
        if article.username != request.user.username:
            raise PermissionDenied
        serializer = self.get_serializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(article, serializer.validated_data)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """
        DELETE /posts/{post_id}/
        """
        article = get_object_or_404(Article, id=pk)
        if article.username != request.user.username:
            raise PermissionDenied
        article.delete()
        return Response('{article deleted}')

    @action(detail=True, methods=['POST', 'GET'])
    def comments(self, request, pk):
        """
        POST /articles/{article_id}/comments/
        data params
        - content(required)
        """
        if request.method == 'POST':
            content = request.data['content']

            if not content:
                return Response({"error": "content required field."},
                                status=status.HTTP_400_BAD_REQUEST)

            comment = Comment.objects.create(username=request.user.username, content=content, article_id=pk)
            return Response(status=status.HTTP_201_CREATED)

        if request.method == 'GET':
            comments = Comment.objects.filter(article_id=pk)
            paginator = self.paginator
            paginated_comments = paginator.paginate_queryset(comments, request)
            return paginator.get_paginated_response(CommentSerializer(paginated_comments, many=True).data)


class CommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated(), ]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny(), ]
        return self.permission_classes

    def destroy(self, request, pk):
        """
        DELETE /comments/{comment_id}/
        """
        comment = get_object_or_404(Comment, id=pk)
        if comment.username != request.user.username:
            raise PermissionDenied
        comment.delete()
        return Response('{comment deleted}')

    @action(detail=True, methods=['POST', 'GET'])
    def ccomments(self, request, pk):
        """
        POST /comments/{comment_id}/ccomments/
        data params
        - content(required)
        """
        if request.method == 'POST':
            content = request.data['content']

            if not content:
                return Response({"error": "content required field."},
                                status=status.HTTP_400_BAD_REQUEST)

            ccomment = CComment.objects.create(username=request.user.username, content=content, comment_id=pk)
            return Response(status=status.HTTP_201_CREATED)

        if request.method == 'GET':
            ccomments = CComment.objects.filter(comment_id=pk)
            paginator = self.paginator
            paginated_ccomments = paginator.paginate_queryset(ccomments, request)
            return paginator.get_paginated_response(CCommentSerializer(paginated_ccomments, many=True).data)


class CCommentViewSet(viewsets.GenericViewSet):
    queryset = CComment.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated(), ]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny(), ]
        return self.permission_classes

    def destroy(self, request, pk):
        """
        DELETE /ccomments/{ccomment_id}/
        """
        ccomment = get_object_or_404(CComment, id=pk)
        if ccomment.username != request.user.username:
            raise PermissionDenied
        ccomment.delete()
        return Response('{ccomment deleted}')
