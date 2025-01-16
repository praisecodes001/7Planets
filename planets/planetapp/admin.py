
from django.contrib import admin
from .models import Post
from .forms import PostForm

admin.site.register(Post)
