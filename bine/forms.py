from django import forms

from bine.models import BookNote


class BookNoteForm(forms.ModelForm):
    class Meta:
        model = BookNote