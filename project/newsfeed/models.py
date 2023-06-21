from django.db import models
from accounts.models import User
from django.utils import timezone
# Create your models here.


class Posts(models.Model):
    user = models.ForeignKey(
        User,
        related_name="post",
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, null=True, blank=True, related_name='bzz_likes')

    class Meta:
        db_table = 'posts'

    #Keep track of likes
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}) "
            f"{self.body}"
        )


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'comments'


