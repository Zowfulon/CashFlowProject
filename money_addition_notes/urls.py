from django.urls import path

from money_addition_notes.views import MoneyAdditionNotesView, notes_filter, \
    change_tabs

app_name = 'notes'

urlpatterns = [
    path('', MoneyAdditionNotesView.as_view(), name='money_page'),
    path('filter/', notes_filter, name='notes_filter'),
    path('change_tabs/', change_tabs, name='change_tabs')
]
