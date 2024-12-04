from django.db import models
from django.contrib.auth.models import User


class Advertisement(models.Model):
    """Модель объявления, содержащая информацию о заголовке, содержимом и авторе."""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращает строковое представление объявления (заголовок)."""
        return self.title


class Comment(models.Model):
    """Модель комментария к объявлению."""

    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращает строковое представление комментария (автор и его содержание)."""
        return f'Comment by {self.author} on {self.advertisement}'
