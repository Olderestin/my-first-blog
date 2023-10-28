from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def delete_related_images(self):
        for post_image in self.postimage_set.all():
            post_image.delete()

    def delete(self, *args, **kwargs):
        self.delete_related_images()
        super().delete(*args, **kwargs)

def generate_image_filename(instance, filename):
    username = instance.post.author.username
    date_string = timezone.now().strftime('%Y.%m.%d.%H.%M.%S')
    unique_id = str(uuid.uuid4())
    new_filename = f'post_images/{date_string}_{username}_{unique_id}.jpg'
    return new_filename


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_image_filename)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.author)
