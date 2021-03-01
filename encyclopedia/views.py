from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
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

def search(request):
    query = request.GET.get("q")
    if str(util.search(query)).lower() == query.lower():
        return HttpResponseRedirect(reverse('article', args=[query]))
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": util.search(query)
        })

def random(request):
    entry = util.random_entry()
    return HttpResponseRedirect(reverse('article', args=[entry]))