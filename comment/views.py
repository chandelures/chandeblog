from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from blog.models import Article

from comment.models import Comment
from comment.serializers import CommentSerializer


class CommentList(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        article = get_object_or_404(
            Article.objects.all(), slug=self.kwargs['article_slug'])
        return article.comment.filter(tag=0)


class CommentCreate(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id

        article = get_object_or_404(
            Article.objects.all(), slug=self.kwargs['article_slug'])
        data['article'] = article.id

        if(data.get('parent')):
            parent = get_object_or_404(
                Comment.objects.all(), uid=data.get('parent')
            )
            data['parent'] = parent.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
