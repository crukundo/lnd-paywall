from django.shortcuts import get_object_or_404, render

from apps.blog.models import Entry


def entries(request):
    entries = (
        Entry.objects.select_related("author__profile")
        .filter(status=Entry.PUBLISHED)
        .order_by(
            "-start_publication",
        )
    )
    return render(request, "blog/entries.html", {"entries": entries})


def entry(request, slug):
    blog_entry = get_object_or_404(
        Entry.objects.select_related("author__profile"), slug=slug, status=Entry.PUBLISHED
    )
    return render(request, "blog/entry.html", {"entry": blog_entry})