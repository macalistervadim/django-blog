from typing import TypeAlias

from django.http import HttpRequest, HttpResponse
import django.shortcuts
from django.views.generic import ListView

import blog.models
import blog.forms


class PostListView(ListView):
    queryset = blog.models.Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    post = django.shortcuts.get_object_or_404(
        blog.models.Post,
        id=post_id,
        status=blog.models.Post.Status.PUBLISHED,
    )
    if request.method == "POST":
        form = blog.forms.EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

    else:
        form = blog.forms.EmailPostForm()
    
    return django.shortcuts.render(request=request, template_name="blog/post/share.html", context={"post": post, "form": form})


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
