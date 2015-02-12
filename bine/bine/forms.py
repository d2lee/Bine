from bine.models import BookNote
from django import forms

class BookNoteForm(forms.ModelForm):
    class Meta:
        model = BookNote