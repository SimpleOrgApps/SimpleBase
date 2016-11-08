from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout

from .forms import LoginForm
from .models import SiteSetting, SidebarLink, TitlebarLink

def login_view(request):
    background = None
    try:
        site_settings = SiteSetting.objects.get(pk=1)
        organization = site_settings.organization
        description = site_settings.description
        background = site_settings.background
    except SiteSetting.DoesNotExist:
        organization = "My Organization"
        description = "An organization description will need to be set up in \
        the admin panel"
    try:
        sidebar_links = SidebarLink.objects.all()
    except SidebarLink.DoesNotExist:
        sidebar_links = None
    try:
        titlebar_links = TitlebarLink.objects.all()
    except TitlebarLink.DoesNotExist:
        titlebar_links = None

    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
    return render(request, 'SimpleBase/login.html', {
        'form': form,
        'organization': organization,
        'description': description,
        'background': background,
        'sidebar_links': sidebar_links,
        'titlebar_links': titlebar_links,
    })
