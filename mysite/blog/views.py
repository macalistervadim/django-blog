from typing import TypeAlias

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
import django.shortcuts

import blog.models


def post_list(request: HttpRequest) -> HttpResponse:
    post_list = blog.models.Post.published.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return django.shortcuts.render(
        request=request,
        template_name="blog/post/list.html",
        context={"posts": posts},
    )


Year: TypeAlias = int
Day: TypeAlias = int
Month: TypeAlias = int


def post_detail(
    request: HttpRequest,
    year: Year,
    month: int,
    day: int,
    post: str,  # slug
) -> HttpResponse:
    post_ = django.shortcuts.get_object_or_404(
        blog.models.Post,
        status=blog.models.Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return django.shortcuts.render(
        request=request,
        template_name="blog/post/detail.html",
        context={"post": post_},
    )
