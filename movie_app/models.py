from django.db import models
from django.contrib.auth.models import User



class Director(models.Model):
    name = models.CharField(max_length=150)

    def movie_count(self):
        return self.movie_set.all().count()



    def __str__(self):
        return self.name




class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    duration = models.FloatField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def rating(self):
        lst = [review.stars for review in self.reviews.all()]
        return (sum(lst) / len(lst)) if len(lst) != 0 else "No reviews yet"

    def __str__(self):
        return self.title





RATING = (
    (1,'⭐'),
    (2,'⭐ ⭐'),
    (3,'⭐ ⭐ ⭐'),
    (4,'⭐ ⭐ ⭐ ⭐️'),
    (5,'⭐ ⭐ ⭐ ⭐ ⭐️')
)

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    stars = models.IntegerField(default=5, choices=RATING)


    def __str__(self):
        if len(self.text) <= 50:
            return (self.author.username if self.author is not None else 'Anonymous') + ', ' \
                   + self.text + '; ' + self.movie.title
        return (self.author.username if self.author is not None else 'Anonymous') + ', ' \
               + self.text[0:50] + '...;  ' + self.movie.title