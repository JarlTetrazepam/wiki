from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, entry):
    return render(request, "encyclopedia/article.html", {
        "entry": util.get_entry(entry),
        "title": entry
    })