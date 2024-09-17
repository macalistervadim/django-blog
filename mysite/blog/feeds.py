from typing import Any

from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
import markdown

import blog.models


class LatestPostsFeed(Feed):
    title = "My blog"
    link = reverse_lazy("blog:post_list")
    description = "New posts of my blog."

    def items(self) -> QuerySet[blog.models.Post]:
        return blog.models.Post.published.all()[:5]

    def item_title(self, item: {title}) -> Any:
        return item.title

    def item_description(self, item: Any) -> str:
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item: Any) -> str:
        return item.publish
