from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib import messages
from .forms import NewEntryForm, EditEntryForm
import markdown2
import re
import random
from . import util


def index(request):
    """
    1. Update index.html such that user can click on any entry name to be taken directly to that entry page.
    """
    entries = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):

    """
    1. Get the content of the encyclopedia entry by calling the appropriate util function.
    2. If an entry does not exist, show error page displaying entry was not found.
    3. If the entry exists, present page with content of the entry. Title of the page should include name of the entry.
    """

    """
    Markdown to HTML Conversion: On each entry’s page, any Markdown content in the entry file should be converted to HTML before being displayed to the user. You may use the python-markdown2 package to perform this conversion, installable via pip3 install markdown2.
    """
    content = util.get_entry(title)
    if content == None:
        content = title
        messages.error(request, f"Sorry, {title} does not exist.")
        return render(request, "encyclopedia/error.html")
    else:
        content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
        "content": content, "title": title
        })

def search(request):

    """
    1. Allow user to type a query into the search box.
    2. Redirect user to search page if query matches.
    3. If the query does not match entry, direct user to results page that displays a list of all entries that have the query as a substring.
    4. Clicking on any of the entry names on the search results page should take the user to that entry’s page.
    """
    content = request.GET.get("q")
    title = content
    entry = util.get_entry(content)

    if content in util.list_entries():
        messages.info(request, f"Found {title}.")
        return render(request, "encyclopedia/entry.html", {
            "content": entry, "title": title
        })

    else:
        entries = util.list_entries()
        substring = []
        for entry in entries:
            if re.findall(content, entry, re.IGNORECASE):
                substring.append(entry)
        if substring:
            for item in substring:
                print(util.get_entry(item))
            messages.success(request, f"{len(substring)} entries found.")
            return render(request, "encyclopedia/search_list.html", { "entries": substring })
        else:
            messages.error(request, f"{title} does not exist.")
            return render(request, "encyclopedia/error.html", { "content": content })

def new(request):
    """
    1. New Page: Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
    2. Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
    3. Users should be able to click a button to save their new page.
    4. When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
    5. Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
    """
    entries = []
    form = NewEntryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        body = form.cleaned_data["body"]

        if title in util.list_entries():
            messages.warning(request, f"{title} is already taken.")
            return render(request, "encyclopedia/error.html", { "title": title })
        util.save_entry(title, body)

        return redirect(f"/wiki/{title}/")
        messages.success(request, f'{title} saved!')
    else:
        return render(request, "encyclopedia/new.html", { "form": form })


def edit(request, title):
    """
    1. Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
    2. The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
    3. The user should be able to click a button to save the changes made to the entry.
    4. Once the entry is saved, the user should be redirected back to that entry’s page.
    """

    form = EditEntryForm(request.POST or None)
    entry = util.get_entry(title)

    # GET the form if entry exists
    if request.method == "GET" and entry:
        form.fields["title"].initial = title
        form.fields["body"].initial = entry
        return render(request, "encyclopedia/edit.html", { "form": form, "title": title })

    # POST if valid entry and title does not exist
    elif request.method == "POST" and entry and form.is_valid():
        title = form.cleaned_data["title"]
        body = form.cleaned_data["body"]
        util.save_entry(title, body)

        return redirect(f"/wiki/{title}/")
        messages.success(request, f'{title} saved!')
    else:
        messages.error(request, f'{title} does not exist.')
        return render(request, "encyclopedia/error.html", { "error": title })


def random_page(request):
    """
    1. Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
    """
    substring = []
    for item in util.list_entries():
        substring.append(item)

    title = random.choice(substring)
    return redirect(f"/wiki/{title}/")
