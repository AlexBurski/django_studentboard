from django.urls import path
from .views import home, notes, delete_notes, \
    NotesDetailView, homework, update_homework, delete_homework, youtube, todo, delete_todo, \
    update_todo, books, dictionary, wiki, conversion

urlpatterns = [
    path('', home, name='home'),

    path('notes/', notes, name='notes'),
    path('delete_note/<int:pk>', delete_notes, name='delete-note'),
    path('notes_detail/<int:pk>', NotesDetailView.as_view(), name='notes-detail'),

    path('homework/', homework, name='homework'),
    path('update_homework/<int:pk>', update_homework, name='update-homework'),
    path('delete_homework/<int:pk>', delete_homework, name='delete-homework'),

    path('youtube/', youtube, name='youtube'),

    path('to_do/', todo, name='to-do'),
    path('delete_todo/<int:pk>', delete_todo, name='delete-todo'),
    path('update_todo/<int:pk>', update_todo, name='update-to-do'),

    path('books/', books, name='books'),

    path('dictionary/', dictionary, name='dictionary'),

    path('wiki/', wiki, name='wiki'),

    path('conversion/', conversion, name='conversion'),


]
