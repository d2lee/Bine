from bine.models import BookNote, BookNoteReply, User, Book, BookNoteLikeit
from bine.serializers import BookNoteWriteSerializer
from rest_framework.views import APIView
from bine.forms import BookNoteForm
from django.http.response import JsonResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed

def get_current_user(request):
    if request.user:
        user = request.user
    else: 
        user = User.objects.get(pk=2)
    return user

def get_book(request):
    book = Book.objects.get(pk=request.POST['book'])
    return book

class BookSearch(APIView):
    def get(self, request):
        title = request.GET.get('title', None)
        if title is None:
            return HttpResponseNotAllowed(request);
          
        books = Book.objects.filter(title__icontains=title)[:10]
        
        json_text = list(map(lambda x: x.to_json(), books.all()))
        return JsonResponse(json_text, safe=False)
    
class BookList(APIView):
    def get(self, request):
        books = Book.objects.all()[:10]
        
        json_text = list(map(lambda x: x.to_json(), books.all()))
        return JsonResponse(json_text, safe=False)
            
class BookNoteList(APIView):
    def get(self, request):
        notes = BookNote.objects.all()[:20]
        json_text = list(map(lambda x: x.to_json(), notes.all()))
        
        return JsonResponse(json_text, safe=False)
    
    def post(self, request):
        form = BookNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save();
        
        if form:
            return JsonResponse(note.to_json(), safe=False)
    
class BookNoteDetail(APIView):
    def get(self, request, pk):
        note = BookNote.objects.get(pk=pk)
        json_text = note.to_json();
        return JsonResponse(json_text, safe=False)
    
    def post(self, request, pk):
        note = BookNote.objects.get(pk=pk)
        if note is None:
            return HttpResponseBadRequest()
        
        serializer = BookNoteWriteSerializer(instance = note, data=request.data)
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

class BookNoteLikeItUpdate(APIView):
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
        
class BookNoteReplyList(APIView):
    def get(self, request, note_id):
        if note_id is None:
            return HttpResponseBadRequest(request);
        
        replies = BookNoteReply.objects.filter(note__pk = note_id)
        json_text = list(map(lambda x: x.to_json(), replies.all()))
        
        return JsonResponse(json_text, safe=False)
    
    def post(self, request, note_id):
        if note_id is None:
            return HttpResponseBadRequest(request);
        
        reply = BookNoteReply()
        reply.user = get_current_user(request)
        reply.note = BookNote.objects.get(pk=note_id)
        reply.content = request.data.get('content')
        reply.save()
        
        return JsonResponse(reply.to_json(), safe = False)
    
class BookNoteReplyDetail(APIView):
    def post(self, request, note_id, reply_id):
        if reply_id is None:
            return HttpResponseBadRequest(request);
        
        reply = BookNoteReply.objects.get(pk=reply_id)
        if reply is None:
            return HttpResponseBadRequest(request);
        
        reply.content = request.data.get('content')
        reply.save()
        return JsonResponse(reply.to_json(), safe = False)
    
    def delete(self, request, note_id, reply_id):
        if reply_id is None:
            return HttpResponseBadRequest(request);
        
        reply = BookNoteReply.objects.get(pk=reply_id)
        if reply:
            reply.delete()
        
        return JsonResponse({'status':'success'}, safe = False)