from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import util
from django import forms
from datetime import datetime

class NewEntry(forms.Form):
    new_entry_title = forms.CharField(label="Title:", max_length=150)
    new_entry_content = forms.CharField(label="Add a new Encyclopedia entry", widget=forms.Textarea)

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

def add_new(request):

    if request.method == "POST":
        new_entry = NewEntry(request.POST)
        if new_entry.is_valid():
            title = new_entry.cleaned_data["new_entry_title"]
            content = new_entry.cleaned_data["new_entry_content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('article', args=[title]))
        else:
            return render(request, "encyclopedia/add_new.html", {
                "form": new_entry
            })

    return render(request, "encyclopedia/add_new.html", {
        "form": NewEntry()
    })