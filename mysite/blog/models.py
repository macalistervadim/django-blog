import django.db.models
import django.utils.timezone
import django.contrib.auth.models as django_models_auth


class PublishedManager(django.db.models.Manager):
    def get_queryset(self) -> django.db.models.QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(django.db.models.Model):

    class Status(django.db.models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = django.db.models.CharField(max_length=250)
    slug = django.db.models.SlugField(max_length=250)
    author = django.db.models.ForeignKey(
        django_models_auth.User,
        on_delete=django.db.models.CASCADE,
        related_name="blog_posts",
    )
    body = django.db.models.TextField()
    publish = django.db.models.DateTimeField(default=django.utils.timezone.now)
    created = django.db.models.DateTimeField(auto_now_add=True)
    updated = django.db.models.DateTimeField(auto_now=True)
    status = django.db.models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    objects = django.db.models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            django.db.models.Index(fields=["-publish"]),
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
            f"published={self.published!r})"
        )

    def __str__(self) -> str:
        return self.title
