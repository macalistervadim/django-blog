from django.urls import path

import blog.feeds
import blog.views


app_name = "blog"

urlpatterns = [
    path("", blog.views.PostListView.as_view(), name="post_list"),
    path(
        "tag/<slug:tag_slug>/",
        blog.views.PostListView.as_view(),
        name="post_list_by_tag",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>",
        blog.views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "<int:post_id>/share/",
        blog.views.PostShareView.as_view(),
        name="post_share",
    ),
    path(
        "<int:post_id>/comment/",
        blog.views.PostCommentView.as_view(),
        name="post_comment",
    ),
    path("feed/", blog.feeds.LatestPostsFeed(), name="post_feed"),
    path("search/", blog.views.PostSearchView.as_view(), name="post_search"),
]
