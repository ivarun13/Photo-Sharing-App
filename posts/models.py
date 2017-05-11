from django.db import models
from django.core.urlresolvers import reverse
from accounts.models import User


def upload_location(instance,filename):
    return "%s/%s" %(instance.id,filename)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='post',default=1)
    title = models.CharField(max_length=120)
    image = models.FileField(upload_to=upload_location,null=True,blank=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"id":self.id})

    class Meta:
        ordering = ["-timestamp","-updated"]


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='liked_post')
    user = models.ForeignKey(User, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{} : {}'.format(self.user, self.post)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments')
    user = models.ForeignKey(User, related_name='commenter')
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=120)

    def __unicode__(self):
        return self.content

    def __str__(self):
        return self.content

