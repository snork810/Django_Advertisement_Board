from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Модель профиля пользователя для хранения информации о количестве созданных объявлений."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    advertisement_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Advertisement(models.Model):
    """Модель объявления, содержащая информацию о заголовке, содержимом и авторе."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='advertisements/', null=True, blank=True, storage=FileSystemStorage())
    likes = models.ManyToManyField(User, related_name='liked_advertisements', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_advertisements', blank=True)

    def __str__(self):
        """Возвращает строковое представление объявления (заголовок)."""
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def save(self, *args, **kwargs):
        """Обновляет счётчик объявлений при создании нового объявления."""
        super().save(*args, **kwargs)
        Profile.objects.filter(user=self.author).update(advertisement_count=models.F('advertisement_count') + 1)

    def delete(self, *args, **kwargs):
        """Обновляет счётчик объявлений при удалении объявления."""
        Profile.objects.filter(user=self.author).update(advertisement_count=models.F('advertisement_count') - 1)
        super().delete(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создает профиль пользователя после его создания."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль пользователя при его обновлении."""
    instance.profile.save()


class Comment(models.Model):
    """Модель комментария к объявлению."""
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращает строковое представление комментария (автор и его содержание)."""
        return f'Comment by {self.author} on {self.advertisement}'
