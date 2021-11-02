from djongo import models


class Comment(models.Model):
    _id = models.ObjectIdField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
    _id = models.ObjectIdField()
    comments = models.ArrayField(
        model_container=Comment
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
