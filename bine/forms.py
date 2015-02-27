from django import forms

from bine.models import BookNote


class BookNoteForm(forms.ModelForm):
    class Meta:
        model = BookNote
        fields = ['user', 'book', 'read_date_from', 'read_date_to',
                  'content', 'preference', 'attach', 'share_to']