from django.contrib import admin

from bine.models import User, Book, BookCategory, BookNote, BookNoteReply


admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookCategory)
admin.site.register(BookNote)
admin.site.register(BookNoteReply)