from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import util
from django import forms
from datetime import datetime
from markdown2 import Markdown
import re

md = Markdown()

class NewEntry(forms.Form):
    new_entry_title = forms.CharField(label="Title:", max_length=150, widget=forms.TextInput(attrs={"class": "newEntryTitle"}))
    new_entry_content = forms.CharField(label="Add a new Encyclopedia entry", widget=forms.Textarea(attrs={"class": "newEntryContent"}))

class EditEntry(forms.Form):
    edit_entry_title = forms.CharField(label="Title:", max_length=150, widget=forms.TextInput(attrs={"class": "newEntryTitle"}))
    edit_entry_content = forms.CharField(label="Add a new Encyclopedia entry", widget=forms.Textarea(attrs={"class": "newEntryContent"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def article(request, entry):
    return render(request, "encyclopedia/article.html", {
        "entry": md.convert(util.get_entry(entry)),
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

            if util.save_entry(title, content) == FileExistsError:
                return render(request, "encyclopedia/add_new.html", {
                    "entry": title,
                    "form": new_entry,
                    "error": FileExistsError,
                })

            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('article', args=[title]))

        else:
            return render(request, "encyclopedia/add_new.html", {
                "form": new_entry
            })

    return render(request, "encyclopedia/add_new.html", {
        "form": NewEntry()
    })

def edit_entry(request, entry):
    if request.method == "POST":
        edit_entry = EditEntry(request.POST)

        if edit_entry.is_valid():
            cleaned_title = edit_entry.cleaned_data["edit_entry_title"]
            cleaned_content = edit_entry.cleaned_data["edit_entry_content"]

            util.edit_entry(cleaned_title, cleaned_content)

            return HttpResponseRedirect(reverse('article', args=[cleaned_title]))

        else:
            return render(request, "encyclopedia/edit_entry.html", {
                "form": edit_entry,
                "title": entry,
            })

    return render(request, "encyclopedia/edit_entry.html", {
        "title": entry,
        "form": EditEntry({"edit_entry_title": entry, "edit_entry_content": re.sub("^.*\n*", "", util.get_entry(entry))}) # removes title from markup do avoid duplication
    })