from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(("title"), max_length=255)
    authors = models.CharField(("authors"), max_length=255)
    average_rating = models.FloatField(("average rating"))
    num_pages = models.IntegerField(("number of pages"))
    ratings_count = models.IntegerField(("rating count"))
    text_review_count = models.IntegerField(("text review count"))
    publication_date = models.DateField(("publication date"), auto_now=True)
    publisher = models.CharField(("publisher"), max_length=150)

