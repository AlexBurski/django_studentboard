from django.shortcuts import render, redirect
from .models import Notes, Homework, ToDo
from .forms import NotesForm, HomeworkForm, DashboardForm,ToDoForm, ConversionalForm, \
    ConversionMassForm, ConversionLengthForm, UserRegistrationForm
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
   return  render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method =='POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            nots = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            nots.save()
        messages.success(request, f'New note from {request.user.username} added successfully!')
    else:
        form = NotesForm()
    nots = Notes.objects.filter(user=request.user)
    context = {'notes': nots, 'form': form, }#'messages': messages}
    return render(request, 'dashboard/notes.html', context)

@login_required
def delete_notes(request, pk=None):
    Notes.objects.get(id=pk).delete()
    messages.success(request, f'Note deleted!')
    return redirect('notes')


class NotesDetailView(generic.DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            new_homework = Homework(
                user = request.user,
                title = request.POST['title'],
                subject=request.POST['subject'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            new_homework.save()
            messages.success(request, f'Homework from {request.user.username} added successfully!')

    else:
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks':homeworks, 'homework_done':homework_done, 'form':form}
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request, pk=None):
    taken_homework = Homework.objects.get(id=pk)
    if taken_homework.is_finished:
        taken_homework.is_finished = False
    else:
        taken_homework.is_finished = True
    taken_homework.save()
    return redirect('homework')

@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    messages.info(request, f'Homework deleted!')
    return redirect('homework')

@login_required
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        videos = VideosSearch(text, limit=10)
        result_list = []
        for video in videos.result()['result']:
            result_dict ={
                'input': text,
                'title': video['title'],
                'duration': video['duration'],
                'thumbnail': video['thumbnails'][0]['url'],
                'channel': video['channel']['name'],
                'link': video['link'],
                'views': video['viewCount']['short'],
                'published': video['publishedTime'],
            }
            desc = ''
            if video['descriptionSnippet']:
                for j in video['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            new_context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/youtube.html', new_context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)

@login_required
def todo(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished=='on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = ToDo(
                user = request.user,
                title = request.POST['title'],
                is_finished= finished
            )
            todos.save()
            messages.success(request, f'To-do Added from {request.user}')
    else:
        form = ToDoForm()
    todos = ToDo.objects.filter(user=request.user)
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'todos':todos,
        'form':form,
        'todo_done':todo_done,
    }
    return render(request, 'dashboard/todo.html', context)

@login_required
def delete_todo(request, pk=None):
    ToDo.objects.get(id=pk).delete()
    messages.info(request, f'To-do deleted!')
    return redirect('to-do')

@login_required
def update_todo(request, pk=None):
    taken_todo = ToDo.objects.get(id=pk)
    if taken_todo.is_finished:
        taken_todo.is_finished = False
    else:
        taken_todo.is_finished = True
    taken_todo.save()
    return redirect('to-do')


def books(request):  # Bug: cannot make request
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        print(r)
        answer = r.json()
        print(answer)
        result_list = []
        print(answer)
        for book_ in range(10):
            result_dict ={
                'title': answer['items'][book_]['volumeInfo']['title'],
                'subtitle': answer['items'][book_]['volumeInfo'].get('subtitle'),
                'description': answer['items'][book_]['volumeInfo'].get('description'),
                'count': answer['items'][book_]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][book_]['volumeInfo'].get('categories'),
                'rating': answer['items'][book_]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][book_]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][book_]['volumeInfo'].get('previewLink'),
            }

            result_list.append(result_dict)
            new_context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html', new_context)
    else:
        form = DashboardForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()
        print(answer[0])
        try:

            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][1]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0].get('example', '')
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
            print('ok')
        except:
            context= {
                'form': form,
                'input': ''
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):  # Bug: not precise search. Not everything can be found ToDo
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary,
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
        'form': form
        }
    return render(request, 'dashboard/wiki.html', context)


def conversion(request):
    if request.method == 'POST':
        form = ConversionalForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }

        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {round(int(input)/2.205, 2)} kilos'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilos = {int(input)* 2.205} pound'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
    else:
        form = ConversionalForm()
        context = {
        'form': form,
        'input': False
    }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegistrationForm
    context = {
        'form': form
            }
    return render(request, 'dashboard/register.html', context)

@login_required
def profile(request):
    homework_ = Homework.objects.filter(is_finished=False, user= request.user)
    todos_ = ToDo.objects.filter(is_finished=False, user=request.user)
    if len(homework_) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos_) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks': homework_,
        'todos': todos_,
        'homework_done':homework_done,
        'todos_done': todos_done,
    }
    return render(request, 'dashboard/profile.html', context)