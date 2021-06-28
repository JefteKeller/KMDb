from django.db.models.query import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from rest_framework import status

from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Movie, Review, Comment
from .serializers import MovieSerializer, ReviewSerializer, CommentSerializer

from .permissions import (
    OnlyAdminCanCreateDeleteMovie,
    OnlyCriticCanCreateUpdateReview,
    OnlyUserCanCreateUpdateComment,
)


class ListCreateMovieView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        OnlyAdminCanCreateDeleteMovie,
    ]

    def get_queryset(self):
        queryset = self.queryset

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        if self.request.data.get('title'):
            queryset = queryset.filter(
                title__icontains=self.request.data.get('title')
            ).all()

        return queryset


class RetrieveDeleteMovieView(RetrieveDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        OnlyAdminCanCreateDeleteMovie,
    ]


class CreateUpdateReviewView(GenericAPIView, CreateModelMixin, UpdateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyCriticCanCreateUpdateReview]

    def perform_create(self, serializer):

        critic = self.request.user
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))

        has_review = movie.criticism_set.filter(critic__id=critic.id).first()

        if has_review:
            duplication_error = ValidationError(
                {'detail': 'You already made this review.'}
            )
            duplication_error.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

            raise duplication_error

        serializer.save(critic=critic, movie=movie)

    def get_object(self):

        critic = self.request.user
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))

        requested_review = movie.criticism_set.filter(critic__id=critic.id).first()

        if not requested_review:
            raise NotFound()

        return requested_review

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CreateUpdateCommentView(GenericAPIView, CreateModelMixin, UpdateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyUserCanCreateUpdateComment]

    def perform_create(self, serializer):

        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))

        return serializer.save(user=self.request.user, movie=movie)

    def get_object(self):
        user = self.request.user
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))

        requested_comment = movie.comment_set.filter(
            pk=self.request.data.get('comment_id')
        ).first()

        if not requested_comment:
            raise NotFound()

        if requested_comment.user.id != user.id:
            raise PermissionDenied()

        return requested_comment

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
