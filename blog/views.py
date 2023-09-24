from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Blog


class BlogListView(ListView):
    """
    Выводит список статей пользователя
    """
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Полезные статьи'
        return context

    def get_queryset(self, *args, **kwargs):
        """
        Выводит в список только опубликованные статьи
        """
        queryset = super().get_queryset(*args, **kwargs)

        try:
            user = self.request.user

            if user.is_superuser or user.groups.filter(name='manager'):
                return queryset

            else:
                queryset = queryset.filter(blog_owner=user)

        except TypeError:
            pass

        return queryset
