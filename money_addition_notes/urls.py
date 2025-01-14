from django.urls import path

from money_addition_notes.views import MoneyAdditionNotesView, notes_filter, \
    change_tabs, NotesDetailView, NoteCreateView

app_name = 'notes'

urlpatterns = [
    path('', MoneyAdditionNotesView.as_view(), name='money_page'),
    path('filter/', notes_filter, name='notes_filter'),
    path('change_tabs/', change_tabs, name='change_tabs'),
    path('create/', NoteCreateView.as_view(), name='create_note'),
    path('<pk>/change/', NotesDetailView.as_view(), name='change_note')
]
