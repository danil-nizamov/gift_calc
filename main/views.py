from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import UserStory


class UserStoryListView(ListView):
    model = UserStory
    template_name = 'main/user_stories.html'
    context_object_name = 'user_stories'
    ordering = ['-created_at']


class CalcView(TemplateView):
    template_name = "main/index.html"

