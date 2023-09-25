from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
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
        queryset = queryset.filter(blog_is_active=True)

        return queryset


class BlogCreateView(CreateView):
    """
    Выводит форму создания статьи
    """
    model = Blog
    form_class = BlogForm

    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        """
        Реализует заполнение формы блога
        """
        self.object = form.save()
        self.object.blog_owner = self.request.user
        self.object.save()

        if form.is_valid():
            new_article = form.save()
            new_article.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Создание статьи'
        return context


class BlogDetailView(DetailView):
    """
    Выводит информаццию о статье
    """
    model = Blog

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Просмотр статьи'
        return context

    def get_object(self, queryset=None):
        """
        Считает количество просмотров статьи
        """
        self.object = super(BlogDetailView, self).get_object(queryset)
        self.object.blog_views_count += 1
        self.object.save()

        return self.object


class BlogUpdateView(UpdateView):
    """
    Выводит форму редактирования статьи
    """
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        """
        Реализует создание Slug — человекопонятный URL
        """
        if form.is_valid():
            new_article = form.save()
            new_article.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Изменение статьи'
        return context


class BlogDeleteView(DeleteView):
    """
    Выводит форму удаления статьи
    """
    model = Blog

    success_url = reverse_lazy('blog:blog_list')

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Удаление статьи'
        return context
