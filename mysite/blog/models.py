import django.contrib.auth.models as django_models_auth
from django.db import models
from django.urls import reverse
import django.utils.timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date="publish",
    )
    author = models.ForeignKey(
        django_models_auth.User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    body = models.TextField()
    publish = models.DateTimeField(default=django.utils.timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"title={self.title!r}, "
            f"slug={self.slug!r}, "
            f"author={self.author!r}, "
            f"body={self.body!r}, "
            f"publish={self.publish!r}, "
            f"created={self.created!r}, "
            f"updated={self.created!r}, "
            f"status={self.status!r}, "
            f"objects={self.objects!r}, "
            f"tags={self.tags!r}, "
            f"published={self.published!r})"
        )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"post={self.post!r}, "
            f"name={self.name!r}, "
            f"email={self.email!r}, "
            f"body={self.body!r}, "
            f"created={self.created!r}, "
            f"updated={self.updated!r}, "
            f"active={self.active!r})"
        )
