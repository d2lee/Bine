from bine.models import BookNote, BookNoteReply, User, Book, BookNoteLikeit
from bine.serializers import BookNoteWriteSerializer
from rest_framework.views import APIView
from bine.forms import BookNoteForm
from django.http.response import JsonResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST,\
    HTTP_200_OK
from rest_framework.response import Response
from django.views.generic.base import View
from django.shortcuts import render, redirect
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework import response

def get_book(request):
    book = Book.objects.get(pk=request.POST['book'])
    return book

def auth_response_payload_handler(token, user=None):
    return {
        'token': token,
        'user' : user.to_json()
    }


class IndexView(View):
    def get(self, request):
        return redirect('/static/bine/html/bine.html')
        
class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        if not (username and password):
            return JsonResponse(status=HTTP_400_BAD_REQUEST)
        
        if request.user:
            logout(request)
            
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(user.to_json(), status=HTTP_200_OK)
        
        return Response(status=HTTP_403_FORBIDDEN)
    
class Register(APIView):
    def post(self, request):
        username = request.data['username']
        fullname = request.data['fullname']
        birthday = request.data['birthday']
        sex = request.data['sex']
        email = request.data['email']
        password = request.data['password']
        
        # validation code is required here        
        user = User.objects.create_user(username=username, 
                                 fullname=fullname,
                                 birthday=birthday,
                                 sex=sex,
                                 email = email,
                                 password=password)
        if user is not None:
            serializer = self.JSONWebTokenSerializer(data=request.DATA)
            if serializer.is_valid():
                token = serializer.object.get('token')
                response_data = auth_response_payload_handler(token, user)
                return Response(response_data);
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_403_FORBIDDEN)
    

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
        if request.user is None:
            return response(status= HTTP_400_BAD_REQUEST)
            
        notes = request.user.booknotes.all();
        #notes = BookNote.objects.all()[:20]
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
        user = request.user
        note = BookNote.objects.get(pk=note_id)
        
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
        reply.user = request.user
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