from django.shortcuts import render
from rest_framework import status, viewsets
# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from article.models import Article, Category
from article.serializers import ArticleSerializer


class ArticleViewSet(viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
            return Response({"error": "title and content are required field."}, status=status.HTTP_400_BAD_REQUEST)
        category = get_object_or_404(Category, id=data['category_id'])
        article = Article.objects.create(title=data['title'], content=data['content'], category=category, user=request.user)
        return Response(self.get_serializer(article).data)

    def list(self, request):
        """
        GET /posts/
        query params
        - offset
        - limit
        """
        posts = Post.objects.all()
        paginator = self.paginator
        paginated_posts = paginator.paginate_queryset(posts, request)
        return paginator.get_paginated_response(self.get_serializer(paginated_posts, many=True).data)

    def retrieve(self, request, pk):
        """
        GET /posts/{post_id}/
        """
        post = get_object_or_404(Post, id=pk)
        return Response(self.get_serializer(post).data)

    def partial_update(self, request, pk):
        """
        PATCH /posts/{post_id}/
        """
        post = get_object_or_404(Post, id=pk)
        if post.author != request.user:
            raise PermissionDenied
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(post, serializer.validated_data)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """
        DELETE /posts/{post_id}/
        """
        post = get_object_or_404(Post, id=pk)
        if post.author != request.user:
            raise PermissionDenied
        post.delete()
        return Response('{post deleted}')
