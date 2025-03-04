from django.db import models
from django.contrib.auth.models import User

# TODO-7: let users to add another users to friend list
"""
1. Three categories of preferences:
- not authorized
- authorized but users are not friends
- authorized and users are friends
2. Befriend button
"""


# TODO-11: Create manager for most used filter-query
class MovieManager(models.Manager):
	def num_comments(self, num_comments):
		return (self.raw
		        (""
		         "SELECT basic_site_movies.title, COUNT(*) "
		         "FROM basic_site_movies INNER JOIN basic_site_comments "
		         "ON basic_site_movies.id = basic_site_comments.movie_id "
		         "GROUP BY basic_site_movies.title "
		         "HAVING COUNT(*) > %s;",
		         [num_comments]))

	def num_movies(self):
		return self.raw('SELECT COUNT(*) FROM basic_site_movies')


class Genres(models.Model):
	name = models.CharField(max_length=20, unique=True, db_index=True)

	def __str__(self):
		return self.name


class Movies(models.Model):
	title = models.CharField(max_length=100, unique=True,
	                         db_index=True)  # unique=True is just for more convenient debug
	overview = models.TextField(max_length=500, blank=True)  # NEW
	release_date = models.DateField(null=True, blank=True)
	country = models.CharField(max_length=100)
	genres = models.ManyToManyField(Genres, related_name='movies')
	poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True,
	                           default='movie_posters/default-poster.jpg')
	adult = models.BooleanField(default=False)  # NEW
	average_rating = models.FloatField(default=0.0)

	objects = MovieManager()

	def __str__(self):
		return self.title

	class Meta:
		indexes = [
			models.Index(fields=['title', 'release_date', 'country', 'poster', 'average_rating']),
		]


class WatchLater(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlater')
	movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='watchlater')
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'movie')


# TODO-12: new model
"""
class MoviesPlaylist
	user = FK
	movie = FK
	name = unique
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)

	class Meta:
		unique_together = ('user', 'movie')
"""
# TODO-13: Add opportunity to add a movie in a playlist + create a new one on a movie-page
