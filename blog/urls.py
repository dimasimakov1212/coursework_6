from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('blog/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
    path('edit_blog/<int:pk>/', BlogUpdateView.as_view(), name='edit_blog'),
    path('delete_blog/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),
]
