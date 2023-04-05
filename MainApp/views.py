from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', "form": form}
        return render(request, 'pages/add_snippet.html', context)

    form = SnippetForm(request.POST, request.FILES)
    if form.is_valid():
        snippet = form.save(commit=False)
        if request.user.is_authenticated:
            snippet.user = request.user
        snippet.save()
        return redirect('snippets-list')
    context = {'pagename': 'Добавление нового сниппета', "form": form}
    return render(request, 'pages/add_snippet.html', context)


@login_required
def edit_snippet_page(request, id):
    if request.method == "GET":
        snippet = Snippet.objects.get(id=id)
        form = SnippetForm(instance=snippet)
        if snippet.user == request.user:
            context = {'pagename': 'Страница сниппета',
                       "snippet": snippet,
                       "edit": True,
                       "form": form}
            return render(request, 'pages/snippet_info.html', context)


@login_required
def delete_snippet_page(request, id):
    snippet = Snippet.objects.get(id=id)
    if snippet.user != request.user:
        raise HttpResponseForbidden
    snippet.delete()
    return render(request, 'pages/view_snippets.html')


def snippets_page(request):
    # snippets = Snippet.objects.all()
    # sort_field = request.GET.get("sort")
    # if sort_field is not None:
    #     snippets = snippets.order_by(sort_field)
    # context = {'pagename': 'Просмотр сниппетов',
    #            "snippets": snippets}
    # return render(request, 'pages/view_snippets.html', context)

    # STATE: 0 NONE 1 UP 2 DOWN
    fields = {"id": 0, "name": 0, "creation_date": 0}
    snippets = Snippet.objects.all()
    sort_field = request.GET.get("sort")
    if sort_field is not None:
        if "-" in sort_field:
            fields[sort_field.replace("-", "")] = 2
        else:
            fields[sort_field] = 1
        snippets = snippets.order_by(sort_field)
    sort_user = request.GET.get("user")
    if sort_user:
        snippets = snippets.filter(user__username=sort_user)
    users = User.objects.all().annotate(count_snippets=Count('snippet'))
    users = [user for user in users if user.count_snippets > 0]
    context = {
        'pagename': 'Просмотр сниппетов',
        "snippets": snippets,
        "fields": fields,
        "users": users,
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, id):
    snippet = Snippet.objects.get(id=id)
    form_comment = CommentForm()
    context = {'pagename': 'Страница сниппета',
               "snippet": snippet,
               "form_comment": form_comment}
    return render(request, 'pages/snippet_info.html', context)


def register(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {"form": form}
        return render(request, 'pages/register_page.html', context)

    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('home')

    context = {"form": form}
    return render(request, 'pages/register_page.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST["snippet_id"]
        if comment_form.is_valid():
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()

        return redirect(f'/snippet/{snippet_id}')
    raise Http404
