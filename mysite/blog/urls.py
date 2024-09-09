from django.urls import path

import blog.views

app_name = "blog"

urlpatterns = [
    path("", blog.views.PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>",
        blog.views.post_detail,
        name="post_detail",
    ),
    path("<int:post_id>/share/", blog.views.post_share, name="post_share"),
]
