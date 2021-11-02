from djongo import models


class CComment(models.Model):
    _id = models.ObjectIdField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ccomment"


class AComment(models.Model):
    _id = models.ObjectIdField()
    ccomments = models.ArrayField(
        model_container=CComment
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "acomment"


class Category(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"


class Article(models.Model):
    _id = models.ObjectIdField()
    acomments = models.ArrayField(
        model_container=AComment
    )
    category = models.EmbeddedField(
        model_container=Category
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "article"
