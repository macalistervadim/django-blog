from django.contrib.sitemaps import Sitemap

import blog.models


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return blog.models.Post.published.all()

    def lastmod(self, obj):
        return obj.updated