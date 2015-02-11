from bine.models import BookNote, BookNoteReply, User, Book, BookNoteLikeit
from django.http.response import JsonResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed
from django.views.generic.base import View
from bine.serializers import BookNoteWriteSerializer
import json

def get_current_user(request):
    if request.user:
        user = request.user
    else: 
        user = User.objects.get(pk=2)
    return user

def get_book(request):
    book = Book.objects.get(pk=request.POST['book'])
    return book

class BookList(View):
    def get(self, request):
        title = request.GET['title']
        if title is None:
            return HttpResponseNotAllowed(request);
          
        books = Book.objects.filter(title__icontains=title)
        
        json_text = list(map(lambda x: x.to_json(), books.all()))
        return JsonResponse(json_text, safe=False)
            
class BookNoteList(View):
    def get(self, request):
        notes = BookNote.objects.all()
        json_text = list(map(lambda x: x.to_json(), notes.all()))
        
        return JsonResponse(json_text, safe=False)
    
    def post(self, request):    
        json_data =  json.loads(request.body.decode('utf-8'))
                            
        serializer = BookNoteWriteSerializer(data=json_data)
        if not serializer.is_valid():
            return HttpResponseBadRequest()
        
        note = serializer.save()
        """
        note.user = get_current_user(request)
        note.book = get_book(json_data.get('book_id'))
        note.read_date_from = json_data.get('read_date_from')
        note.read_date_to = json_data.get('read_date_to')
        note.preference = json_data.get('preference')
        note.share_to = json_data.get('share_to')
        note.content = json_data.get('content')
        note.save()
        """        
        if note:
            return JsonResponse(note.to_json(), safe=False)
    
class BookNoteDetail(View):
    def get(self, request, pk):
        note = BookNote.objects.get(pk=pk)
        json_text = note.to_json();
        return JsonResponse(json_text, safe=False)
    
    def post(self, request, pk):
        note = BookNote.objects.get(pk=pk)
        if note is None:
            return HttpResponseBadRequest()
        
        json_data = json.loads(request.body.decode('utf-8'))
        serializer = BookNoteWriteSerializer(instance = note, data=json_data)
        if not serializer.is_valid():
            return HttpResponseBadRequest(serializer.errors())
        
        note = serializer.save();
            
        if note:
            return JsonResponse(note.to_json(), safe=False)
        
    def delete(self, request, pk):
        note = BookNote.objects.get(pk=pk)
        if note is None:
            return HttpResponseBadRequest()
        
        note.delete();
        
        return JsonResponse({'status':'success'})

class BookNoteLikeItUpdate(View):
    def post(self, request, note_id):
        user = get_current_user(request)
        note = BookNote.objects.get(pk=note_id);
        
        if user and note:
            likeit = BookNoteLikeit()
            likeit.user = user;
            likeit.note = note;
            likeit.save();
            return JsonResponse({'likeit':note.likeit.count()});
        else:
            return HttpResponseBadRequest();
        
class BookNoteReplyList(View):
    def get(self, request, note_id):
        if note_id is None:
            return HttpResponseBadRequest(request);
        
        replies = BookNoteReply.objects.filter(note__pk = note_id)
        json_text = list(map(lambda x: x.to_json(), replies.all()))
        
        return JsonResponse(json_text, safe=False)
    
    def post(self, request, note_id):
        if note_id is None:
            return HttpResponseBadRequest(request);
        
        json_data =  json.loads(request.body.decode('utf-8'))
        reply = BookNoteReply()
        reply.user = get_current_user()
        reply.note = BookNote.objects.get(pk=note_id)
        reply.content = json_data.get('content')
        reply.save()
        
        return JsonResponse(reply.to_json(), safe = False)
    
class BookNoteReplyDetail(View):
    def post(self, request, note_id, reply_id):
        if reply_id is None:
            return HttpResponseBadRequest(request);
        
        reply = BookNoteReply.objects.get(pk=reply_id)
        if reply is None:
            return HttpResponseBadRequest(request);
        
        json_data = json.loads(request.body.decode('utf-8'))
        reply.content = json_data.get('content')
        reply.save()
        return JsonResponse(reply.to_json(), safe = False)
    
        
    def delete(self, request, note_id, reply_id):
        if reply_id is None:
            return HttpResponseBadRequest(request);
        
        reply = BookNoteReply.objects.get(pk=reply_id)
        if reply:
            reply.delete()
        
        return JsonResponse({'status':'success'}, safe = False)