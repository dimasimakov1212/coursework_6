from django import forms

from blog.models import Blog
from mailing.models import Mailing, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_current_version":
                field.widget.attrs['class'] = 'form-control'


class BlogForm(StyleFormMixin, forms.ModelForm):
    """
     Создает форму для создания товара
    """
    class Meta:
        """
        Определяет параметры формы
        """
        model = Blog

        fields = ('blog_title', 'blog_text', 'blog_preview')
