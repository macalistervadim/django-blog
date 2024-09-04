import django.http
import django.shortcuts

import blog.models


def post_list(request: django.http.HttpRequest) -> django.http.HttpResponse:
    posts = blog.models.Post.published.all()

    return django.shortcuts.render(
        request=request,
        template_name="blog/post/list.html",
        context={"posts": posts},
    )


def post_detail(
    request: django.http.HttpRequest, id: int
) -> django.http.HttpResponse:
    post = django.shortcuts.get_object_or_404(
        blog.models.Post, id=id, status=blog.models.Post.Status.PUBLISHED
    )

    return django.shortcuts.render(
        request=request,
        template_name="blog/post/detail.html",
        context={"post": post},
    )
