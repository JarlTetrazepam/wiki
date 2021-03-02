import re
import markdown2
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown

md = Markdown()

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return FileExistsError
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns an error.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return md.convert(f.read().decode("utf-8"))
    except FileNotFoundError:
        return f"Error: File '{title}' not found"

def search(query):
    results = []
    for title in list_entries():
        if query.lower() == title.lower():
            results.append(title)
            return title
        if query.lower() in title.lower():
            results.append(title)
    return results

def random_entry():
    entries = list_entries()
    random_index = random.randint(0, len(entries) - 1)
    return entries[random_index]