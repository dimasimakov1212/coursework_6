from django.urls import path


from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
]
