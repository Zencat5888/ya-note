from pytils.translit import slugify
from django import forms
from .models import Note

WARNING = ' - такой slug уже существует, придумайте уникальное значение!'


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text', 'slug')

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = slugify(self.cleaned_data.get('title'))[:100]

        # Проверка уникальности с учётом редактирования существующей заметки
        if Note.objects.filter(slug=slug).exclude(id=getattr(self.instance, 'id', None)).exists():
            raise forms.ValidationError(slug + WARNING)
        return slug
    
# from pytils.translit import slugify

# from django import forms
# from django.core.exceptions import ValidationError

# from .models import Note

# WARNING = ' - такой slug уже существует, придумайте уникальное значение!'


# class NoteForm(forms.ModelForm):
#     """Форма для создания или обновления заметки."""

#     class Meta:
#         model = Note
#         fields = ('title', 'text', 'slug')

#     def clean_slug(self):
#         """Обрабатывает случай, если slug не уникален."""
#         cleaned_data = super().clean()
#         slug = cleaned_data.get('slug')
#         if not slug:
#             title = cleaned_data.get('title')
#             slug = slugify(title)[:100]
#         if Note.objects.filter(
#                 slug=slug
#         ).exclude(id=self.instance.pk).exists():
#             raise ValidationError(slug + WARNING)
#         return slug
