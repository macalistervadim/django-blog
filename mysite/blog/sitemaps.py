from typing import Any

from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet

import blog.models


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self) -> QuerySet[blog.models.Post]:
        return blog.models.Post.published.all()

    def lastmod(self, obj: Any) -> Any:
        return obj.updated
