from django.urls import path

import blog.views

app_name = "blog"

urlpatterns = [
    path("", blog.views.post_list, name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>",
        blog.views.post_detail,
        name="post_detail",
    ),
]
