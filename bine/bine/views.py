from bine.models import BookNote, BookNoteReply, User
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.views.generic.base import View
import json

class BookNoteList(View):
    def get(self, request):
        notes = BookNote.objects.all()
        json = list(map(lambda x: x.to_json(), notes.all()))
        
        return JsonResponse(json, safe=False)
    
class BookNoteDetail(View):
    def get(self, request, pk):
        note = BookNote.objects.get(pk=pk)
        json = note.to_json();
        return JsonResponse(json, safe=False)

class NoteReplyList(View):
    def get(self, request, note_id):
        if note_id is None:
            return HttpResponseBadRequest(request);
        
        replies = BookNoteReply.objects.filter(note__pk = note_id)
        json = list(map(lambda x: x.to_json(), replies.all()))
        
        return JsonResponse(json, safe=False)
    
    def post(self, request, note_id):
        if note_id is None:
            return HttpResponseBadRequest(request);
        
        json_data =  json.loads(request.body.decode('utf-8'))
        reply = BookNoteReply()
        reply.user = User.objects.first()
        reply.note = BookNote.objects.get(pk=note_id)
        reply.content = json_data.get('content')
        reply.save()
        
        return JsonResponse(reply.to_json(), safe = False)
    
class NoteReplyDetail(View):
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