from movie_app.models import *
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id username first_name last_name email'.split()


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split(' ')

    def get_movies_count(self, director):
        return director.movie_count()


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25, required=True)

    def validate_name(self, name):
        name_exists = Director.objects.filter(name=name).exists()
        if not name_exists:
            return name
        raise ValidationError('Режииссер с таким именем нет')


class MovieSerializer(serializers.ModelSerializer):
    director = serializers.PrimaryKeyRelatedField(pk_field='id', queryset=Director.objects.all())
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director rating'.split()

    def get_rating(self, movie):
        return movie.rating()


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    duration = serializers.IntegerField(required=True)
    director_id = serializers.IntegerField(required=True, min_value=1)

    def validate_title(self, title):
        title_exists = Movie.objects.filter(title=title).exists()
        if not title_exists:
            return title
        raise ValidationError('фильм создан')

    def validate_director_id(self, director_id):
        director_exists = Director.objects.filter(id=director_id).exists()
        if not director_exists:
            raise ValidationError('Director with that id does not exists')
        return director_id


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), pk_field='id')
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), pk_field='id')

    class Meta:
        model = Review
        fields = '__all__'


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=10, required=True)
    stars = serializers.IntegerField(min_value=1, max_value=5, required=True)
    movie_id = serializers.IntegerField(min_value=1, required=True)

    def validate_movie_id(self, movie_id):
        movie_exists = Movie.objects.filter(id=movie_id).exists()
        if movie_exists:
            return movie_id
        raise ValidationError('Фильма с таким id не существует')


class MoviesReviewsSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = 'id title description duration director reviews rating'.split()

    def get_rating(self, movie):
        return movie.rating()