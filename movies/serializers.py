from rest_framework import serializers

from .models import Movie, Genre, Review, Comment
from accounts.serializers import CriticSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'critic', 'stars', 'review', 'spoilers']


class CommentSerializer(serializers.ModelSerializer):
    user = CriticSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    criticism_set = ReviewSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'duration',
            'genres',
            'launch',
            'classification',
            'synopsis',
            'criticism_set',
            'comment_set',
        ]
        depth = 1

    def create(self, validated_data):
        genre_data = validated_data.pop('genres')
        genre_objects = [
            Genre.objects.get_or_create(name=genre['name'])[0] for genre in genre_data
        ]
        new_movie = Movie.objects.create(**validated_data)
        new_movie.genres.set(genre_objects)
        return new_movie
